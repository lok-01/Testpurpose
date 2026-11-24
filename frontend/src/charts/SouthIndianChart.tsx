import React from 'react';
import { PlanetPosition, HouseCusp } from '../types';

interface SouthIndianChartProps {
  houses: HouseCusp[];
  planets: PlanetPosition[];
  lagnaRashiNumber: number;
  onSelectHouse?: (house: HouseCusp) => void;
  selectedHouseNumber?: number;
}

export const SouthIndianChart: React.FC<SouthIndianChartProps> = ({
  houses,
  planets,
  lagnaRashiNumber,
  onSelectHouse,
  selectedHouseNumber,
}) => {
  // Grid layout for 12 signs in South Indian chart (row, col)
  const SIGN_GRID: Record<number, { r: number; c: number; name: string }> = {
    12: { r: 0, c: 0, name: 'Pisces' },
    1: { r: 0, c: 1, name: 'Aries' },
    2: { r: 0, c: 2, name: 'Taurus' },
    3: { r: 0, c: 3, name: 'Gemini' },
    4: { r: 1, c: 3, name: 'Cancer' },
    5: { r: 2, c: 3, name: 'Leo' },
    6: { r: 3, c: 3, name: 'Virgo' },
    7: { r: 3, c: 2, name: 'Libra' },
    8: { r: 3, c: 1, name: 'Scorpio' },
    9: { r: 3, c: 0, name: 'Sagittarius' },
    10: { r: 2, c: 0, name: 'Capricorn' },
    11: { r: 1, c: 0, name: 'Aquarius' },
  };

  const getPlanetsInSign = (signNum: number) => {
    return planets.filter((p) => p.rashi_number === signNum);
  };

  const getHouseForSign = (signNum: number) => {
    return houses.find((h) => h.sign_number === signNum);
  };

  return (
    <div className="relative w-full max-w-[480px] mx-auto bg-white p-3 rounded-xl shadow-md border border-slate-200">
      <div className="flex justify-between items-center mb-2 px-1">
        <span className="text-xs font-semibold tracking-wider text-vedic-navy uppercase font-cinzel">
          South Indian Vedic Kundli (D1)
        </span>
        <span className="text-[11px] text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200 font-medium">
          Fixed Sign Matrix
        </span>
      </div>

      <div className="grid grid-cols-4 grid-rows-4 w-full aspect-square border-2 border-vedic-navy bg-[#FCFDFE]">
        {/* Render 16 cells (12 signs + 4 center cells) */}
        {[0, 1, 2, 3].map((r) =>
          [0, 1, 2, 3].map((c) => {
            // Check if center 2x2
            if ((r === 1 || r === 2) && (c === 1 || c === 2)) {
              if (r === 1 && c === 1) {
                return (
                  <div
                    key={`${r}-${c}`}
                    className="col-span-2 row-span-2 border border-slate-200 bg-slate-50 flex flex-col items-center justify-center p-2 text-center"
                  >
                    <span className="text-xs font-cinzel font-bold text-vedic-navy uppercase tracking-widest">
                      AstroRize Lab
                    </span>
                    <span className="text-[10px] text-slate-500 mt-1">Swiss Ephemeris 2.10</span>
                    <span className="text-[10px] text-amber-600 font-medium">Lahiri Chitrapaksha</span>
                  </div>
                );
              }
              return null;
            }

            // Find sign for this (r, c)
            const signEntry = Object.entries(SIGN_GRID).find(
              ([_, pos]) => pos.r === r && pos.c === c
            );
            if (!signEntry) return null;

            const signNum = parseInt(signEntry[0], 10);
            const signData = signEntry[1];
            const isLagna = signNum === lagnaRashiNumber;
            const houseObj = getHouseForSign(signNum);
            const isSelected = houseObj && selectedHouseNumber === houseObj.house_number;
            const occupants = getPlanetsInSign(signNum);

            return (
              <div
                key={signNum}
                onClick={() => houseObj && onSelectHouse && onSelectHouse(houseObj)}
                className={`relative border border-slate-300 p-1.5 flex flex-col justify-between cursor-pointer transition-colors duration-150 ${
                  isSelected ? 'bg-amber-100/70' : 'hover:bg-slate-50'
                }`}
              >
                {/* Sign Label & House Number */}
                <div className="flex justify-between items-center text-[10px] leading-tight">
                  <span className="font-semibold text-slate-600">{signData.name.substring(0, 3)}</span>
                  {houseObj && (
                    <span className="text-[9px] text-slate-400 font-mono">H{houseObj.house_number}</span>
                  )}
                </div>

                {/* Lagna indicator diagonal badge */}
                {isLagna && (
                  <div className="absolute top-0 right-0 w-3 h-3 border-t-2 border-r-2 border-amber-600">
                    <span className="absolute -top-1 -right-1 text-[8px] font-bold text-amber-700">L</span>
                  </div>
                )}

                {/* Occupant Planets */}
                <div className="flex flex-wrap gap-1 my-auto justify-center">
                  {occupants.map((p) => (
                    <span
                      key={p.name}
                      className={`text-[11px] font-bold px-1 rounded ${
                        p.name === 'Sun' || p.name === 'Moon'
                          ? 'text-amber-800 bg-amber-50'
                          : p.is_combust
                          ? 'text-red-600 bg-red-50'
                          : 'text-slate-800'
                      }`}
                    >
                      {p.name.substring(0, 2)}
                      {p.is_retrograde && <span className="text-[9px] text-red-500">Ⓡ</span>}
                    </span>
                  ))}
                </div>
              </div>
            );
          })
        )}
      </div>

      <div className="mt-2 flex justify-between text-[11px] text-slate-500 px-1">
        <span>Click any box to inspect house details</span>
        <span>L = Lagna (Ascendant)</span>
      </div>
    </div>
  );
};
