import React, { useState } from 'react';
import { DashaData, VimshottariDashaLevel } from '../types';
import { Clock, ChevronRight, ChevronDown, Sparkles, CheckCircle2 } from 'lucide-react';

interface ParasharaDashaCardProps {
  dashaData: DashaData | null;
  compact?: boolean;
}

export const ParasharaDashaCard: React.FC<ParasharaDashaCardProps> = ({ dashaData, compact = false }) => {
  const [expandedMd, setExpandedMd] = useState<string | null>(null);
  const [expandedAd, setExpandedAd] = useState<string | null>(null);

  if (!dashaData) {
    return (
      <div className="bg-white p-6 rounded-xl border border-slate-200 text-center text-xs text-slate-500">
        No Dasha progression available. Select or calculate a profile.
      </div>
    );
  }

  const nakLord = dashaData.birth_nakshatra_lord || dashaData.starting_mahadasha_lord;
  const balanceYmd = dashaData.balance_ymd || `${dashaData.balance_years} years`;

  // Auto-expand current MD on initial load
  React.useEffect(() => {
    if (dashaData.current_mahadasha && !expandedMd) {
      setExpandedMd(dashaData.current_mahadasha);
    }
  }, [dashaData]);

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      {/* CLASSIC PARASHARA'S LIGHT HEADER BANNER */}
      <div className="bg-[#0B1B3D] text-amber-300 p-4 border-b border-amber-500/30">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <div className="flex items-center space-x-2">
              <Clock className="w-4 h-4 text-amber-400" />
              <h3 className="font-cinzel text-sm sm:text-base font-bold tracking-wide text-white">
                Vimshottari Dasha at Birth
              </h3>
            </div>
            <div className="mt-1.5 space-y-0.5 text-xs">
              <div className="text-slate-200 font-medium">
                Birth Nakshatra:{' '}
                <strong className="text-amber-300">{dashaData.birth_nakshatra}</strong>
                {dashaData.birth_nakshatra_pada && (
                  <span className="text-slate-300"> (Pada {dashaData.birth_nakshatra_pada})</span>
                )}{' '}
                <span className="text-amber-200/80 font-normal">
                  (Ruled by {nakLord})
                </span>
              </div>
              <div className="text-slate-200 font-medium">
                Balance of Dasha at Birth:{' '}
                <strong className="text-emerald-400 font-mono">
                  {nakLord} – {dashaData.balance_years} years
                </strong>{' '}
                <span className="text-slate-300 font-mono text-[11px]">({balanceYmd})</span>
              </div>
            </div>
          </div>

          {/* Running Period Badge */}
          <div className="bg-slate-900/80 border border-amber-400/40 rounded-lg p-2 text-right">
            <span className="text-[10px] uppercase font-mono text-amber-300/80 tracking-wider block">
              Currently Running
            </span>
            <span className="text-xs font-bold text-white font-mono">
              {dashaData.current_mahadasha} - {dashaData.current_antardasha} - {dashaData.current_pratyantardasha}
            </span>
          </div>
        </div>
      </div>

      {/* PARASHARA COMPACT LIST + DRILLDOWN ACCORDION */}
      <div className="p-4 bg-slate-50">
        {/* PARASHARA QUICK-CODE GRID (e.g. Ke: 2005, Ve: 2025, Su: 2031...) */}
        <div className="mb-4">
          <div className="text-[11px] uppercase font-bold text-slate-500 font-mono mb-2 flex items-center justify-between">
            <span>Parashara Dasha Ending Years (Click to expand Antardashas)</span>
            <span className="text-[10px] text-amber-700 font-normal">
              Cycle: 120 Solar Years
            </span>
          </div>
          <div className="grid grid-cols-3 sm:grid-cols-5 md:grid-cols-9 gap-2">
            {dashaData.dashas.map((md) => {
              const abbr = md.abbr || md.planet.substring(0, 2);
              const isSelected = expandedMd === md.planet;
              return (
                <button
                  key={md.planet}
                  type="button"
                  onClick={() => {
                    setExpandedMd(isSelected ? null : md.planet);
                    setExpandedAd(null);
                  }}
                  className={`p-2 rounded-lg border text-left transition font-mono relative flex flex-col justify-between ${
                    md.is_current
                      ? 'bg-amber-100 border-amber-400 text-vedic-navy shadow-sm ring-1 ring-amber-400'
                      : isSelected
                      ? 'bg-blue-50 border-blue-400 text-blue-900'
                      : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-100'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-xs">
                      {abbr}: {md.end_year || md.end_date.substring(0, 4)}
                    </span>
                    {md.is_current && (
                      <span className="w-1.5 h-1.5 rounded-full bg-amber-500 animate-ping" />
                    )}
                  </div>
                  <span className="text-[10px] text-slate-500 truncate mt-0.5">
                    {md.planet}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        {/* DETAILED DRILLDOWN FOR SELECTED MAHADASHA */}
        {expandedMd && (
          <div className="mt-4 bg-white p-4 rounded-xl border border-slate-200 shadow-sm animate-fadeIn">
            {(() => {
              const activeMd = dashaData.dashas.find((m) => m.planet === expandedMd);
              if (!activeMd) return null;
              const mdAbbr = activeMd.abbr || activeMd.planet.substring(0, 2);

              return (
                <div className="space-y-3">
                  <div className="flex items-center justify-between border-b border-slate-200 pb-2">
                    <div>
                      <h4 className="font-cinzel text-xs sm:text-sm font-bold text-vedic-navy flex items-center space-x-2">
                        <span className="w-6 h-6 rounded bg-vedic-navy text-amber-300 text-xs font-bold font-mono flex items-center justify-center">
                          {mdAbbr}
                        </span>
                        <span>{activeMd.planet} Mahadasha</span>
                        {activeMd.is_current && (
                          <span className="px-2 py-0.5 text-[10px] bg-amber-100 text-amber-800 font-bold rounded-full border border-amber-300">
                            Current MD
                          </span>
                        )}
                      </h4>
                      <p className="text-[11px] text-slate-500 font-mono mt-0.5">
                        Duration: {activeMd.start_date} to {activeMd.end_date} ({activeMd.duration_years} Years)
                      </p>
                    </div>
                    <span className="text-xs text-slate-400 font-mono">
                      {activeMd.sub_periods?.length || 9} Antardashas
                    </span>
                  </div>

                  {/* ANTARDASHA TABLE / CHIPS */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
                    {activeMd.sub_periods?.map((ad) => {
                      const adAbbr = ad.abbr || ad.planet.substring(0, 2);
                      const pairCode = ad.pair_abbr || `${mdAbbr}-${adAbbr}`;
                      const isAdSelected = expandedAd === ad.planet;

                      return (
                        <div
                          key={ad.planet}
                          onClick={() => setExpandedAd(isAdSelected ? null : ad.planet)}
                          className={`p-2.5 rounded-lg border text-xs cursor-pointer transition ${
                            ad.is_current
                              ? 'bg-amber-50 border-amber-400 font-semibold ring-1 ring-amber-300'
                              : isAdSelected
                              ? 'bg-blue-50 border-blue-300'
                              : 'bg-slate-50 border-slate-200 hover:bg-slate-100'
                          }`}
                        >
                          <div className="flex justify-between items-center font-mono">
                            <span className="font-bold text-slate-800 text-xs">
                              {pairCode} ({ad.planet})
                            </span>
                            {ad.is_current && (
                              <span className="text-[10px] text-amber-700 font-bold bg-amber-100 px-1.5 py-0.2 rounded">
                                Active AD
                              </span>
                            )}
                          </div>
                          <div className="text-[11px] text-slate-500 font-mono mt-1 flex justify-between">
                            <span>{ad.start_date}</span>
                            <span>→</span>
                            <span className="font-semibold text-slate-700">{ad.end_date}</span>
                          </div>

                          {/* Pratyantardasha Accordion */}
                          {isAdSelected && ad.sub_periods && (
                            <div className="mt-2 pt-2 border-t border-slate-200 space-y-1">
                              <span className="text-[10px] uppercase font-mono text-slate-400 block mb-1">
                                Pratyantardashas (PD):
                              </span>
                              <div className="space-y-1 max-h-36 overflow-y-auto text-[10px] font-mono">
                                {ad.sub_periods.map((pd) => (
                                  <div
                                    key={pd.planet}
                                    className={`p-1 rounded flex justify-between ${
                                      pd.is_current
                                        ? 'bg-amber-200 text-amber-900 font-bold'
                                        : 'bg-white text-slate-600'
                                    }`}
                                  >
                                    <span>
                                      {pairCode}-{pd.planet.substring(0, 2)}
                                    </span>
                                    <span>
                                      {pd.start_date.substring(5)} to {pd.end_date.substring(5)}
                                    </span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })()}
          </div>
        )}
      </div>
    </div>
  );
};
