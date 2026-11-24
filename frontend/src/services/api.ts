import {
  BirthProfile,
  BirthChartData,
  DashaData,
  PanchangData,
  YogaDetail,
  DoshaDetail,
  AshtakootaMatchingData,
  VerificationCase,
  DashboardSummary,
} from '../types';
import { searchClientCities, CityLocation } from '../data/majorCities';

const API_BASE = '/api';

// Helper: Resolve exact historical UTC offset for any IANA timezone and date
function getUtcOffsetForDate(tzName: string, dateStr: string = '2000-01-01'): number {
  try {
    const d = new Date(dateStr + 'T12:00:00Z');
    const formatter = new Intl.DateTimeFormat('en-US', {
      timeZone: tzName,
      timeZoneName: 'longOffset',
    });
    const parts = formatter.formatToParts(d);
    const tzPart = parts.find((p) => p.type === 'timeZoneName')?.value;
    if (tzPart) {
      const match = tzPart.match(/GMT([+-])(\d{1,2}):?(\d{2})?/);
      if (match) {
        const sign = match[1] === '-' ? -1 : 1;
        const hours = parseInt(match[2], 10);
        const mins = match[3] ? parseInt(match[3], 10) : 0;
        return sign * (hours + mins / 60.0);
      }
    }
  } catch {
    // ignore
  }

  const tzOffsets: Record<string, number> = {
    'Asia/Kolkata': 5.5,
    'Asia/Calcutta': 5.5,
    'Asia/Dubai': 4.0,
    'Asia/Kathmandu': 5.75,
    'Asia/Colombo': 5.5,
    'Asia/Singapore': 8.0,
    'Asia/Tokyo': 9.0,
    'Europe/London': 0.0,
    'America/New_York': -5.0,
    'America/Los_Angeles': -8.0,
    'America/Chicago': -6.0,
  };
  return tzOffsets[tzName] ?? 5.5;
}

