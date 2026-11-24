import React, { useState, useEffect, useRef } from 'react';
import {
  LayoutDashboard,
  User,
  Compass,
  Table,
  Home,
  Layers,
  Sparkles,
  Clock,
  Calendar,
  Flame,
  AlertTriangle,
  HeartHandshake,
  Navigation,
  Bot,
  CheckCircle2,
  History,
  Settings as SettingsIcon,
  ChevronRight,
  RefreshCw,
  Send,
  Plus,
  Trash2,
  Search,
  MapPin,
  Check,
  Globe,
  FileSpreadsheet,
} from 'lucide-react';
import { api } from './services/api';
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
  HouseCusp,
} from './types';
import { NorthIndianChart } from './charts/NorthIndianChart';
import { SouthIndianChart } from './charts/SouthIndianChart';
import { ParasharaLightWorksheet } from './components/ParasharaLightWorksheet';
import { ParasharaDashaCard } from './components/ParasharaDashaCard';

export function App() {
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [profiles, setProfiles] = useState<BirthProfile[]>([]);
  const [selectedProfileId, setSelectedProfileId] = useState<number | null>(null);
  const [chartData, setChartData] = useState<BirthChartData | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [chartFormat, setChartFormat] = useState<'north' | 'south'>('north');
  const [selectedHouse, setSelectedHouse] = useState<HouseCusp | null>(null);

  // Settings
  const [activeAyanamsa, setActiveAyanamsa] = useState<string>('LAHIRI');
  const [activeNodeType, setActiveNodeType] = useState<string>('TRUE_NODE');
  const [dashboardData, setDashboardData] = useState<DashboardSummary | null>(null);

  // AI Chat
  const [chatMessages, setChatMessages] = useState<{ role: string; content: string; source?: string }[]>([]);
  const [chatInput, setChatInput] = useState<string>('');
  const [chatLoading, setChatLoading] = useState<boolean>(false);

  // Verification
  const [verificationCases, setVerificationCases] = useState<VerificationCase[]>([]);
  const [verificationLoading, setVerificationLoading] = useState<boolean>(false);

  // Specific Feature Data
  const [selectedVarga, setSelectedVarga] = useState<string>('D9');
  const [vargaData, setVargaData] = useState<any>(null);
  const [vargaD9Data, setVargaD9Data] = useState<any>(null);
  const [dashaData, setDashaData] = useState<DashaData | null>(null);
  const [panchangData, setPanchangData] = useState<PanchangData | null>(null);
  const [yogasData, setYogasData] = useState<YogaDetail[]>([]);
  const [doshasData, setDoshasData] = useState<DoshaDetail[]>([]);
  const [transitsData, setTransitsData] = useState<any>(null);

  // Matching Profile Selectors
  const [boyProfileId, setBoyProfileId] = useState<number | null>(null);
  const [girlProfileId, setGirlProfileId] = useState<number | null>(null);
  const [matchingResult, setMatchingResult] = useState<AshtakootaMatchingData | null>(null);

  // 12-Hour AM/PM Time State
  const [timeHour12, setTimeHour12] = useState<number>(6);
  const [timeMinute, setTimeMinute] = useState<number>(33);
  const [timeSecond, setTimeSecond] = useState<number>(0);
  const [timeAmPm, setTimeAmPm] = useState<'AM' | 'PM'>('AM');

  // Location search state
  const [locationQuery, setLocationQuery] = useState<string>('Kolkata, West Bengal, India');
  const [locationResults, setLocationResults] = useState<any[]>([]);
  const [isSearchingLocation, setIsSearchingLocation] = useState<boolean>(false);
  const [showLocationDropdown, setShowLocationDropdown] = useState<boolean>(false);
  const [showManualCoords, setShowManualCoords] = useState<boolean>(false);
  const locationSearchTimeoutRef = useRef<any>(null);

  // Profile Form
  const [newProfile, setNewProfile] = useState({
    name: 'Swami Vivekananda',
    gender: 'Male',
    date_of_birth: '1863-01-12',
    time_of_birth: '06:33:00',
    birthplace: 'Kolkata, West Bengal, India',
    country: 'India',
    state: 'West Bengal',
    city: 'Kolkata',
    latitude: 22.5726,
    longitude: 88.3639,
    timezone_str: 'Asia/Kolkata',
    timezone_offset: 5.5,
  });

  // Convert 12h + AM/PM to 24h string
  const formatTime24 = (h12: number, min: number, sec: number, ampm: 'AM' | 'PM'): string => {
    let h24 = h12;
    if (ampm === 'AM') {
      if (h12 === 12) h24 = 0;
    } else {
      if (h12 !== 12) h24 = h12 + 12;
    }
    const hh = String(h24).padStart(2, '0');
    const mm = String(min).padStart(2, '0');
    const ss = String(sec).padStart(2, '0');
    return `${hh}:${mm}:${ss}`;
  };

  // Sync 24-hr time when 12-hr inputs change
  useEffect(() => {
    const t24 = formatTime24(timeHour12, timeMinute, timeSecond, timeAmPm);
    setNewProfile((prev) => ({ ...prev, time_of_birth: t24 }));
  }, [timeHour12, timeMinute, timeSecond, timeAmPm]);

  // Instant Location Autocomplete
  const handleLocationInputChange = async (val: string) => {
    setLocationQuery(val);
    setNewProfile((prev) => ({ ...prev, birthplace: val }));
    if (!val || val.trim().length < 2) {
      setLocationResults([]);
      setShowLocationDropdown(false);
      return;
    }

    setIsSearchingLocation(true);
    try {
      const results = await api.searchLocation(val, newProfile.date_of_birth);
      setLocationResults(results);
      setShowLocationDropdown(results.length > 0);
    } catch (e) {
      console.error(e);
    } finally {
      setIsSearchingLocation(false);
    }
  };

  // Select location from suggestion list
  const handleSelectLocation = (loc: any) => {
    setNewProfile((prev) => ({
      ...prev,
      birthplace: loc.display_name,
      city: loc.city || loc.display_name.split(',')[0],
      state: loc.state || '',
      country: loc.country || '',
      latitude: loc.latitude,
      longitude: loc.longitude,
      timezone_str: loc.timezone_str,
      timezone_offset: loc.timezone_offset,
    }));
    setLocationQuery(loc.display_name);
    setShowLocationDropdown(false);
  };

  // Initial Load
  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      const [pList, dSummary, vCases] = await Promise.all([
        api.getProfiles(),
        api.getDashboardSummary(),
        api.getVerificationCases(),
      ]);
      setProfiles(pList);
      setDashboardData(dSummary);
      setVerificationCases(vCases);

      if (pList.length > 0) {
        setSelectedProfileId(pList[0].id);
        setBoyProfileId(pList[0].id);
        if (pList.length > 1) {
          setGirlProfileId(pList[1].id);
        }
      }
    } catch (err) {
      console.error('Initialization error:', err);
    }
  };

  // Re-calculate chart when profile or calculation settings change
  useEffect(() => {
    if (selectedProfileId) {
      loadChart(selectedProfileId);
    }
  }, [selectedProfileId, activeAyanamsa, activeNodeType]);

  const loadChart = async (profileId: number) => {
    setLoading(true);
    try {
      const chart = await api.getBirthChart(profileId, activeAyanamsa, activeNodeType);
      setChartData(chart);
      setSelectedHouse(chart.houses[0]);

      // Load sub-modules in parallel
      const [varga, d9, dasha, yogas, doshas, transits] = await Promise.all([
        api.getDivisionalChart(profileId, selectedVarga),
        api.getDivisionalChart(profileId, 'D9'),
        api.getDashaTimeline(profileId),
        api.getYogas(profileId),
        api.getDoshas(profileId),
        api.getTransits(profileId),
      ]);

      setVargaData(varga);
      setVargaD9Data(d9);
      setDashaData(dasha);
      setYogasData(yogas);
      setDoshasData(doshas);
      setTransitsData(transits);
    } catch (err) {
      console.error('Chart calculation error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Load Daily Panchang
  useEffect(() => {
    const today = new Date().toISOString().split('T')[0];
    api.getPanchang(today).then(setPanchangData).catch(console.error);
  }, []);

  // Handle Divisional Chart Change
  const handleVargaChange = async (vKey: string) => {
    setSelectedVarga(vKey);
    if (selectedProfileId) {
      try {
        const v = await api.getDivisionalChart(selectedProfileId, vKey);
        setVargaData(v);
      } catch (err) {
        console.error(err);
      }
    }
  };

  // Handle AI Chat
  const handleSendChat = async () => {
    if (!chatInput.trim() || !selectedProfileId) return;
    const userMsg = chatInput.trim();
    setChatInput('');
    const newHistory = [...chatMessages, { role: 'user', content: userMsg }];
    setChatMessages(newHistory);
    setChatLoading(true);

    try {
      const res = await api.sendChatMessage(selectedProfileId, userMsg, newHistory);
      setChatMessages([
        ...newHistory,
        { role: 'assistant', content: res.response, source: res.source },
      ]);
    } catch (err) {
      setChatMessages([
        ...newHistory,
        { role: 'assistant', content: 'Calculation engine response failed. Please retry.' },
      ]);
    } finally {
      setChatLoading(false);
    }
  };

  // Handle Run All Verification
  const handleRunAllVerification = async () => {
    setVerificationLoading(true);
    try {
      await api.runAllVerificationCases();
      const updated = await api.getVerificationCases();
      setVerificationCases(updated);
      const dSummary = await api.getDashboardSummary();
      setDashboardData(dSummary);
    } catch (err) {
      console.error(err);
    } finally {
      setVerificationLoading(false);
    }
  };

  // Handle Create Profile
  const handleCreateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const created = await api.createProfile(newProfile);
      setProfiles([created, ...profiles]);
      setSelectedProfileId(created.id);
      setActiveTab('parashara-sheet');
    } catch (err) {
      alert('Error saving profile');
    }
  };

  // Handle Matching
  const handleRunMatching = async () => {
    if (!boyProfileId || !girlProfileId) return;
    try {
      const res = await api.matchProfiles(boyProfileId, girlProfileId);
      setMatchingResult(res);
    } catch (err) {
      alert('Matching calculation failed');
    }
  };

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'profiles', label: 'Birth Profile', icon: User },
    { id: 'parashara-sheet', label: 'Kundli Worksheet (D1-D60)', icon: FileSpreadsheet },
    { id: 'planets', label: 'Planetary Positions', icon: Table },
    { id: 'houses', label: 'House Analysis', icon: Home },
    { id: 'divisional', label: 'Divisional Charts (D1-D60)', icon: Layers },
    { id: 'dasha', label: 'Vimshottari Dasha', icon: Clock },
    { id: 'panchang', label: 'Daily Panchang', icon: Calendar },
    { id: 'doshas', label: 'Dosha Analysis', icon: AlertTriangle },
    { id: 'matching', label: 'Kundli Matching', icon: HeartHandshake },
    { id: 'transits', label: 'Transit Analysis', icon: Navigation },
    { id: 'ai-chat', label: 'AI Astrology Chat', icon: Bot },
    { id: 'verification', label: 'Calculation Verification', icon: CheckCircle2 },
    { id: 'test-history', label: 'Test History', icon: History },
    { id: 'settings', label: 'Engine Settings', icon: SettingsIcon },
  ];

  const currentProfile = profiles.find((p) => p.id === selectedProfileId);

  return (
    <div className="flex h-screen bg-[#F8FAFC] text-slate-800 overflow-hidden">
      {/* SIDEBAR NAVIGATION */}
      <aside className="w-64 bg-[#0B1B3D] text-white flex flex-col border-r border-slate-800 select-none flex-shrink-0">
        {/* Brand Header */}
        <div className="p-4 border-b border-slate-800 flex items-center justify-between">
          <div>
            <h1 className="font-cinzel text-lg font-bold tracking-wider text-amber-400">
              AstroRize
            </h1>
            <p className="text-[10px] text-slate-400 tracking-widest uppercase font-mono">
              Vedic Research Lab
            </p>
          </div>
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" title="Swiss Ephemeris Active" />
        </div>

        {/* Engine Status Pill */}
        <div className="mx-3 my-2 p-2 bg-[#071026] rounded-lg border border-slate-700/60 flex items-center justify-between text-[11px]">
          <div>
            <div className="text-slate-400 text-[9px] uppercase font-mono tracking-wider">Engine</div>
            <div className="font-semibold text-amber-200">Swiss Ephemeris 2.10</div>
          </div>
          <span className="bg-amber-400/20 text-amber-300 text-[10px] font-mono px-1.5 py-0.5 rounded">
            {activeAyanamsa}
          </span>
        </div>

        {/* Navigation Links */}
        <nav className="flex-1 overflow-y-auto px-2 py-1 space-y-0.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center justify-between px-3 py-2 text-xs font-medium rounded-lg transition-all ${
                  isActive
                    ? 'bg-amber-400/15 text-amber-300 border-l-2 border-amber-400'
                    : 'text-slate-300 hover:bg-slate-800/60 hover:text-white'
                }`}
              >
                <div className="flex items-center space-x-2.5 truncate">
                  <Icon className={`w-4 h-4 ${isActive ? 'text-amber-400' : 'text-slate-400'}`} />
                  <span className="truncate">{item.label}</span>
                </div>
                {isActive && <ChevronRight className="w-3.5 h-3.5 text-amber-400" />}
              </button>
            );
          })}
        </nav>

        {/* Footer info */}
        <div className="p-3 border-t border-slate-800 text-[10px] text-slate-400 flex justify-between items-center">
          <span>Local Research Edition</span>
          <span className="text-slate-500 font-mono">v1.0.0</span>
        </div>
      </aside>

      {/* MAIN VIEW AREA */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* TOP BAR */}
        <header className="h-14 bg-white border-b border-slate-200 px-6 flex items-center justify-between flex-shrink-0">
          <div className="flex items-center space-x-4">
            <h2 className="text-base font-semibold text-slate-800 font-cinzel">
              {navItems.find((n) => n.id === activeTab)?.label}
            </h2>
            {currentProfile && (
              <div className="hidden sm:flex items-center text-xs bg-slate-100 text-slate-700 px-2.5 py-1 rounded-full border border-slate-200">
                <span className="font-semibold text-vedic-navy">{currentProfile.name}</span>
                <span className="mx-1.5 text-slate-400">•</span>
                <span>{currentProfile.date_of_birth}</span>
                <span className="mx-1.5 text-slate-400">•</span>
                <span>{currentProfile.time_of_birth}</span>
                <span className="mx-1.5 text-slate-400">•</span>
                <span className="text-slate-500">{currentProfile.city}</span>
              </div>
            )}
          </div>

          <div className="flex items-center space-x-3">
            {/* Profile Selector */}
            <div className="flex items-center space-x-1.5 text-xs">
              <span className="text-slate-500 font-medium">Profile:</span>
              <select
                value={selectedProfileId || ''}
                onChange={(e) => setSelectedProfileId(Number(e.target.value))}
                className="bg-slate-50 border border-slate-300 rounded px-2.5 py-1 text-xs font-medium text-slate-700 focus:outline-none focus:ring-1 focus:ring-amber-400"
              >
                {profiles.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.name} ({p.date_of_birth})
                  </option>
                ))}
              </select>
            </div>

            {/* Ayanamsa Selector */}
            <div className="flex items-center space-x-1.5 text-xs">
              <span className="text-slate-500 font-medium">Ayanamsa:</span>
              <select
                value={activeAyanamsa}
                onChange={(e) => setActiveAyanamsa(e.target.value)}
                className="bg-slate-50 border border-slate-300 rounded px-2 py-1 text-xs font-medium text-slate-700 focus:outline-none focus:ring-1 focus:ring-amber-400"
              >
                <option value="LAHIRI">Lahiri (Chitrapaksha)</option>
                <option value="RAMAN">BV Raman</option>
                <option value="KP">Krishnamurti (KP)</option>
                <option value="TRUE_CITRA">True Chitra</option>
                <option value="FAGAN_BRADLEY">Fagan-Bradley</option>
                <option value="YUKTESHWAR">Sri Yukteshwar</option>
              </select>
            </div>

            {/* Quick Switch to Kundli Worksheet (D1-D60) */}
            <button
              onClick={() => setActiveTab('parashara-sheet')}
              className={`flex items-center space-x-1 px-2.5 py-1 text-xs font-semibold rounded-md transition ${
                activeTab === 'parashara-sheet'
                  ? 'bg-vedic-navy text-amber-300 shadow-sm'
                  : 'bg-amber-50 text-amber-900 border border-amber-300 hover:bg-amber-100'
              }`}
              title="Open D1-D60 Kundli Worksheet View"
            >
              <FileSpreadsheet className="w-3.5 h-3.5" />
              <span className="hidden md:inline">Worksheet (D1-D60)</span>
            </button>

            {/* Refresh Button */}
            <button
              onClick={() => selectedProfileId && loadChart(selectedProfileId)}
              className="p-1.5 text-slate-500 hover:text-slate-800 hover:bg-slate-100 rounded transition"
              title="Recalculate"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            </button>
          </div>
        </header>

        {/* TAB CONTENTS */}
        <main className="flex-1 overflow-y-auto p-6">
          {/* TAB 1: DASHBOARD */}
          {activeTab === 'dashboard' && (
            <div className="space-y-6">
              {/* Telemetry Metric Cards */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                  <div>
                    <div className="text-xs text-slate-500 font-medium uppercase font-mono">Birth Profiles</div>
                    <div className="text-2xl font-bold text-vedic-navy mt-1">
                      {dashboardData?.total_birth_charts ?? profiles.length}
                    </div>
                  </div>
                  <User className="w-8 h-8 text-amber-500/80" />
                </div>
                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                  <div>
                    <div className="text-xs text-slate-500 font-medium uppercase font-mono">Total Calculations</div>
                    <div className="text-2xl font-bold text-vedic-navy mt-1">
                      {dashboardData?.total_calculations_run ?? 0}
                    </div>
                  </div>
                  <Compass className="w-8 h-8 text-indigo-500/80" />
                </div>
                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                  <div>
                    <div className="text-xs text-slate-500 font-medium uppercase font-mono">Automated Tests Passed</div>
                    <div className="text-2xl font-bold text-emerald-600 mt-1">
                      {dashboardData?.passed_test_cases ?? 0} / {dashboardData?.total_test_cases ?? 0}
                    </div>
                  </div>
                  <CheckCircle2 className="w-8 h-8 text-emerald-500/80" />
                </div>
                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                  <div>
                    <div className="text-xs text-slate-500 font-medium uppercase font-mono">Ephemeris Engine</div>
                    <div className="text-sm font-bold text-vedic-navy mt-1">Swiss Ephemeris 2.10</div>
                    <span className="text-[10px] text-emerald-600 font-medium">Operational & Verified</span>
                  </div>
                  <Layers className="w-8 h-8 text-amber-600/80" />
                </div>
              </div>

              {/* Engine Diagnostic Banner */}
              <div className="bg-gradient-to-r from-[#0B1B3D] to-[#1E293B] text-white p-5 rounded-xl border border-slate-800 flex flex-col md:flex-row justify-between items-start md:items-center">
                <div>
                  <h3 className="font-cinzel text-base font-bold text-amber-300">
                    Swiss Ephemeris High-Precision Planetary Engine
                  </h3>
                  <p className="text-xs text-slate-300 mt-1 max-w-2xl leading-relaxed">
                    Geocentric sidereal calculations with Lahiri Chitrapaksha Ayanamsa. Fully verified via automated pytest suite with zero approximations.
                  </p>
                </div>
                <button
                  onClick={() => setActiveTab('verification')}
                  className="mt-3 md:mt-0 px-4 py-2 bg-amber-400 text-vedic-navy text-xs font-semibold rounded-lg hover:bg-amber-300 transition shadow"
                >
                  Inspect Verification QA
                </button>
              </div>

              {/* Recent Profiles & Calculation Logs */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                  <div className="flex justify-between items-center mb-4">
                    <h4 className="font-cinzel text-sm font-bold text-vedic-navy">Saved Profiles</h4>
                    <button
                      onClick={() => setActiveTab('profiles')}
                      className="text-xs text-amber-600 hover:underline font-medium"
                    >
                      Manage Profiles →
                    </button>
                  </div>
                  <div className="divide-y divide-slate-100">
                    {profiles.map((p) => (
                      <div
                        key={p.id}
                        onClick={() => setSelectedProfileId(p.id)}
                        className={`py-2.5 px-2 flex justify-between items-center rounded-lg cursor-pointer transition ${
                          selectedProfileId === p.id ? 'bg-amber-50/70 border border-amber-200' : 'hover:bg-slate-50'
                        }`}
                      >
                        <div>
                          <div className="text-xs font-semibold text-slate-800">{p.name}</div>
                          <div className="text-[11px] text-slate-500">
                            {p.date_of_birth} at {p.time_of_birth} • {p.city}
                          </div>
                        </div>
                        {selectedProfileId === p.id && (
                          <span className="text-[10px] font-semibold bg-amber-200/60 text-amber-900 px-2 py-0.5 rounded">
                            Active
                          </span>
                        )}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Quick Chart Preview */}
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
                  <div className="flex justify-between items-center mb-2">
                    <h4 className="font-cinzel text-sm font-bold text-vedic-navy">Active Chart Snapshot</h4>
                    <button
                      onClick={() => setActiveTab('parashara-sheet')}
                      className="text-xs text-amber-600 hover:underline font-medium"
                    >
                      Full Kundli Worksheet (D1–D60) →
                    </button>
                  </div>
                  {chartData ? (
                    <div className="flex items-center justify-around py-3">
                      <div className="w-48">
                        <NorthIndianChart houses={chartData.houses} planets={chartData.planets} />
                      </div>
                      <div className="text-xs space-y-1.5 text-slate-600 pl-4">
                        <div>
                          <span className="font-semibold text-slate-800">Lagna:</span>{' '}
                          {chartData.chart_summary.lagna_rashi} ({chartData.chart_summary.lagna_dms})
                        </div>
                        <div>
                          <span className="font-semibold text-slate-800">Lagna Lord:</span>{' '}
                          {chartData.chart_summary.lagna_lord}
                        </div>
                        <div>
                          <span className="font-semibold text-slate-800">Nakshatra:</span>{' '}
                          {chartData.chart_summary.lagna_nakshatra} Pada {chartData.chart_summary.lagna_pada}
                        </div>
                        <div>
                          <span className="font-semibold text-slate-800">Ayanamsa:</span>{' '}
                          {chartData.chart_summary.ayanamsa_value.toFixed(4)}°
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="text-center py-10 text-xs text-slate-400">Loading chart snapshot...</div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: BIRTH PROFILE MANAGEMENT */}
          {activeTab === 'profiles' && (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Form to enter profile */}
              <div className="lg:col-span-5 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <h3 className="font-cinzel text-base font-bold text-vedic-navy mb-3">
                  Add Research Birth Profile
                </h3>

                <form onSubmit={handleCreateProfile} className="space-y-4 text-xs">
                  {/* Name & Gender */}
                  <div className="grid grid-cols-3 gap-2">
                    <div className="col-span-2">
                      <label className="block text-slate-700 font-medium mb-1">Full Name</label>
                      <input
                        type="text"
                        required
                        value={newProfile.name}
                        onChange={(e) => setNewProfile({ ...newProfile, name: e.target.value })}
                        className="w-full px-3 py-1.5 border border-slate-300 rounded focus:ring-1 focus:ring-amber-400 focus:outline-none"
                      />
                    </div>
                    <div>
                      <label className="block text-slate-700 font-medium mb-1">Gender</label>
                      <select
                        value={newProfile.gender}
                        onChange={(e) => setNewProfile({ ...newProfile, gender: e.target.value })}
                        className="w-full px-2 py-1.5 border border-slate-300 rounded focus:ring-1 focus:ring-amber-400"
                      >
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                        <option value="Other">Other</option>
                      </select>
                    </div>
                  </div>

                  {/* Date of Birth */}
                  <div>
                    <label className="block text-slate-700 font-medium mb-1">Date of Birth</label>
                    <input
                      type="date"
                      required
                      value={newProfile.date_of_birth}
                      onChange={(e) => setNewProfile({ ...newProfile, date_of_birth: e.target.value })}
                      className="w-full px-3 py-1.5 border border-slate-300 rounded focus:ring-1 focus:ring-amber-400"
                    />
                  </div>

                  {/* EXACT TIME OF BIRTH: 12-Hour Selector with AM/PM */}
                  <div className="bg-amber-50/40 p-3 rounded-lg border border-amber-200/70">
                    <div className="flex justify-between items-center mb-1.5">
                      <label className="text-slate-800 font-semibold flex items-center space-x-1">
                        <Clock className="w-3.5 h-3.5 text-amber-600" />
                        <span>Exact Birth Time (AM / PM)</span>
                      </label>
                      <span className="font-mono text-[11px] font-bold text-vedic-navy bg-white px-2 py-0.5 rounded border border-amber-200">
                        {String(timeHour12).padStart(2, '0')}:{String(timeMinute).padStart(2, '0')}:{String(timeSecond).padStart(2, '0')} {timeAmPm}
                        <span className="text-slate-400 font-normal ml-1">({newProfile.time_of_birth})</span>
                      </span>
                    </div>

                    <div className="grid grid-cols-4 gap-2">
                      {/* Hour (1-12) */}
                      <div>
                        <span className="text-[10px] text-slate-500 font-medium block mb-0.5">Hour (1-12)</span>
                        <select
                          value={timeHour12}
                          onChange={(e) => setTimeHour12(parseInt(e.target.value, 10))}
                          className="w-full px-2 py-1.5 border border-slate-300 rounded font-mono font-bold text-slate-800 bg-white"
                        >
                          {Array.from({ length: 12 }, (_, i) => i + 1).map((h) => (
                            <option key={h} value={h}>
                              {String(h).padStart(2, '0')}
                            </option>
                          ))}
                        </select>
                      </div>

                      {/* Minute (0-59) */}
                      <div>
                        <span className="text-[10px] text-slate-500 font-medium block mb-0.5">Min (00-59)</span>
                        <select
                          value={timeMinute}
                          onChange={(e) => setTimeMinute(parseInt(e.target.value, 10))}
                          className="w-full px-2 py-1.5 border border-slate-300 rounded font-mono font-bold text-slate-800 bg-white"
                        >
                          {Array.from({ length: 60 }, (_, i) => i).map((m) => (
                            <option key={m} value={m}>
                              {String(m).padStart(2, '0')}
                            </option>
                          ))}
                        </select>
                      </div>

                      {/* Second (0-59) */}
                      <div>
                        <span className="text-[10px] text-slate-500 font-medium block mb-0.5">Sec (00-59)</span>
                        <select
                          value={timeSecond}
                          onChange={(e) => setTimeSecond(parseInt(e.target.value, 10))}
                          className="w-full px-2 py-1.5 border border-slate-300 rounded font-mono font-bold text-slate-800 bg-white"
                        >
                          {Array.from({ length: 60 }, (_, i) => i).map((s) => (
                            <option key={s} value={s}>
                              {String(s).padStart(2, '0')}
                            </option>
                          ))}
                        </select>
                      </div>

                      {/* AM / PM Toggle Buttons */}
                      <div>
                        <span className="text-[10px] text-slate-500 font-medium block mb-0.5">AM / PM</span>
                        <div className="grid grid-cols-2 gap-1">
                          <button
                            type="button"
                            onClick={() => setTimeAmPm('AM')}
                            className={`py-1.5 text-xs font-bold rounded transition ${
                              timeAmPm === 'AM'
                                ? 'bg-vedic-navy text-amber-300 shadow-sm'
                                : 'bg-white border border-slate-300 text-slate-600 hover:bg-slate-100'
                            }`}
                          >
                            AM
                          </button>
                          <button
                            type="button"
                            onClick={() => setTimeAmPm('PM')}
                            className={`py-1.5 text-xs font-bold rounded transition ${
                              timeAmPm === 'PM'
                                ? 'bg-vedic-navy text-amber-300 shadow-sm'
                                : 'bg-white border border-slate-300 text-slate-600 hover:bg-slate-100'
                            }`}
                          >
                            PM
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* PUBLIC LOCATION SEARCH & AUTOCOMPLETE */}
                  <div className="relative">
                    <label className="block text-slate-700 font-semibold mb-1 flex items-center justify-between">
                      <span className="flex items-center space-x-1">
                        <MapPin className="w-3.5 h-3.5 text-red-500" />
                        <span>Birthplace Location (Worldwide Autocomplete)</span>
                      </span>
                      {isSearchingLocation && (
                        <span className="text-[10px] text-amber-600 flex items-center space-x-1">
                          <RefreshCw className="w-3 h-3 animate-spin" />
                          <span>Searching places...</span>
                        </span>
                      )}
                    </label>

                    <div className="relative">
                      <input
                        type="text"
                        placeholder="Type any city, town, or place (e.g. Varanasi, London, New York)..."
                        value={locationQuery}
                        onChange={(e) => handleLocationInputChange(e.target.value)}
                        onFocus={() => locationResults.length > 0 && setShowLocationDropdown(true)}
                        className="w-full pl-8 pr-3 py-2 border border-slate-300 rounded focus:ring-1 focus:ring-amber-400 text-xs font-medium"
                      />
                      <Search className="w-4 h-4 text-slate-400 absolute left-2.5 top-2.5" />
                    </div>

                    {/* Quick Popular City Pills */}
                    <div className="mt-1.5 flex flex-wrap items-center gap-1 text-[10px]">
                      <span className="text-slate-400 font-medium">Quick Pick:</span>
                      {[
                        { name: 'Varanasi', query: 'Varanasi' },
                        { name: 'Ujjain', query: 'Ujjain' },
                        { name: 'Ayodhya', query: 'Ayodhya' },
                        { name: 'New Delhi', query: 'New Delhi' },
                        { name: 'Mumbai', query: 'Mumbai' },
                        { name: 'Bengaluru', query: 'Bengaluru' },
                        { name: 'Kolkata', query: 'Kolkata' },
                        { name: 'London', query: 'London' },
                        { name: 'New York', query: 'New York' },
                      ].map((c) => (
                        <button
                          key={c.name}
                          type="button"
                          onClick={() => handleLocationInputChange(c.query)}
                          className="px-2 py-0.5 rounded-full bg-slate-100 hover:bg-amber-100 text-slate-600 hover:text-amber-900 border border-slate-200 transition"
                        >
                          {c.name}
                        </button>
                      ))}
                    </div>

                    {/* Autocomplete Dropdown */}
                    {showLocationDropdown && locationResults.length > 0 && (
                      <div className="absolute z-30 left-0 right-0 mt-1 bg-white border border-slate-300 rounded-lg shadow-xl max-h-56 overflow-y-auto divide-y divide-slate-100">
                        {locationResults.map((loc, idx) => (
                          <div
                            key={idx}
                            onClick={() => handleSelectLocation(loc)}
                            className="p-2.5 hover:bg-amber-50 cursor-pointer text-xs transition"
                          >
                            <div className="flex justify-between items-start">
                              <span className="font-semibold text-slate-800">{loc.display_name}</span>
                              {loc.source && (
                                <span className="text-[9px] px-1.5 py-0.5 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded font-mono shrink-0 ml-2">
                                  {loc.source}
                                </span>
                              )}
                            </div>
                            <div className="text-[10px] text-slate-500 flex items-center space-x-2 mt-0.5">
                              <span className="font-mono">Lat: {loc.latitude}°, Lon: {loc.longitude}°</span>
                              <span>•</span>
                              <span className="text-amber-700 font-medium">{loc.timezone_str} (UTC {loc.timezone_offset >= 0 ? `+${loc.timezone_offset}` : loc.timezone_offset})</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Auto-filled Coordinate and Timezone Summary Card */}
                  <div className="bg-slate-50 p-2.5 rounded-lg border border-slate-200 text-xs space-y-1">
                    <div className="flex justify-between items-center">
                      <span className="text-slate-500 font-medium">Auto-Resolved Astronomical Coordinates:</span>
                      <button
                        type="button"
                        onClick={() => setShowManualCoords(!showManualCoords)}
                        className="text-[11px] text-amber-700 hover:underline font-semibold"
                      >
                        {showManualCoords ? 'Hide Manual Edit' : 'Edit Coordinates'}
                      </button>
                    </div>
                    <div className="text-slate-700 font-mono text-[11px] flex flex-wrap gap-x-3">
                      <span>Lat: <strong>{newProfile.latitude}°</strong></span>
                      <span>Lon: <strong>{newProfile.longitude}°</strong></span>
                      <span>TZ: <strong>{newProfile.timezone_str} ({newProfile.timezone_offset >= 0 ? `+${newProfile.timezone_offset}` : newProfile.timezone_offset}h)</strong></span>
                    </div>
                  </div>

                  {/* Manual coordinates expansion */}
                  {showManualCoords && (
                    <div className="p-3 bg-white border border-slate-200 rounded-lg space-y-2">
                      <div className="grid grid-cols-2 gap-2">
                        <div>
                          <label className="block text-[10px] text-slate-500 font-medium mb-0.5">Latitude (°)</label>
                          <input
                            type="number"
                            step="any"
                            value={newProfile.latitude}
                            onChange={(e) => setNewProfile({ ...newProfile, latitude: parseFloat(e.target.value) })}
                            className="w-full px-2 py-1 border border-slate-300 rounded font-mono"
                          />
                        </div>
                        <div>
                          <label className="block text-[10px] text-slate-500 font-medium mb-0.5">Longitude (°)</label>
                          <input
                            type="number"
                            step="any"
                            value={newProfile.longitude}
                            onChange={(e) => setNewProfile({ ...newProfile, longitude: parseFloat(e.target.value) })}
                            className="w-full px-2 py-1 border border-slate-300 rounded font-mono"
                          />
                        </div>
                      </div>
                      <div className="grid grid-cols-2 gap-2">
                        <div>
                          <label className="block text-[10px] text-slate-500 font-medium mb-0.5">Timezone IANA</label>
                          <input
                            type="text"
                            value={newProfile.timezone_str}
                            onChange={(e) => setNewProfile({ ...newProfile, timezone_str: e.target.value })}
                            className="w-full px-2 py-1 border border-slate-300 rounded font-mono"
                          />
                        </div>
                        <div>
                          <label className="block text-[10px] text-slate-500 font-medium mb-0.5">UTC Offset (hrs)</label>
                          <input
                            type="number"
                            step="0.5"
                            value={newProfile.timezone_offset}
                            onChange={(e) => setNewProfile({ ...newProfile, timezone_offset: parseFloat(e.target.value) })}
                            className="w-full px-2 py-1 border border-slate-300 rounded font-mono"
                          />
                        </div>
                      </div>
                    </div>
                  )}

                  <button
                    type="submit"
                    className="w-full mt-3 bg-vedic-navy text-white font-semibold py-2 rounded-lg hover:bg-slate-800 transition flex items-center justify-center space-x-1.5 shadow"
                  >
                    <Plus className="w-4 h-4 text-amber-400" />
                    <span>Save & Calculate Chart</span>
                  </button>
                </form>
              </div>

              {/* Profiles List */}
              <div className="lg:col-span-7 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <h3 className="font-cinzel text-base font-bold text-vedic-navy mb-4">
                  Saved Research Profiles ({profiles.length})
                </h3>
                <div className="overflow-x-auto">
                  <table className="w-full text-xs text-left">
                    <thead className="bg-slate-50 text-slate-500 uppercase font-mono text-[10px] border-b border-slate-200">
                      <tr>
                        <th className="py-2.5 px-3">Name</th>
                        <th className="py-2.5 px-3">Date & Time</th>
                        <th className="py-2.5 px-3">Birthplace</th>
                        <th className="py-2.5 px-3">Coordinates & TZ</th>
                        <th className="py-2.5 px-3 text-right">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {profiles.map((p) => (
                        <tr
                          key={p.id}
                          className={`hover:bg-slate-50/80 transition ${
                            selectedProfileId === p.id ? 'bg-amber-50/50' : ''
                          }`}
                        >
                          <td className="py-3 px-3 font-semibold text-slate-800">{p.name}</td>
                          <td className="py-3 px-3">
                            <div>{p.date_of_birth}</div>
                            <div className="text-[11px] text-amber-800 font-mono font-medium">{p.time_of_birth}</div>
                          </td>
                          <td className="py-3 px-3 text-slate-600 max-w-xs truncate" title={p.birthplace}>
                            {p.birthplace}
                          </td>
                          <td className="py-3 px-3 font-mono text-[11px] text-slate-500">
                            <div>{p.latitude.toFixed(4)}°, {p.longitude.toFixed(4)}°</div>
                            <div className="text-[10px] text-slate-400">{p.timezone_str} ({p.timezone_offset >= 0 ? `+${p.timezone_offset}` : p.timezone_offset}h)</div>
                          </td>
                          <td className="py-3 px-3 text-right space-x-2">
                            <button
                              onClick={() => {
                                setSelectedProfileId(p.id);
                                setActiveTab('parashara-sheet');
                              }}
                              className="text-amber-600 hover:text-amber-700 font-semibold text-[11px]"
                            >
                              Load Chart
                            </button>
                            <button
                              onClick={async () => {
                                if (confirm(`Delete profile for ${p.name}?`)) {
                                  await api.deleteProfile(p.id);
                                  setProfiles(profiles.filter((x) => x.id !== p.id));
                                }
                              }}
                              className="text-slate-400 hover:text-red-500"
                              title="Delete"
                            >
                              <Trash2 className="w-3.5 h-3.5 inline" />
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* TAB: KUNDLI WORKSHEET (D1-D60) */}
          {activeTab === 'parashara-sheet' && (
            <ParasharaLightWorksheet
              profile={currentProfile || null}
              chartData={chartData}
              vargaD9Data={vargaD9Data}
              dashaData={dashaData}
              panchangData={panchangData}
              activeAyanamsa={activeAyanamsa}
              activeNodeType={activeNodeType}
            />
          )}

          {/* TAB 4: PLANETARY POSITIONS */}
          {activeTab === 'planets' && chartData && (
            <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
              <div className="flex justify-between items-center mb-4">
                <div>
                  <h3 className="font-cinzel text-base font-bold text-vedic-navy">
                    Planetary Positions (Swiss Ephemeris Geocentric Sidereal)
                  </h3>
                  <p className="text-xs text-slate-500">
                    Ayanamsa: {chartData.chart_summary.ayanamsa_name} (
                    {chartData.chart_summary.ayanamsa_value.toFixed(4)}°) • Engine: {chartData.chart_summary.engine_name} {chartData.chart_summary.engine_version}
                  </p>
                </div>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-xs text-left">
                  <thead className="bg-slate-50 text-slate-500 uppercase font-mono text-[10px] border-b border-slate-200">
                    <tr>
                      <th className="py-2.5 px-3">Planet</th>
                      <th className="py-2.5 px-3">Rashi</th>
                      <th className="py-2.5 px-3">Degrees (DMS)</th>
                      <th className="py-2.5 px-3">Nakshatra (Pada)</th>
                      <th className="py-2.5 px-3">Nak Lord</th>
                      <th className="py-2.5 px-3">House</th>
                      <th className="py-2.5 px-3">Speed</th>
                      <th className="py-2.5 px-3">Motion</th>
                      <th className="py-2.5 px-3">Combustion</th>
                      <th className="py-2.5 px-3">Dignity</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {chartData.planets.map((p) => (
                      <tr key={p.name} className="hover:bg-slate-50 transition">
                        <td className="py-2.5 px-3 font-semibold text-slate-900">{p.name}</td>
                        <td className="py-2.5 px-3 font-medium text-slate-700">{p.rashi}</td>
                        <td className="py-2.5 px-3 font-mono text-slate-600">{p.dms}</td>
                        <td className="py-2.5 px-3">
                          {p.nakshatra} <span className="text-amber-700 font-semibold font-mono">P{p.pada}</span>
                        </td>
                        <td className="py-2.5 px-3 text-slate-600">{p.nakshatra_lord}</td>
                        <td className="py-2.5 px-3 font-bold text-vedic-navy font-mono">H{p.house}</td>
                        <td className="py-2.5 px-3 font-mono text-slate-500">{p.speed.toFixed(3)}°/day</td>
                        <td className="py-2.5 px-3">
                          {p.is_retrograde ? (
                            <span className="text-[10px] font-bold text-red-600 bg-red-50 px-1.5 py-0.5 rounded border border-red-200">
                              Retrograde (R)
                            </span>
                          ) : (
                            <span className="text-[10px] text-slate-500">Direct</span>
                          )}
                        </td>
                        <td className="py-2.5 px-3">
                          {p.is_combust ? (
                            <span className="text-[10px] font-bold text-orange-600 bg-orange-50 px-1.5 py-0.5 rounded border border-orange-200">
                              Combust
                            </span>
                          ) : (
                            <span className="text-[10px] text-slate-400">-</span>
                          )}
                        </td>
                        <td className="py-2.5 px-3">
                          <span
                            className={`text-[10px] font-semibold px-2 py-0.5 rounded ${
                              p.dignity === 'Exalted'
                                ? 'bg-emerald-100 text-emerald-800'
                                : p.dignity === 'Debilitated'
                                ? 'bg-red-100 text-red-800'
                                : p.dignity === 'Own Sign'
                                ? 'bg-amber-100 text-amber-800'
                                : 'bg-slate-100 text-slate-600'
                            }`}
                          >
                            {p.dignity}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* TAB 5: HOUSE ANALYSIS */}
          {activeTab === 'houses' && chartData && (
            <div className="space-y-4">
              <h3 className="font-cinzel text-base font-bold text-vedic-navy">
                12 Bhavas (House Analysis & Lords)
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {chartData.houses.map((h) => (
                  <div key={h.house_number} className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm space-y-2">
                    <div className="flex justify-between items-center border-b border-slate-100 pb-2">
                      <span className="font-cinzel font-bold text-amber-600 text-sm">
                        House {h.house_number}
                      </span>
                      <span className="text-[11px] font-semibold text-slate-600 bg-slate-50 px-2 py-0.5 rounded">
                        {h.sign} ({h.sign_lord})
                      </span>
                    </div>
                    <div className="text-xs space-y-1">
                      <div className="text-slate-500">
                        Occupants:{' '}
                        <strong className="text-slate-800">
                          {h.occupants.length ? h.occupants.join(', ') : 'Empty'}
                        </strong>
                      </div>
                      <div className="text-slate-500">
                        Aspects:{' '}
                        <span className="text-slate-700">
                          {h.aspecting_planets.length ? h.aspecting_planets.join(', ') : 'None'}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 6: DIVISIONAL CHARTS */}
          {activeTab === 'divisional' && (
            <div className="space-y-6">
              <div className="flex flex-wrap items-center justify-between gap-3 bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div>
                  <h3 className="font-cinzel text-base font-bold text-vedic-navy">
                    Parashari Divisional Charts (Vargas)
                  </h3>
                  <p className="text-xs text-slate-500">
                    Explore harmonic sub-divisions from D1 to D60 calculated with classical rules.
                  </p>
                </div>
                <div className="flex flex-wrap gap-1">
                  {[
                    'D1', 'D2', 'D3', 'D4', 'D7', 'D9', 'D10', 'D12',
                    'D16', 'D20', 'D24', 'D27', 'D30', 'D40', 'D45', 'D60'
                  ].map((v) => (
                    <button
                      key={v}
                      onClick={() => handleVargaChange(v)}
                      className={`px-2.5 py-1 text-xs font-semibold rounded border transition ${
                        selectedVarga === v
                          ? 'bg-vedic-navy text-amber-300 border-vedic-navy'
                          : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'
                      }`}
                    >
                      {v}
                    </button>
                  ))}
                </div>
              </div>

              {vargaData && (
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4">
                  <div className="flex justify-between items-center border-b border-slate-100 pb-3">
                    <div>
                      <h4 className="font-cinzel text-lg font-bold text-vedic-navy">
                        {vargaData.varga_key} – {vargaData.varga_name} Chart
                      </h4>
                      <p className="text-xs text-slate-500">{vargaData.description}</p>
                    </div>
                    <span className="text-xs font-semibold bg-amber-100 text-amber-800 px-3 py-1 rounded-full">
                      Lagna: {vargaData.lagna_rashi}
                    </span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Planetary table in Varga */}
                    <table className="w-full text-xs text-left">
                      <thead className="bg-slate-50 text-slate-500 uppercase font-mono text-[10px]">
                        <tr>
                          <th className="py-2 px-3">Planet</th>
                          <th className="py-2 px-3">Varga Rashi</th>
                          <th className="py-2 px-3">Rashi Lord</th>
                          <th className="py-2 px-3">House from Varga Lagna</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-100">
                        {vargaData.planets.map((p: any) => (
                          <tr key={p.name}>
                            <td className="py-2 px-3 font-semibold text-slate-800">{p.name}</td>
                            <td className="py-2 px-3 text-slate-700">{p.sign}</td>
                            <td className="py-2 px-3 text-slate-500">{p.sign_lord}</td>
                            <td className="py-2 px-3 font-bold text-vedic-navy font-mono">H{p.house}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>

                    {/* Varga House summary */}
                    <div className="bg-slate-50 p-4 rounded-lg border border-slate-200 text-xs space-y-2">
                      <h5 className="font-semibold text-slate-700 mb-2 font-cinzel">Houses in {vargaData.varga_key}</h5>
                      <div className="grid grid-cols-2 gap-2">
                        {Object.entries(vargaData.houses).map(([h, occ]: any) => (
                          <div key={h} className="p-1.5 bg-white rounded border border-slate-200">
                            <span className="font-bold text-amber-700">H{h}: </span>
                            <span className="text-slate-600">{occ.length ? occ.join(', ') : 'Empty'}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* TAB 8: VIMSHOTTARI DASHA */}
          {activeTab === 'dasha' && dashaData && (
            <div className="space-y-6">
              {/* AUTHENTIC PARASHARA'S LIGHT DASHA AT BIRTH CARD */}
              <ParasharaDashaCard dashaData={dashaData} />

              <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center">
                <div>
                  <h3 className="font-cinzel text-base font-bold text-vedic-navy">
                    Vimshottari Dasha Progression (120-Year Cycle)
                  </h3>
                  <p className="text-xs text-slate-500 mt-1">
                    Birth Star: <strong>{dashaData.birth_nakshatra}</strong> • Starting Balance:{' '}
                    <strong>{dashaData.balance_years} years</strong> of{' '}
                    <strong>{dashaData.starting_mahadasha_lord}</strong> Mahadasha.
                  </p>
                </div>
                <div className="mt-3 md:mt-0 flex items-center space-x-2 bg-amber-50 border border-amber-200 px-3 py-1.5 rounded-lg text-xs">
                  <span className="text-amber-800 font-medium">Running Period:</span>
                  <span className="font-bold text-vedic-navy">
                    {dashaData.current_mahadasha} - {dashaData.current_antardasha} - {dashaData.current_pratyantardasha}
                  </span>
                </div>
              </div>

              {/* Dasha Timeline List */}
              <div className="space-y-3">
                {dashaData.dashas.map((md) => (
                  <div
                    key={md.planet}
                    className={`bg-white rounded-xl border p-4 shadow-sm transition ${
                      md.is_current ? 'border-amber-400 bg-amber-50/20 ring-1 ring-amber-400' : 'border-slate-200'
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <div className="flex items-center space-x-3">
                        <span className="w-8 h-8 rounded-full bg-vedic-navy text-amber-300 font-bold font-cinzel flex items-center justify-center text-xs">
                          {md.planet.substring(0, 2)}
                        </span>
                        <div>
                          <h4 className="text-sm font-bold text-slate-900">{md.planet} Mahadasha</h4>
                          <span className="text-xs text-slate-500 font-mono">
                            {md.start_date} to {md.end_date} ({md.duration_years} yrs)
                          </span>
                        </div>
                      </div>
                      {md.is_current && (
                        <span className="px-2.5 py-1 bg-amber-400 text-vedic-navy text-xs font-bold rounded-full">
                          Current Running Dasha
                        </span>
                      )}
                    </div>

                    {/* Antardasha accordion preview */}
                    {md.sub_periods && (
                      <div className="mt-3 pt-3 border-t border-slate-100 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 lg:grid-cols-9 gap-2">
                        {md.sub_periods.map((ad) => (
                          <div
                            key={ad.planet}
                            className={`p-2 rounded text-center text-xs border ${
                              ad.is_current
                                ? 'bg-amber-100 border-amber-300 font-bold text-vedic-navy'
                                : 'bg-slate-50 border-slate-100 text-slate-600'
                            }`}
                          >
                            <div className="font-semibold">{ad.planet}</div>
                            <div className="text-[10px] text-slate-400 font-mono mt-0.5">
                              {ad.start_date.substring(0, 7)}
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 9: PANCHANG */}
          {activeTab === 'panchang' && panchangData && (
            <div className="space-y-6">
              <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <h3 className="font-cinzel text-base font-bold text-vedic-navy mb-1">
                  Daily Panchang ({panchangData.date})
                </h3>
                <p className="text-xs text-slate-500">
                  Calculated from exact astronomical longitudes and Swiss Ephemeris sunrise algorithms.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm space-y-1">
                  <span className="text-xs text-slate-500 font-medium">Tithi (Lunar Day)</span>
                  <div className="text-base font-bold text-vedic-navy">{panchangData.tithi}</div>
                  <div className="text-xs text-slate-400">
                    Paksha: {panchangData.paksha} • Progress: {panchangData.tithi_progress_pct}%
                  </div>
                </div>

                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm space-y-1">
                  <span className="text-xs text-slate-500 font-medium">Vara (Weekday)</span>
                  <div className="text-base font-bold text-vedic-navy">{panchangData.vara}</div>
                  <div className="text-xs text-slate-400">Solar day reckoned from local sunrise</div>
                </div>

                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm space-y-1">
                  <span className="text-xs text-slate-500 font-medium">Moon Nakshatra</span>
                  <div className="text-base font-bold text-vedic-navy">{panchangData.nakshatra}</div>
                  <div className="text-xs text-slate-400">Nakshatra #{panchangData.nakshatra_number}</div>
                </div>

                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm space-y-1">
                  <span className="text-xs text-slate-500 font-medium">Yoga</span>
                  <div className="text-base font-bold text-vedic-navy">{panchangData.yoga}</div>
                  <div className="text-xs text-slate-400">Yoga #{panchangData.yoga_number} of 27</div>
                </div>

                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm space-y-1">
                  <span className="text-xs text-slate-500 font-medium">Karana (Half-Tithi)</span>
                  <div className="text-base font-bold text-vedic-navy">{panchangData.karana}</div>
                  <div className="text-xs text-slate-400">Lunar action disposition</div>
                </div>

                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm space-y-1">
                  <span className="text-xs text-slate-500 font-medium">Solar Transitions</span>
                  <div className="text-sm font-semibold text-slate-700">
                    Sunrise: <span className="text-amber-700 font-mono font-bold">{panchangData.sunrise}</span>
                  </div>
                  <div className="text-sm font-semibold text-slate-700">
                    Sunset: <span className="text-indigo-700 font-mono font-bold">{panchangData.sunset}</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 11: DOSHA ANALYSIS */}
          {activeTab === 'doshas' && (
            <div className="space-y-4">
              <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <h3 className="font-cinzel text-base font-bold text-vedic-navy">
                  Dosha & Affliction Evaluation
                </h3>
                <p className="text-xs text-slate-500 mt-1">
                  Rigorous, non-fear-based verification of Manglik, Kala Sarpa, Pitru Dosha, and classical cancellations.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {doshasData.map((d) => (
                  <div
                    key={d.name}
                    className={`bg-white p-5 rounded-xl border shadow-sm space-y-3 ${
                      d.is_present && !d.is_cancelled ? 'border-orange-200' : 'border-slate-200'
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <h4 className="font-cinzel text-sm font-bold text-vedic-navy">{d.name}</h4>
                      <span
                        className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                          d.severity === 'None'
                            ? 'bg-emerald-100 text-emerald-800'
                            : d.is_cancelled
                            ? 'bg-blue-100 text-blue-800'
                            : 'bg-orange-100 text-orange-800'
                        }`}
                      >
                        {d.severity}
                      </span>
                    </div>
                    <div className="text-xs text-slate-600 font-mono bg-slate-50 p-2 rounded border border-slate-100">
                      Rule: {d.rule_applied}
                    </div>
                    <p className="text-xs text-slate-600 leading-relaxed">{d.explanation}</p>
                    {d.cancellation_factors.length > 0 && (
                      <div className="text-xs text-emerald-700 bg-emerald-50 p-2 rounded border border-emerald-100">
                        <strong>Cancellations:</strong> {d.cancellation_factors.join(' ')}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 12: KUNDLI MATCHING */}
          {activeTab === 'matching' && (
            <div className="space-y-6">
              <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <h3 className="font-cinzel text-base font-bold text-vedic-navy mb-4">
                  Ashtakoota 36-Point Compatibility Matching
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
                  <div>
                    <label className="block text-xs font-semibold text-slate-600 mb-1">Select Boy's Profile</label>
                    <select
                      value={boyProfileId || ''}
                      onChange={(e) => setBoyProfileId(Number(e.target.value))}
                      className="w-full text-xs p-2 border border-slate-300 rounded focus:ring-1 focus:ring-amber-400"
                    >
                      {profiles.map((p) => (
                        <option key={p.id} value={p.id}>
                          {p.name} ({p.date_of_birth})
                        </option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-600 mb-1">Select Girl's Profile</label>
                    <select
                      value={girlProfileId || ''}
                      onChange={(e) => setGirlProfileId(Number(e.target.value))}
                      className="w-full text-xs p-2 border border-slate-300 rounded focus:ring-1 focus:ring-amber-400"
                    >
                      {profiles.map((p) => (
                        <option key={p.id} value={p.id}>
                          {p.name} ({p.date_of_birth})
                        </option>
                      ))}
                    </select>
                  </div>
                  <button
                    onClick={handleRunMatching}
                    className="w-full bg-vedic-navy text-white text-xs font-semibold py-2.5 rounded hover:bg-slate-800 transition"
                  >
                    Calculate Ashtakoota Match
                  </button>
                </div>
              </div>

              {matchingResult && (
                <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-6">
                  {/* Score summary banner */}
                  <div className="text-center p-4 bg-amber-50 border border-amber-200 rounded-xl">
                    <span className="text-xs uppercase font-mono tracking-widest text-amber-800">
                      Ashtakoota Score
                    </span>
                    <div className="text-4xl font-cinzel font-bold text-vedic-navy mt-1">
                      {matchingResult.total_score} <span className="text-xl text-slate-400">/ 36</span>
                    </div>
                    <div className="text-sm font-semibold text-amber-700 mt-1">
                      {matchingResult.recommendation}
                    </div>
                    <p className="text-xs text-slate-600 mt-2 max-w-xl mx-auto">
                      {matchingResult.matching_summary}
                    </p>
                  </div>

                  {/* 8 Kootas Table */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    {[
                      { name: 'Varna', score: matchingResult.varna.score, max: 1 },
                      { name: 'Vashya', score: matchingResult.vashya.score, max: 2 },
                      { name: 'Tara', score: matchingResult.tara.score, max: 3 },
                      { name: 'Yoni', score: matchingResult.yoni.score, max: 4 },
                      { name: 'Graha Maitri', score: matchingResult.graha_maitri.score, max: 5 },
                      { name: 'Gana', score: matchingResult.gana.score, max: 6 },
                      { name: 'Bhakoot', score: matchingResult.bhakoot.score, max: 7 },
                      { name: 'Nadi', score: matchingResult.nadi.score, max: 8 },
                    ].map((k) => (
                      <div key={k.name} className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-center">
                        <span className="text-xs text-slate-500 font-medium">{k.name}</span>
                        <div className="text-lg font-bold text-slate-800 mt-0.5">
                          {k.score} <span className="text-xs font-normal text-slate-400">/ {k.max}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* TAB 13: TRANSIT ANALYSIS */}
          {activeTab === 'transits' && transitsData && (
            <div className="space-y-6">
              <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex justify-between items-center">
                <div>
                  <h3 className="font-cinzel text-base font-bold text-vedic-navy">
                    Gochara (Real-Time Planetary Transits)
                  </h3>
                  <p className="text-xs text-slate-500">
                    Transit Date: {transitsData.transit_date} • Engine: Swiss Ephemeris {transitsData.engine_version}
                  </p>
                </div>
                <div className="text-xs font-semibold px-3 py-1 bg-amber-100 text-amber-800 rounded">
                  {transitsData.sade_sati_status}
                </div>
              </div>

              <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <table className="w-full text-xs text-left">
                  <thead className="bg-slate-50 text-slate-500 uppercase font-mono text-[10px] border-b">
                    <tr>
                      <th className="py-2.5 px-3">Planet</th>
                      <th className="py-2.5 px-3">Transit Sign</th>
                      <th className="py-2.5 px-3">Degrees (DMS)</th>
                      <th className="py-2.5 px-3">Nakshatra</th>
                      <th className="py-2.5 px-3">Motion</th>
                      <th className="py-2.5 px-3">From Lagna</th>
                      <th className="py-2.5 px-3">From Moon</th>
                      <th className="py-2.5 px-3">Gochara Influence</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {transitsData.transits.map((t: any) => (
                      <tr key={t.planet} className="hover:bg-slate-50">
                        <td className="py-2 px-3 font-semibold text-slate-800">{t.planet}</td>
                        <td className="py-2 px-3 font-medium text-slate-700">{t.rashi}</td>
                        <td className="py-2 px-3 font-mono text-slate-500">{t.dms}</td>
                        <td className="py-2 px-3 text-slate-600">{t.nakshatra} (P{t.pada})</td>
                        <td className="py-2 px-3">
                          {t.is_retrograde ? (
                            <span className="text-[10px] text-red-600 font-bold">Retrograde</span>
                          ) : (
                            <span className="text-[10px] text-slate-500">Direct</span>
                          )}
                        </td>
                        <td className="py-2 px-3 font-bold text-slate-700 font-mono">H{t.house_from_lagna}</td>
                        <td className="py-2 px-3 font-bold text-amber-700 font-mono">H{t.house_from_moon}</td>
                        <td className="py-2 px-3">
                          <span
                            className={`text-[10px] font-semibold px-2 py-0.5 rounded ${
                              t.is_favorable_gochara ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-600'
                            }`}
                          >
                            {t.is_favorable_gochara ? 'Favorable' : 'Transformative'}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* TAB 14: AI ASTROLOGY CHAT */}
          {activeTab === 'ai-chat' && (
            <div className="flex flex-col h-[calc(100vh-8.5rem)] bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
              {/* Chat Header */}
              <div className="p-4 border-b border-slate-200 flex justify-between items-center bg-slate-50">
                <div className="flex items-center space-x-2">
                  <Bot className="w-5 h-5 text-amber-600" />
                  <div>
                    <h3 className="font-cinzel text-sm font-bold text-vedic-navy">
                      AstroRize Vedic AI Astrologer
                    </h3>
                    <p className="text-[11px] text-slate-500">
                      Grounded in calculated chart data for: <strong>{currentProfile?.name}</strong>
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => setChatMessages([])}
                  className="text-xs text-slate-500 hover:text-slate-800 hover:underline"
                >
                  Clear Chat
                </button>
              </div>

              {/* Chat Message Scroll */}
              <div className="flex-1 overflow-y-auto p-4 space-y-3">
                {chatMessages.length === 0 && (
                  <div className="text-center py-10 space-y-3">
                    <Bot className="w-10 h-10 text-amber-500 mx-auto opacity-70" />
                    <h4 className="font-cinzel text-sm font-bold text-slate-700">
                      Welcome to AstroRize Grounded AI Chat
                    </h4>
                    <p className="text-xs text-slate-500 max-w-md mx-auto">
                      Ask questions about Lagna, planetary positions, Vimshottari dasha periods, Yogas, and Doshas.
                      All responses are directly grounded in your verified Swiss Ephemeris birth chart.
                    </p>
                    <div className="flex flex-wrap justify-center gap-2 max-w-lg mx-auto pt-2">
                      {[
                        'Explain my Lagna and 1st house',
                        'Tell me about my Moon Nakshatra',
                        'Explain my current Mahadasha',
                        'Which Yogas are present in my chart?',
                        'Analyze my 10th house career prospects',
                      ].map((prompt) => (
                        <button
                          key={prompt}
                          onClick={() => setChatInput(prompt)}
                          className="text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 px-3 py-1.5 rounded-full border border-slate-200 transition"
                        >
                          "{prompt}"
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {chatMessages.map((m, idx) => (
                  <div
                    key={idx}
                    className={`flex flex-col ${m.role === 'user' ? 'items-end' : 'items-start'}`}
                  >
                    <div
                      className={`max-w-2xl p-3.5 rounded-xl text-xs leading-relaxed whitespace-pre-wrap ${
                        m.role === 'user'
                          ? 'bg-vedic-navy text-white rounded-br-none'
                          : 'bg-slate-100 text-slate-800 rounded-bl-none border border-slate-200'
                      }`}
                    >
                      {m.content}
                    </div>
                    {m.source && (
                      <span className="text-[10px] text-slate-400 mt-1 px-1 font-mono">
                        Source: {m.source}
                      </span>
                    )}
                  </div>
                ))}

                {chatLoading && (
                  <div className="flex items-center space-x-2 text-xs text-slate-400 italic">
                    <RefreshCw className="w-3.5 h-3.5 animate-spin text-amber-500" />
                    <span>Synthesizing Vedic chart placements...</span>
                  </div>
                )}
              </div>

              {/* Chat Input Bar */}
              <div className="p-3 border-t border-slate-200 bg-slate-50 flex items-center space-x-2">
                <input
                  type="text"
                  placeholder="Ask a question about your birth chart..."
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSendChat()}
                  className="flex-1 bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs text-slate-800 focus:outline-none focus:ring-1 focus:ring-amber-400"
                />
                <button
                  onClick={handleSendChat}
                  disabled={chatLoading || !chatInput.trim()}
                  className="bg-vedic-navy text-white px-4 py-2 rounded-lg hover:bg-slate-800 transition disabled:opacity-50 text-xs font-semibold flex items-center space-x-1"
                >
                  <Send className="w-3.5 h-3.5 text-amber-400" />
                  <span>Send</span>
                </button>
              </div>
            </div>
          )}

          {/* TAB 15: CALCULATION VERIFICATION & QA */}
          {activeTab === 'verification' && (
            <div className="space-y-6">
              <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center">
                <div>
                  <h3 className="font-cinzel text-base font-bold text-vedic-navy">
                    Automated Calculation Verification & QA Protocol
                  </h3>
                  <p className="text-xs text-slate-500 mt-1">
                    Every case strictly verifies calculated Swiss Ephemeris longitudes against independently established benchmark values.
                  </p>
                </div>
                <button
                  onClick={handleRunAllVerification}
                  disabled={verificationLoading}
                  className="mt-3 md:mt-0 px-4 py-2 bg-emerald-600 text-white text-xs font-semibold rounded-lg hover:bg-emerald-700 transition shadow flex items-center space-x-1.5"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${verificationLoading ? 'animate-spin' : ''}`} />
                  <span>Run All Verification Benchmarks</span>
                </button>
              </div>

              <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm overflow-x-auto">
                <table className="w-full text-xs text-left">
                  <thead className="bg-slate-50 text-slate-500 uppercase font-mono text-[10px] border-b">
                    <tr>
                      <th className="py-2.5 px-3">Test Case</th>
                      <th className="py-2.5 px-3">Reference Source</th>
                      <th className="py-2.5 px-3">Target Profile</th>
                      <th className="py-2.5 px-3">Tolerance</th>
                      <th className="py-2.5 px-3">Actual vs Expected</th>
                      <th className="py-2.5 px-3">Max Dev</th>
                      <th className="py-2.5 px-3">Status</th>
                      <th className="py-2.5 px-3 text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {verificationCases.map((vc) => {
                      const maxDiff = vc.differences
                        ? Math.max(...Object.values(vc.differences as Record<string, number>))
                        : 0.0;
                      return (
                        <tr key={vc.id} className="hover:bg-slate-50">
                          <td className="py-3 px-3 font-semibold text-slate-900">{vc.test_name}</td>
                          <td className="py-3 px-3 text-slate-600">{vc.reference_source}</td>
                          <td className="py-3 px-3 text-slate-500">{vc.profile_details?.name}</td>
                          <td className="py-3 px-3 font-mono text-slate-600">±{vc.tolerance}°</td>
                          <td className="py-3 px-3 text-[11px] font-mono text-slate-500">
                            {vc.actual_values ? Object.keys(vc.actual_values).length : 0} points verified
                          </td>
                          <td className="py-3 px-3 font-mono text-[11px]">
                            {vc.differences ? `${maxDiff.toFixed(4)}°` : '-'}
                          </td>
                          <td className="py-3 px-3">
                            <span
                              className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                                vc.status === 'PASSED'
                                  ? 'bg-emerald-100 text-emerald-800'
                                  : vc.status === 'FAILED'
                                  ? 'bg-red-100 text-red-800'
                                  : 'bg-slate-100 text-slate-600'
                              }`}
                            >
                              {vc.status}
                            </span>
                          </td>
                          <td className="py-3 px-3 text-right">
                            <button
                              onClick={async () => {
                                await api.runVerificationCase(vc.id);
                                const updated = await api.getVerificationCases();
                                setVerificationCases(updated);
                              }}
                              className="text-amber-600 hover:underline font-semibold"
                            >
                              Run Test
                            </button>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* TAB 16: TEST HISTORY */}
          {activeTab === 'test-history' && (
            <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4">
              <h3 className="font-cinzel text-base font-bold text-vedic-navy">
                Regression & Verification Test History
              </h3>
              <p className="text-xs text-slate-500">
                Persistent verification log stored locally in SQLite database.
              </p>
              <div className="space-y-3">
                {verificationCases.map((vc) => (
                  <div key={vc.id} className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs">
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-slate-800">{vc.test_name}</span>
                      <span
                        className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                          vc.status === 'PASSED' ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-200 text-slate-600'
                        }`}
                      >
                        {vc.status}
                      </span>
                    </div>
                    <div className="text-slate-500 mt-1">
                      Source: {vc.reference_source} • Executed:{' '}
                      {vc.executed_at ? new Date(vc.executed_at).toLocaleString() : 'Not yet executed'}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 17: ENGINE SETTINGS */}
          {activeTab === 'settings' && (
            <div className="max-w-2xl bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-5">
              <h3 className="font-cinzel text-base font-bold text-vedic-navy">
                Astronomical & Vedic Engine Configuration
              </h3>
              <div className="space-y-4 text-xs">
                <div>
                  <label className="block text-slate-700 font-semibold mb-1">Calculation Engine</label>
                  <input
                    type="text"
                    disabled
                    value="Swiss Ephemeris (C library + Python binding pyswisseph 2.10.3)"
                    className="w-full p-2 bg-slate-100 border border-slate-300 rounded font-mono text-slate-600"
                  />
                </div>
                <div>
                  <label className="block text-slate-700 font-semibold mb-1">Ayanamsa</label>
                  <select
                    value={activeAyanamsa}
                    onChange={(e) => setActiveAyanamsa(e.target.value)}
                    className="w-full p-2 border border-slate-300 rounded"
                  >
                    <option value="LAHIRI">Lahiri / Chitrapaksha (Standard Parashari)</option>
                    <option value="RAMAN">BV Raman Ayanamsa</option>
                    <option value="KP">Krishnamurti (KP)</option>
                    <option value="TRUE_CITRA">True Chitra Ayanamsa</option>
                    <option value="FAGAN_BRADLEY">Fagan-Bradley</option>
                    <option value="YUKTESHWAR">Sri Yukteshwar</option>
                  </select>
                </div>
                <div>
                  <label className="block text-slate-700 font-semibold mb-1">Lunar Node Mode</label>
                  <select
                    value={activeNodeType}
                    onChange={(e) => setActiveNodeType(e.target.value)}
                    className="w-full p-2 border border-slate-300 rounded"
                  >
                    <option value="TRUE_NODE">True Node (Astronomical Topocentric Oscillation)</option>
                    <option value="MEAN_NODE">Mean Node (Averaged Circular Orbit)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-slate-700 font-semibold mb-1">House System</label>
                  <input
                    type="text"
                    disabled
                    value="Whole Sign System (Parashari Rashi Bhava)"
                    className="w-full p-2 bg-slate-100 border border-slate-300 rounded font-mono text-slate-600"
                  />
                </div>
                <div className="pt-2 border-t border-slate-200">
                  <div className="text-slate-500 text-[11px]">
                    All calculations execute strictly on your local machine using compiled Swiss Ephemeris binaries.
                  </div>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
