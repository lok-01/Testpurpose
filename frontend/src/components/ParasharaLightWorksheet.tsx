import React, { useState, useEffect } from 'react';
import { BirthChartData, DashaData, PanchangData, BirthProfile, HouseCusp, PlanetPosition } from '../types';
import { NorthIndianChart } from '../charts/NorthIndianChart';
import { SouthIndianChart } from '../charts/SouthIndianChart';
import { api } from '../services/api';
import { Printer, RefreshCw } from 'lucide-react';

interface ParasharaWorksheetProps {
  profile: BirthProfile | null;
  chartData: BirthChartData | null;
  vargaD9Data: any | null;
  dashaData: DashaData | null;
  panchangData: PanchangData | null;
  activeAyanamsa: string;
  activeNodeType?: string;
}

const ALL_VARGAS = [
  'D1', 'D2', 'D3', 'D4', 'D7', 'D9', 'D10', 'D12',
  'D16', 'D20', 'D24', 'D27', 'D30', 'D40', 'D45', 'D60'
];

export const ParasharaLightWorksheet: React.FC<ParasharaWorksheetProps> = ({
  profile,
  chartData,
  dashaData,
  activeAyanamsa,
  activeNodeType = 'TRUE_NODE',
}) => {
  const [selectedVarga, setSelectedVarga] = useState<string>('D1');
  const [chartType, setChartType] = useState<'north' | 'south'>('north');
  const [vargaFull, setVargaFull] = useState<any>(null);
  const [loadingVarga, setLoadingVarga] = useState<boolean>(false);

  // Sub-tabs matching the reference UI
  const [vargaDetailTab, setVargaDetailTab] = useState<'Placements' | 'Lagna' | 'Friendship' | 'Aspects'>('Placements');
  const [upagrahaTab, setUpagrahaTab] = useState<'Upagraha' | 'Sphuta' | 'Varnada' | 'Tithi'>('Upagraha');
  const [strengthMainTab, setStrengthMainTab] = useState<'Vimshopaka' | 'Shadbala' | 'Ashtakavarga' | 'Dasha'>('Vimshopaka');
  const [vimshopakaSubTab, setVimshopakaSubTab] = useState<'Shad' | 'Sapta' | 'Dasha' | 'Shodasha'>('Shad');

  useEffect(() => {
    if (!profile) return;
    let cancelled = false;
    setLoadingVarga(true);
    api
      .getFullVargaWorksheet(profile.id, selectedVarga, activeAyanamsa, activeNodeType)
      .then((res) => {
        if (!cancelled) setVargaFull(res);
      })
      .catch((err) => console.error('Failed to load varga details:', err))
      .finally(() => {
        if (!cancelled) setLoadingVarga(false);
      });
    return () => {
      cancelled = true;
    };
  }, [profile?.id, selectedVarga, activeAyanamsa, activeNodeType]);

  if (!profile || !chartData) {
    return (
      <div className="bg-[#FAF8F2] p-12 text-center rounded-lg border border-[#D8D0C0]">
        <p className="text-sm text-stone-600">Please select or calculate a birth profile to view the Kundli Worksheet.</p>
      </div>
    );
  }

  // Build HouseCusp[] and PlanetPosition[] for NorthIndianChart / SouthIndianChart from selected Varga
  const buildVargaChartProps = (): { houses: HouseCusp[]; planets: PlanetPosition[]; lagnaNum: number } => {
    if (!vargaFull) {
      return {
        houses: chartData.houses,
        planets: chartData.planets,
        lagnaNum: chartData.chart_summary.lagna_rashi_number,
      };
    }

    const lagnaNum = vargaFull.lagna_rashi_number;
    const signs = [
      'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
      'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces',
    ];
    const lords = [
      'Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury',
      'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter',
    ];

    const houses: HouseCusp[] = Array.from({ length: 12 }, (_, idx) => {
      const hNum = idx + 1;
      const signNum = ((lagnaNum - 1 + idx) % 12) + 1;
      return {
        house_number: hNum,
        sign: signs[signNum - 1],
        sign_number: signNum,
        sign_lord: lords[signNum - 1],
        start_degree: (signNum - 1) * 30,
        cusp_degree: (signNum - 1) * 30 + 15,
        occupants: vargaFull.houses[String(hNum)] || vargaFull.houses[hNum] || [],
        aspecting_planets: [],
      };
    });

    const planets: PlanetPosition[] = (vargaFull.placements || []).map((pl: any, i: number) => ({
      name: pl.body,
      id: i,
      tropical_longitude: 0,
      sidereal_longitude: 0,
      latitude: 0,
      speed: 0,
      is_retrograde: pl.is_retrograde,
      rashi: pl.sign,
      rashi_number: pl.sign_number,
      rashi_lord: lords[pl.sign_number - 1],
      degree_in_rashi: 0,
      dms: pl.deg,
      parashara_dms: pl.deg,
      nakshatra: pl.nakshatra,
      nakshatra_number: 1,
      pada: 1,
      nakshatra_lord: '',
      house: pl.house,
      is_combust: pl.is_combust,
      dignity: pl.dignity,
    }));

    return { houses, planets, lagnaNum };
  };

  const { houses: chartHouses, planets: chartPlanets, lagnaNum } = buildVargaChartProps();
  const vimshopakaRows = vargaFull?.vimshopaka?.[vimshopakaSubTab] || [];

  // Compute Sphuta points from Sun, Moon, Lagna
  const sunLon = chartData.planets.find((p) => p.name === 'Sun')?.sidereal_longitude || 0;
  const moonLon = chartData.planets.find((p) => p.name === 'Moon')?.sidereal_longitude || 0;
  const lagnaLon = chartData.chart_summary.lagna_longitude || 0;
  const formatLonSign = (lon: number) => {
    const norm = ((lon % 360) + 360) % 360;
    const sIdx = Math.floor(norm / 30);
    const deg = norm % 30;
    const d = Math.floor(deg);
    const mF = (deg - d) * 60;
    const m = Math.floor(mF);
    const s = Math.round((mF - m) * 60);
    const signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
    const house = ((sIdx + 1 - chartData.chart_summary.lagna_rashi_number + 12) % 12) + 1;
    return {
      sign: signs[sIdx],
      dms: `${d}° ${String(m).padStart(2, '0')}' ${String(s).padStart(2, '0')}"`,
      house,
    };
  };

  const sphutaList = [
    { body: 'Trisputa (Asc+Sun+Moon)', ...formatLonSign(lagnaLon + sunLon + moonLon) },
    { body: 'Chaturasputa (Sun+Moon)', ...formatLonSign(sunLon + moonLon) },
    { body: 'Pancha Sphuta (+Rahu)', ...formatLonSign(lagnaLon + sunLon + moonLon + (chartData.planets.find((p) => p.name === 'Rahu')?.sidereal_longitude || 0)) },
    { body: 'Prana Sphuta (Asc×5+Moon)', ...formatLonSign(lagnaLon * 5 + moonLon) },
    { body: 'Deha Sphuta (Moon×8+Asc)', ...formatLonSign(moonLon * 8 + lagnaLon) },
    { body: 'Mrityu Sphuta (Asc×7+Sun)', ...formatLonSign(lagnaLon * 7 + sunLon) },
  ];

  return (
    <div className="bg-[#FAF8F2] text-[#2C2A25] p-5 sm:p-7 rounded-xl border border-[#DDD5C4] shadow-sm space-y-7 font-sans">
      {/* TOP BAR: Profile Summary + Varga Selector (D1 to D60) */}
      <div className="flex flex-col gap-3 border-b border-[#CFC6B4] pb-4">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div>
            <h2 className="text-lg font-bold tracking-tight text-[#1E1C18]">
              {profile.name} — {profile.date_of_birth} {profile.time_of_birth}
            </h2>
            <p className="text-xs text-[#6B655B]">
              {profile.birthplace} ({profile.latitude.toFixed(4)}°, {profile.longitude.toFixed(4)}°, UTC {profile.timezone_offset >= 0 ? `+${profile.timezone_offset}` : profile.timezone_offset}) • Ayanamsa: {activeAyanamsa}
            </p>
          </div>
          <button
            onClick={() => window.print()}
            className="flex items-center space-x-1.5 px-3 py-1.5 bg-[#4A3F31] hover:bg-[#362E23] text-white text-xs font-medium rounded transition"
          >
            <Printer className="w-3.5 h-3.5" />
            <span>Print</span>
          </button>
        </div>

        {/* D1 - D60 Selector Strip */}
        <div className="flex flex-wrap items-center gap-1 pt-1">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-[#6B655B] mr-1.5">
            Varga (D1–D60):
          </span>
          {ALL_VARGAS.map((vk) => (
            <button
              key={vk}
              onClick={() => setSelectedVarga(vk)}
              className={`px-2.5 py-1 text-xs font-semibold border transition ${
                selectedVarga === vk
                  ? 'bg-[#4A3F31] text-white border-[#4A3F31]'
                  : 'bg-white text-[#4A3F31] border-[#CFC6B4] hover:bg-[#EFECE3]'
              }`}
            >
              {vk}
            </button>
          ))}
        </div>
      </div>

      {/* SECTION 1: CHART — D1..D60 */}
      <div>
        <div className="flex items-center justify-between border-b border-[#8C8476] pb-1.5 mb-4">
          <h3 className="text-base font-bold text-[#1E1C18] flex items-center space-x-2">
            <span>Chart — {selectedVarga}</span>
            {vargaFull && (
              <span className="text-xs font-normal text-[#6B655B]">({vargaFull.varga_name})</span>
            )}
            {loadingVarga && <RefreshCw className="w-3.5 h-3.5 animate-spin text-[#6B655B]" />}
          </h3>

          {/* North | South Toggle */}
          <div className="inline-flex border border-[#8C8476] text-xs font-semibold">
            <button
              onClick={() => setChartType('north')}
              className={`px-3 py-1 transition ${
                chartType === 'north' ? 'bg-[#4A3F31] text-white' : 'bg-white text-[#4A3F31] hover:bg-[#EFECE3]'
              }`}
            >
              North
            </button>
            <button
              onClick={() => setChartType('south')}
              className={`px-3 py-1 transition ${
                chartType === 'south' ? 'bg-[#4A3F31] text-white' : 'bg-white text-[#4A3F31] hover:bg-[#EFECE3]'
              }`}
            >
              South
            </button>
          </div>
        </div>

        <div className="flex justify-center py-2">
          <div className="w-full max-w-md bg-white/80 p-3 border border-[#CFC6B4]">
            <div className="text-center text-[11px] font-semibold text-[#6B655B] mb-1">{selectedVarga}</div>
            {chartType === 'north' ? (
              <NorthIndianChart houses={chartHouses} planets={chartPlanets} />
            ) : (
              <SouthIndianChart houses={chartHouses} planets={chartPlanets} lagnaRashiNumber={lagnaNum} />
            )}
          </div>
        </div>
      </div>

      {/* SECTION 2: TWO-COLUMN LAYOUT — VARGA DETAILS (LEFT) + UPAGRAHA & SPHUTA (RIGHT) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* LEFT COLUMN: Varga Details — D1..D60 */}
        <div className="lg:col-span-7 space-y-3">
          <div className="border-b border-[#8C8476] pb-1.5">
            <h3 className="text-base font-bold text-[#1E1C18]">Varga Details — {selectedVarga}</h3>
          </div>

          {/* Sub-tabs: Placements | Lagna | Friendship | Aspects */}
          <div className="flex border-b border-[#CFC6B4] text-xs">
            {(['Placements', 'Lagna', 'Friendship', 'Aspects'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setVargaDetailTab(tab)}
                className={`px-3.5 py-1.5 border border-b-0 -mb-px transition ${
                  vargaDetailTab === tab
                    ? 'bg-[#FAF8F2] border-[#8C8476] font-bold text-[#1E1C18]'
                    : 'bg-[#F2EFE7] border-transparent text-[#6B655B] hover:text-[#1E1C18]'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          {vargaDetailTab === 'Placements' && (
            <div className="overflow-x-auto">
              <div className="text-[11px] text-[#6B655B] mb-1.5">Placements</div>
              <table className="w-full text-xs text-left border-collapse">
                <thead>
                  <tr className="border-t border-b border-[#4A3F31] text-[10px] font-bold uppercase tracking-wider text-[#2C2A25]">
                    <th className="py-2 pr-2">BODY</th>
                    <th className="py-2 px-1.5">H</th>
                    <th className="py-2 px-1.5">SIGN</th>
                    <th className="py-2 px-2">DEG</th>
                    <th className="py-2 px-2">NAKSHATRA</th>
                    <th className="py-2 px-1.5 text-center">AMSHA</th>
                    <th className="py-2 px-2">DIGNITY</th>
                    <th className="py-2 px-1.5 text-center">NAT</th>
                    <th className="py-2 px-1.5 text-center">FUNC</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-dashed divide-[#CFC6B4] text-[12px]">
                  {(vargaFull?.placements || []).map((row: any, idx: number) => (
                    <tr key={row.body} className={idx % 2 === 1 ? 'bg-[#F2EFE7]/70' : ''}>
                      <td className="py-2 pr-2 font-bold text-[#1E1C18] whitespace-nowrap">
                        {row.body}
                        {row.is_retrograde && <span className="ml-1 text-emerald-700 font-bold">*</span>}
                      </td>
                      <td className="py-2 px-1.5 font-mono text-[#2C2A25]">{row.house}</td>
                      <td className="py-2 px-1.5 font-medium text-[#2C2A25]">{row.sign_abbr}</td>
                      <td className="py-2 px-2 font-mono text-[#2C2A25] whitespace-nowrap">{row.deg}</td>
                      <td className="py-2 px-2 text-[#2C2A25] whitespace-nowrap">{row.nakshatra}</td>
                      <td className="py-2 px-1.5 text-center font-mono text-[#2C2A25]">{row.amsha}</td>
                      <td className="py-2 px-2 text-[#2C2A25]">{row.dignity}</td>
                      <td className="py-2 px-1.5 text-center font-mono">{row.nat}</td>
                      <td className="py-2 px-1.5 text-center font-mono">{row.func}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {vargaDetailTab === 'Lagna' && vargaFull && (
            <div className="p-4 bg-[#F2EFE7]/60 border border-[#CFC6B4] text-xs space-y-2">
              <div><strong>{selectedVarga} Lagna Sign:</strong> {vargaFull.lagna_rashi} ({vargaFull.lagna_sign_abbr})</div>
              <div><strong>{selectedVarga} Lagna Degree:</strong> {vargaFull.lagna_deg}</div>
              <div><strong>D1 Birth Lagna:</strong> {chartData.chart_summary.lagna_rashi} {chartData.chart_summary.lagna_dms} ({chartData.chart_summary.lagna_nakshatra} Pada {chartData.chart_summary.lagna_pada})</div>
              <div><strong>Lagna Lord:</strong> {chartData.chart_summary.lagna_lord}</div>
            </div>
          )}

          {vargaDetailTab === 'Friendship' && (
            <div className="p-4 bg-[#F2EFE7]/60 border border-[#CFC6B4] text-xs">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-[#4A3F31] text-[10px] uppercase">
                    <th className="py-1.5">Planet</th>
                    <th className="py-1.5">Sign in {selectedVarga}</th>
                    <th className="py-1.5">Dignity</th>
                    <th className="py-1.5">Natural / Functional</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-dashed divide-[#CFC6B4]">
                  {(vargaFull?.placements || []).map((r: any) => (
                    <tr key={r.body}>
                      <td className="py-1.5 font-bold">{r.body}</td>
                      <td className="py-1.5">{r.sign}</td>
                      <td className="py-1.5">{r.dignity}</td>
                      <td className="py-1.5 font-mono">{r.nat} / {r.func}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {vargaDetailTab === 'Aspects' && (
            <div className="p-4 bg-[#F2EFE7]/60 border border-[#CFC6B4] text-xs">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-[#4A3F31] text-[10px] uppercase">
                    <th className="py-1.5">House</th>
                    <th className="py-1.5">Sign</th>
                    <th className="py-1.5">Occupants</th>
                    <th className="py-1.5">Aspecting Planets (D1)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-dashed divide-[#CFC6B4]">
                  {chartHouses.map((h) => {
                    const d1H = chartData.houses.find((x) => x.house_number === h.house_number);
                    return (
                      <tr key={h.house_number}>
                        <td className="py-1.5 font-bold">H{h.house_number}</td>
                        <td className="py-1.5">{h.sign}</td>
                        <td className="py-1.5">{h.occupants.join(', ') || '—'}</td>
                        <td className="py-1.5">{d1H?.aspecting_planets.join(', ') || '—'}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* RIGHT COLUMN: Upagraha & Sphuta */}
        <div className="lg:col-span-5 space-y-3">
          <div className="border-b border-[#8C8476] pb-1.5">
            <h3 className="text-base font-bold text-[#1E1C18]">Upagraha &amp; Sphuta</h3>
          </div>

          <div className="flex border-b border-[#CFC6B4] text-xs">
            {(['Upagraha', 'Sphuta', 'Varnada', 'Tithi'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setUpagrahaTab(tab)}
                className={`px-3.5 py-1.5 border border-b-0 -mb-px transition ${
                  upagrahaTab === tab
                    ? 'bg-[#FAF8F2] border-[#8C8476] font-bold text-[#1E1C18]'
                    : 'bg-[#F2EFE7] border-transparent text-[#6B655B] hover:text-[#1E1C18]'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          {upagrahaTab === 'Upagraha' && (
            <div className="overflow-x-auto">
              <div className="text-[11px] text-[#6B655B] mb-1.5">Upagraha Details ({selectedVarga})</div>
              <table className="w-full text-xs text-left border-collapse">
                <thead>
                  <tr className="border-t border-b border-[#4A3F31] text-[10px] font-bold uppercase tracking-wider text-[#2C2A25]">
                    <th className="py-2 pr-2">BODY</th>
                    <th className="py-2 px-2">SIGN</th>
                    <th className="py-2 px-2">DEGREES</th>
                    <th className="py-2 pl-2 text-right">HOUSE</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-dashed divide-[#CFC6B4] text-[12px]">
                  {(vargaFull?.upagrahas || []).map((u: any, idx: number) => (
                    <tr key={u.body} className={idx % 2 === 1 ? 'bg-[#F2EFE7]/70' : ''}>
                      <td className="py-2 pr-2 font-bold text-[#1E1C18]">{u.body}</td>
                      <td className="py-2 px-2 text-[#2C2A25]">{u.sign}</td>
                      <td className="py-2 px-2 font-mono text-[#2C2A25] whitespace-nowrap">{u.degrees}</td>
                      <td className="py-2 pl-2 text-right font-mono text-[#2C2A25]">{u.house}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <p className="text-[10px] text-[#6B655B] mt-2">
                Degrees show sign-relative DMS; houses mapped in {selectedVarga}.
              </p>
            </div>
          )}

          {upagrahaTab === 'Sphuta' && (
            <div className="overflow-x-auto">
              <div className="text-[11px] text-[#6B655B] mb-1.5">Classical Sphutas</div>
              <table className="w-full text-xs text-left border-collapse">
                <thead>
                  <tr className="border-t border-b border-[#4A3F31] text-[10px] font-bold uppercase tracking-wider text-[#2C2A25]">
                    <th className="py-2 pr-2">BODY</th>
                    <th className="py-2 px-2">SIGN</th>
                    <th className="py-2 px-2">DEGREES</th>
                    <th className="py-2 pl-2 text-right">HOUSE</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-dashed divide-[#CFC6B4] text-[12px]">
                  {sphutaList.map((sp, idx) => (
                    <tr key={sp.body} className={idx % 2 === 1 ? 'bg-[#F2EFE7]/70' : ''}>
                      <td className="py-2 pr-2 font-bold text-[#1E1C18]">{sp.body}</td>
                      <td className="py-2 px-2 text-[#2C2A25]">{sp.sign}</td>
                      <td className="py-2 px-2 font-mono text-[#2C2A25] whitespace-nowrap">{sp.dms}</td>
                      <td className="py-2 pl-2 text-right font-mono text-[#2C2A25]">{sp.house}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {upagrahaTab === 'Varnada' && (
            <div className="overflow-x-auto">
              <div className="flex justify-between items-center text-[11px] text-[#6B655B] mb-1.5">
                <span>Varnada</span>
                <span>whole sign</span>
              </div>
              <table className="w-full text-xs text-left border-collapse">
                <thead>
                  <tr className="border-t border-b border-[#4A3F31] text-[10px] font-bold uppercase tracking-wider text-[#2C2A25]">
                    <th className="py-2 pr-2">VARNADA</th>
                    <th className="py-2 px-2">SIGN</th>
                    <th className="py-2 pl-2 text-right">HOUSE</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-dashed divide-[#CFC6B4] text-[12px]">
                  {(vargaFull?.varnada || []).map((v: any, idx: number) => (
                    <tr key={v.varnada} className={idx % 2 === 1 ? 'bg-[#F2EFE7]/70' : ''}>
                      <td className="py-2 pr-2 font-bold text-[#1E1C18]">{v.varnada}</td>
                      <td className="py-2 px-2 text-[#2C2A25]">{v.sign}</td>
                      <td className="py-2 pl-2 text-right font-mono text-[#2C2A25]">{v.house}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <p className="text-[10px] text-[#6B655B] mt-2">
                One varnada for each house. These are whole signs and carry no degree of their own.
              </p>
            </div>
          )}

          {upagrahaTab === 'Tithi' && (
            <div className="overflow-x-auto">
              <div className="flex justify-between items-center text-[11px] text-[#6B655B] mb-1.5">
                <span>Special Tithi</span>
                <span>lord · deity</span>
              </div>
              <table className="w-full text-xs text-left border-collapse">
                <thead>
                  <tr className="border-t border-b border-[#4A3F31] text-[10px] font-bold uppercase tracking-wider text-[#2C2A25]">
                    <th className="py-2 pr-2">TITHI</th>
                    <th className="py-2 px-1.5">NAME</th>
                    <th className="py-2 px-1.5 text-right">% LEFT</th>
                    <th className="py-2 px-1.5">LORD</th>
                    <th className="py-2 pl-1.5">DEITY</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-dashed divide-[#CFC6B4] text-[11px]">
                  {(vargaFull?.special_tithis || []).map((t: any, idx: number) => (
                    <tr key={t.tithi} className={idx % 2 === 1 ? 'bg-[#F2EFE7]/70' : ''}>
                      <td className="py-2 pr-2 font-bold text-[#1E1C18]">{t.tithi}</td>
                      <td className="py-2 px-1.5 text-[#2C2A25]">{t.name}</td>
                      <td className="py-2 px-1.5 text-right font-mono">{t.pct_left}</td>
                      <td className="py-2 px-1.5 text-[#2C2A25]">{t.lord}</td>
                      <td className="py-2 pl-1.5 text-[#2C2A25]">{t.deity}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <p className="text-[10px] text-[#6B655B] mt-2">
                A tithi for each house, taken from how far the Moon stood from the Sun at birth.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* SECTION 3: STRENGTH DETAILS (Vimshopaka, Shadbala, Ashtakavarga, Vimshottari Dasha) */}
      <div className="space-y-3 pt-2">
        <div className="border-b border-[#8C8476] pb-1.5">
          <h3 className="text-base font-bold text-[#1E1C18]">Strength Details</h3>
        </div>

        {/* Main Tabs */}
        <div className="flex border-b border-[#CFC6B4] text-xs">
          {(['Vimshopaka', 'Shadbala', 'Ashtakavarga', 'Dasha'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setStrengthMainTab(tab)}
              className={`px-4 py-1.5 border border-b-0 -mb-px transition ${
                strengthMainTab === tab
                  ? 'bg-[#FAF8F2] border-[#8C8476] font-bold text-[#1E1C18]'
                  : 'bg-[#F2EFE7] border-transparent text-[#6B655B] hover:text-[#1E1C18]'
              }`}
            >
              {tab === 'Dasha' ? 'Vimshottari Dasha at Birth' : tab}
            </button>
          ))}
        </div>

        {strengthMainTab === 'Vimshopaka' && (
          <div className="space-y-3">
            {/* Sub-tabs: Shad | Sapta | Dasha | Shodasha */}
            <div className="flex border-b border-[#CFC6B4] text-xs">
              {(['Shad', 'Sapta', 'Dasha', 'Shodasha'] as const).map((sub) => (
                <button
                  key={sub}
                  onClick={() => setVimshopakaSubTab(sub)}
                  className={`px-3.5 py-1.5 border border-b-0 -mb-px transition ${
                    vimshopakaSubTab === sub
                      ? 'bg-[#FAF8F2] border-[#8C8476] font-bold text-[#1E1C18]'
                      : 'bg-[#F2EFE7] border-transparent text-[#6B655B] hover:text-[#1E1C18]'
                  }`}
                >
                  {sub}
                </button>
              ))}
            </div>

            <div className="flex justify-between items-center text-[11px] text-[#6B655B]">
              <span>Vimshopaka — {vimshopakaSubTab}</span>
              <span>score/20 · % · band · designation</span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left border-collapse">
                <thead>
                  <tr className="border-t border-b border-[#4A3F31] text-[10px] font-bold uppercase tracking-wider text-[#2C2A25]">
                    <th className="py-2 pr-3">BODY</th>
                    <th className="py-2 px-3">SCORE/20</th>
                    <th className="py-2 px-3">%</th>
                    <th className="py-2 px-3 w-40">METER</th>
                    <th className="py-2 px-3">BAND</th>
                    <th className="py-2 pl-3">DESIGNATION</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-dashed divide-[#CFC6B4] text-[12px]">
                  {vimshopakaRows.map((row: any, idx: number) => (
                    <tr key={row.body} className={idx % 2 === 1 ? 'bg-[#F2EFE7]/70' : ''}>
                      <td className="py-2.5 pr-3 font-bold text-[#1E1C18]">{row.body}</td>
                      <td className="py-2.5 px-3 font-mono">{row.score.toFixed(2)}</td>
                      <td className="py-2.5 px-3 font-mono">{row.pct.toFixed(2)}%</td>
                      <td className="py-2.5 px-3">
                        <div className="w-32 h-2.5 bg-[#E6E0D2] border border-[#B8B09E] overflow-hidden">
                          <div
                            className="h-full bg-[#A8A090]"
                            style={{ width: `${Math.min(100, Math.max(0, row.pct))}%` }}
                          />
                        </div>
                      </td>
                      <td className="py-2.5 px-3">{row.band}</td>
                      <td className="py-2.5 pl-3 font-mono">{row.designation}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {strengthMainTab === 'Shadbala' && (
          <div className="space-y-3">
            <div className="flex justify-between items-center text-[11px] text-[#6B655B]">
              <span>Shadbala</span>
              <span>Sthāna · Dig · Kāla · Ceṣṭā · Naisargika · Drik · Total · Rūpa · %</span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left border-collapse">
                <thead>
                  <tr className="border-t border-b border-[#4A3F31] text-[10px] font-bold uppercase tracking-wider text-[#2C2A25]">
                    <th className="py-2 pr-2">BODY</th>
                    <th className="py-2 px-2">STHANA</th>
                    <th className="py-2 px-2">DIG</th>
                    <th className="py-2 px-2">KALA</th>
                    <th className="py-2 px-2">CHESTA</th>
                    <th className="py-2 px-2">NAISARGIKA</th>
                    <th className="py-2 px-2">DRIK</th>
                    <th className="py-2 px-2">TOTAL</th>
                    <th className="py-2 px-2">RŪPA</th>
                    <th className="py-2 px-2">%</th>
                    <th className="py-2 px-2">METER</th>
                    <th className="py-2 pl-2 text-center">MIN</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-dashed divide-[#CFC6B4] text-[12px]">
                  {(vargaFull?.shadbala || []).map((row: any, idx: number) => (
                    <tr key={row.body} className={idx % 2 === 1 ? 'bg-[#F2EFE7]/70' : ''}>
                      <td className="py-2.5 pr-2 font-bold text-[#1E1C18]">{row.body}</td>
                      <td className="py-2.5 px-2 font-mono">{row.sthana.toFixed(2)}</td>
                      <td className="py-2.5 px-2 font-mono">{row.dig.toFixed(2)}</td>
                      <td className="py-2.5 px-2 font-mono">{row.kala.toFixed(2)}</td>
                      <td className="py-2.5 px-2 font-mono">{row.chesta.toFixed(2)}</td>
                      <td className="py-2.5 px-2 font-mono">{row.naisargika.toFixed(2)}</td>
                      <td className="py-2.5 px-2 font-mono">{row.drik.toFixed(2)}</td>
                      <td className="py-2.5 px-2 font-mono font-bold">{row.total.toFixed(2)}</td>
                      <td className="py-2.5 px-2 font-mono">{row.rupa.toFixed(2)}</td>
                      <td className="py-2.5 px-2 font-mono">{row.pct.toFixed(2)}%</td>
                      <td className="py-2.5 px-2">
                        <div className="w-24 h-2.5 bg-[#E6E0D2] border border-[#B8B09E] overflow-hidden">
                          <div
                            className="h-full bg-[#A8A090]"
                            style={{ width: `${Math.min(100, Math.max(0, (row.pct / 200) * 100))}%` }}
                          />
                        </div>
                      </td>
                      <td className="py-2.5 pl-2 text-center font-bold">
                        {row.meets_min ? '✓' : '—'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {strengthMainTab === 'Ashtakavarga' && vargaFull?.ashtakavarga && (
          <div className="space-y-3">
            <div className="flex justify-between items-center text-[11px] text-[#6B655B]">
              <span>Ashtakavarga — {selectedVarga}</span>
              <span>rekhas 0–8 · SAV 0–56 · Lagna {vargaFull.lagna_rashi}</span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left border-collapse">
                <thead>
                  <tr className="border-t border-b border-[#4A3F31] text-[10px] font-bold uppercase tracking-wider text-[#2C2A25]">
                    <th className="py-2 pr-3">BODY</th>
                    {['AR', 'TA', 'GE', 'CN', 'LE', 'VI', 'LI', 'SC', 'SG', 'CP', 'AQ', 'PI'].map((s) => (
                      <th key={s} className="py-2 px-1.5 text-center">{s}</th>
                    ))}
                    <th className="py-2 pl-2 text-right">TOT</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-dashed divide-[#CFC6B4] text-[12px]">
                  {vargaFull.ashtakavarga.rows.map((row: any, idx: number) => (
                    <tr key={row.body} className={idx % 2 === 1 ? 'bg-[#F2EFE7]/70' : ''}>
                      <td className="py-2 pr-3 font-bold text-[#1E1C18]">{row.body}</td>
                      {row.signs.map((cnt: number, si: number) => (
                        <td key={si} className="py-2 px-1.5 text-center font-mono">{cnt}</td>
                      ))}
                      <td className="py-2 pl-2 text-right font-mono font-bold">{row.total}</td>
                    </tr>
                  ))}
                  <tr className="border-t border-[#4A3F31] bg-[#F2EFE7] font-bold">
                    <td className="py-2 pr-3 text-[#1E1C18]">SAV</td>
                    {vargaFull.ashtakavarga.sav.map((cnt: number, si: number) => (
                      <td key={si} className="py-2 px-1.5 text-center font-mono">{cnt}</td>
                    ))}
                    <td className="py-2 pl-2 text-right font-mono">{vargaFull.ashtakavarga.sav_total}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        )}

        {strengthMainTab === 'Dasha' && dashaData && (
          <div className="p-4 bg-[#F2EFE7]/60 border border-[#CFC6B4] space-y-3 text-xs">
            <div className="space-y-1">
              <div className="font-bold text-sm text-[#1E1C18]">Vimshottari Dasha at Birth</div>
              <div>
                Birth Nakshatra: <strong>{dashaData.birth_nakshatra}</strong> (Ruled by{' '}
                <strong>{dashaData.birth_nakshatra_lord || dashaData.starting_mahadasha_lord}</strong>)
              </div>
              <div>
                Balance of Dasha at Birth:{' '}
                <strong>
                  {dashaData.starting_mahadasha_lord} – {dashaData.balance_years} years
                </strong>{' '}
                ({dashaData.balance_ymd || ''})
              </div>
            </div>
            <div className="grid grid-cols-3 sm:grid-cols-5 md:grid-cols-9 gap-2 pt-2 font-mono">
              {dashaData.dashas.map((d) => (
                <div
                  key={d.planet}
                  className={`p-2 border text-center ${
                    d.is_current
                      ? 'bg-[#4A3F31] text-white border-[#4A3F31] font-bold'
                      : 'bg-white border-[#CFC6B4] text-[#2C2A25]'
                  }`}
                >
                  <div>{d.abbr || d.planet.substring(0, 2)}: {d.end_year || d.end_date.substring(0, 4)}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