export const api = {
  // Profiles
  async getProfiles(): Promise<BirthProfile[]> {
    const res = await fetch(`${API_BASE}/profiles/`);
    if (!res.ok) throw new Error('Failed to fetch profiles');
    return res.json();
  },

  async createProfile(data: Partial<BirthProfile>): Promise<BirthProfile> {
    const res = await fetch(`${API_BASE}/profiles/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to create profile');
    return res.json();
  },

  async updateProfile(id: number, data: Partial<BirthProfile>): Promise<BirthProfile> {
    const res = await fetch(`${API_BASE}/profiles/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to update profile');
    return res.json();
  },

  async deleteProfile(id: number): Promise<void> {
    const res = await fetch(`${API_BASE}/profiles/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to delete profile');
  },

  // External Public Geocoding & Timezone API (Live Public APIs: Open-Meteo + OpenStreetMap + Photon)
  async searchLocation(query: string, dateStr?: string): Promise<any[]> {
    const qTrim = query ? query.trim() : '';
    if (qTrim.length < 2) return [];

    // 1. Primary External Public API: Open-Meteo Geocoding API
    // High accuracy coordinates, exact IANA timezone, free, CORS enabled, no API key needed
    try {
      const openMeteoUrl = `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(qTrim)}&count=8&language=en&format=json`;
      const res = await fetch(openMeteoUrl, { signal: AbortSignal.timeout(4000) });
      if (res.ok) {
        const data = await res.json();
        if (data && Array.isArray(data.results) && data.results.length > 0) {
          return data.results.map((item: any) => {
            const city = item.name;
            const state = item.admin1 || item.admin2 || '';
            const country = item.country || '';
            const disp = `${city}${state ? ', ' + state : ''}, ${country}`;
            const tz = item.timezone || (country.toLowerCase() === 'india' ? 'Asia/Kolkata' : 'UTC');
            const offset = getUtcOffsetForDate(tz, dateStr || '2000-01-01');

            return {
              display_name: disp,
              city: city,
              state: state,
              country: country,
              latitude: Math.round(item.latitude * 10000) / 10000,
              longitude: Math.round(item.longitude * 10000) / 10000,
              timezone_str: tz,
              timezone_offset: offset,
              source: 'Open-Meteo Public API',
            };
          });
        }
      }
    } catch (err) {
      console.warn('Open-Meteo external geocoding failed, trying OpenStreetMap...', err);
    }

    // 2. Secondary External Public API: OpenStreetMap Nominatim
    try {
      const nominatimUrl = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(qTrim)}&format=json&addressdetails=1&limit=8`;
      const res = await fetch(nominatimUrl, {
        headers: { 'Accept-Language': 'en' },
        signal: AbortSignal.timeout(4000),
      });
      if (res.ok) {
        const items = await res.json();
        if (Array.isArray(items) && items.length > 0) {
          return items.map((item: any) => {
            const lat = parseFloat(item.lat);
            const lon = parseFloat(item.lon);
            const addr = item.address || {};
            const city = addr.city || addr.town || addr.village || addr.municipality || item.display_name.split(',')[0];
            const state = addr.state || addr.region || '';
            const country = addr.country || '';
            const isIndia = country.toLowerCase().includes('india') || (lat >= 6 && lat <= 38 && lon >= 68 && lon <= 98);
            const tz = isIndia ? 'Asia/Kolkata' : 'UTC';
            const offset = isIndia ? 5.5 : Math.round((lon / 15.0) * 2) / 2;

            return {
              display_name: item.display_name,
              city: city,
              state: state,
              country: country,
              latitude: Math.round(lat * 10000) / 10000,
              longitude: Math.round(lon * 10000) / 10000,
              timezone_str: tz,
              timezone_offset: offset,
              source: 'OpenStreetMap Public API',
            };
          });
        }
      }
    } catch (err) {
      console.warn('Nominatim external geocoding failed, trying Photon...', err);
    }

    // 3. Tertiary External Public API: Komoot Photon
    try {
      const photonUrl = `https://photon.komoot.io/api/?q=${encodeURIComponent(qTrim)}&limit=8`;
      const res = await fetch(photonUrl, { signal: AbortSignal.timeout(3500) });
      if (res.ok) {
        const pData = await res.json();
        const features = pData.features || [];
        if (features.length > 0) {
          return features.map((f: any) => {
            const coords = f.geometry?.coordinates || [0, 0];
            const lon = coords[0];
            const lat = coords[1];
            const p = f.properties || {};
            const city = p.city || p.name || qTrim;
            const state = p.state || '';
            const country = p.country || '';
            const disp = `${city}${state ? ', ' + state : ''}${country ? ', ' + country : ''}`;
            const isIndia = country.toLowerCase().includes('india') || (lat >= 6 && lat <= 38 && lon >= 68 && lon <= 98);
            const tz = isIndia ? 'Asia/Kolkata' : 'UTC';
            const offset = isIndia ? 5.5 : Math.round((lon / 15.0) * 2) / 2;

            return {
              display_name: disp,
              city: city,
              state: state,
              country: country,
              latitude: Math.round(lat * 10000) / 10000,
              longitude: Math.round(lon * 10000) / 10000,
              timezone_str: tz,
              timezone_offset: offset,
              source: 'Photon Public API',
            };
          });
        }
      }
    } catch (err) {
      console.warn('Photon external geocoding failed...', err);
    }

    // 4. Offline Fallback: Built-in Major Cities Database
    return searchClientCities(qTrim, 8);
  },

  // Chart
  async getBirthChart(
    profileId: number,
    ayanamsa = 'LAHIRI',
    nodeType = 'TRUE_NODE',
    houseSystem = 'WHOLE_SIGN'
  ): Promise<BirthChartData> {
    const url = `${API_BASE}/chart/calculate/${profileId}?ayanamsa=${ayanamsa}&node_type=${nodeType}&house_system=${houseSystem}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to calculate birth chart');
    return res.json();
  },

  // Divisional Chart
  async getDivisionalChart(profileId: number, vargaKey: string): Promise<any> {
    const res = await fetch(`${API_BASE}/calculations/divisional/${profileId}/${vargaKey}`);
    if (!res.ok) throw new Error(`Failed to calculate ${vargaKey} chart`);
    return res.json();
  },

  async getFullVargaWorksheet(
    profileId: number,
    vargaKey: string,
    ayanamsa = 'LAHIRI',
    nodeType = 'TRUE_NODE'
  ): Promise<any> {
    const res = await fetch(
      `${API_BASE}/calculations/varga-full/${profileId}/${vargaKey}?ayanamsa=${ayanamsa}&node_type=${nodeType}`
    );
    if (!res.ok) throw new Error(`Failed to load ${vargaKey} details`);
    return res.json();
  },

  // Dasha
  async getDashaTimeline(profileId: number, targetDate?: string): Promise<DashaData> {
    const query = targetDate ? `?target_date=${targetDate}` : '';
    const res = await fetch(`${API_BASE}/calculations/dasha/${profileId}${query}`);
    if (!res.ok) throw new Error('Failed to calculate Dasha timeline');
    return res.json();
  },

  // Panchang
  async getPanchang(date: string, lat = 28.6139, lon = 77.2090, tz = 5.5): Promise<PanchangData> {
    const res = await fetch(`${API_BASE}/calculations/panchang?date=${date}&latitude=${lat}&longitude=${lon}&timezone_offset=${tz}`);
    if (!res.ok) throw new Error('Failed to calculate Panchang');
    return res.json();
  },

  // Yogas & Doshas
  async getYogas(profileId: number): Promise<YogaDetail[]> {
    const res = await fetch(`${API_BASE}/calculations/yogas/${profileId}`);
    if (!res.ok) throw new Error('Failed to calculate Yogas');
    return res.json();
  },

  async getDoshas(profileId: number): Promise<DoshaDetail[]> {
    const res = await fetch(`${API_BASE}/calculations/doshas/${profileId}`);
    if (!res.ok) throw new Error('Failed to calculate Doshas');
    return res.json();
  },

  // Matching
  async matchProfiles(boyId: number, girlId: number): Promise<AshtakootaMatchingData> {
    const res = await fetch(`${API_BASE}/calculations/matching?boy_profile_id=${boyId}&girl_profile_id=${girlId}`);
    if (!res.ok) throw new Error('Failed to calculate matching');
    return res.json();
  },

  // Transits
  async getTransits(profileId?: number, date?: string): Promise<any> {
    let url = `${API_BASE}/calculations/transits?`;
    if (profileId) url += `profile_id=${profileId}&`;
    if (date) url += `transit_date=${date}&`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to calculate transits');
    return res.json();
  },

  // AI Chat
  async sendChatMessage(profileId: number, message: string, history: { role: string; content: string }[]): Promise<any> {
    const res = await fetch(`${API_BASE}/ai/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        profile_id: profileId,
        message,
        conversation_history: history,
      }),
    });
    if (!res.ok) throw new Error('AI Chat query failed');
    return res.json();
  },

  // Verification & QA
  async getVerificationCases(): Promise<VerificationCase[]> {
    const res = await fetch(`${API_BASE}/verification/cases`);
    if (!res.ok) throw new Error('Failed to fetch verification cases');
    return res.json();
  },

  async runVerificationCase(caseId: number): Promise<any> {
    const res = await fetch(`${API_BASE}/verification/run/${caseId}`, { method: 'POST' });
    if (!res.ok) throw new Error(`Verification test ${caseId} failed`);
    return res.json();
  },

  async runAllVerificationCases(): Promise<any> {
    const res = await fetch(`${API_BASE}/verification/run-all`, { method: 'POST' });
    if (!res.ok) throw new Error('Run all verification failed');
    return res.json();
  },

  // Dashboard & Settings
  async getDashboardSummary(): Promise<DashboardSummary> {
    const res = await fetch(`${API_BASE}/settings/dashboard-summary`);
    if (!res.ok) throw new Error('Failed to fetch dashboard summary');
    return res.json();
  },

  async getEngineStatus(): Promise<any> {
    const res = await fetch(`${API_BASE}/settings/status`);
    if (!res.ok) throw new Error('Failed to fetch engine status');
    return res.json();
  },

  async updateEngineSettings(settings: { ayanamsa?: string; node_type?: string; house_system?: string }): Promise<any> {
    let query = new URLSearchParams(settings as any).toString();
    const res = await fetch(`${API_BASE}/settings/update?${query}`, { method: 'POST' });
    if (!res.ok) throw new Error('Failed to update engine settings');
    return res.json();
  },
};
