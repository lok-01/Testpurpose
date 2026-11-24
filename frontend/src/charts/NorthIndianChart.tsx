import React from 'react';
import { PlanetPosition, HouseCusp } from '../types';

interface NorthIndianChartProps {
  houses: HouseCusp[];
  planets: PlanetPosition[];
  onSelectHouse?: (house: HouseCusp) => void;
  selectedHouseNumber?: number;
}

export const NorthIndianChart: React.FC<NorthIndianChartProps> = ({
  houses,
  planets,
  onSelectHouse,
  selectedHouseNumber,
}) => {
  // House polygon geometry on a 400x400 SVG canvas
  // 1: Top Diamond (Ascendant / Lagna)
  // 2: Top Left Triangle
  // 3: Left Top Triangle
  // 4: Left Diamond
  // 5: Left Bottom Triangle
  // 6: Bottom Left Triangle
  // 7: Bottom Diamond
  // 8: Bottom Right Triangle
  // 9: Right Bottom Triangle
  // 10: Right Diamond
  // 11: Right Top Triangle
  // 12: Top Right Triangle
  
  const houseCoords: Record<number, { points: string; textPos: [number, number]; labelPos: [number, number] }> = {
    1: { points: "200,0 300,100 200,200 100,100", textPos: [200, 110], labelPos: [200, 45] },
    2: { points: "100,100 200,0 0,0", textPos: [115, 45], labelPos: [140, 25] },
    3: { points: "0,0 100,100 0,200", textPos: [45, 115], labelPos: [25, 140] },
    4: { points: "100,100 0,200 100,300 200,200", textPos: [110, 200], labelPos: [45, 200] },
    5: { points: "0,200 100,300 0,400", textPos: [45, 285], labelPos: [25, 260] },
    6: { points: "0,400 100,300 200,400", textPos: [115, 355], labelPos: [140, 375] },
    7: { points: "200,200 100,300 200,400 300,300", textPos: [200, 290], labelPos: [200, 355] },
    8: { points: "200,400 300,300 400,400", textPos: [285, 355], labelPos: [260, 375] },
    9: { points: "300,300 400,200 400,400", textPos: [355, 285], labelPos: [375, 260] },
    10: { points: "300,100 200,200 300,300 400,200", textPos: [290, 200], labelPos: [355, 200] },
    11: { points: "400,0 400,200 300,100", textPos: [355, 115], labelPos: [375, 140] },
    12: { points: "200,0 300,100 400,0", textPos: [285, 45], labelPos: [260, 25] },
  };

  const getPlanetsInHouse = (hNum: number) => {
    return planets.filter((p) => p.house === hNum);
  };

  const getSignNumInHouse = (hNum: number) => {
    const h = houses.find((x) => x.house_number === hNum);
    return h ? h.sign_number : '';
  };

  return (
    <div className="relative w-full max-w-[480px] mx-auto bg-white p-3 rounded-xl shadow-md border border-slate-200">
      <div className="flex justify-between items-center mb-2 px-1">
        <span className="text-xs font-semibold tracking-wider text-vedic-navy uppercase font-cinzel">
          North Indian Vedic Kundli (D1)
        </span>
        <span className="text-[11px] text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200 font-medium">
          Whole Sign Houses
        </span>
      </div>

      <svg viewBox="0 0 400 400" className="w-full h-auto drop-shadow-sm select-none">
        {/* Outer background */}
        <rect x="0" y="0" width="400" height="400" fill="#FCFDFE" stroke="#0B1B3D" strokeWidth="2.5" />

        {/* Diagonal & cross division lines */}
        <line x1="0" y1="0" x2="400" y2="400" stroke="#0B1B3D" strokeWidth="1.5" />
        <line x1="400" y1="0" x2="0" y2="400" stroke="#0B1B3D" strokeWidth="1.5" />
        <polygon points="200,0 400,200 200,400 0,200" fill="none" stroke="#0B1B3D" strokeWidth="1.8" />

        {/* 12 House Polygons */}
        {Object.entries(houseCoords).map(([hStr, data]) => {
          const hNum = parseInt(hStr, 10);
          const isSelected = selectedHouseNumber === hNum;
          const occupants = getPlanetsInHouse(hNum);
          const signNum = getSignNumInHouse(hNum);
          const houseObj = houses.find((h) => h.house_number === hNum);

          return (
            <g
              key={hNum}
              className="cursor-pointer transition-colors duration-150 group"
              onClick={() => houseObj && onSelectHouse && onSelectHouse(houseObj)}
            >
              <polygon
                points={data.points}
                fill={isSelected ? '#FEF3C7' : 'transparent'}
                className="hover:fill-amber-50/60"
              />

              {/* Rashi / Sign Number badge */}
              <text
                x={data.labelPos[0]}
                y={data.labelPos[1]}
                textAnchor="middle"
                dominantBaseline="central"
                className="text-[11px] font-bold fill-slate-400 font-mono"
              >
                {signNum}
              </text>

              {/* House Number Indicator (Small Roman/Digit) */}
              {hNum === 1 && (
                <text
                  x="200"
                  y="75"
                  textAnchor="middle"
                  className="text-[9px] font-bold fill-amber-600 tracking-widest font-cinzel uppercase"
                >
                  LAGNA
                </text>
              )}

              {/* Planets occupying house */}
              <text
                x={data.textPos[0]}
                y={data.textPos[1]}
                textAnchor="middle"
                dominantBaseline="central"
                className="text-[11px] font-semibold fill-vedic-navy"
              >
                {occupants.map((p, idx) => {
                  const pAbbr = p.name.substring(0, 2);
                  const isRetro = p.is_retrograde ? 'Ⓡ' : '';
                  const yOffset = (idx - (occupants.length - 1) / 2) * 13;
                  return (
                    <tspan
                      key={p.name}
                      x={data.textPos[0]}
                      dy={idx === 0 ? -(occupants.length - 1) * 6.5 : 13}
                      className={
                        p.name === 'Sun' || p.name === 'Moon'
                          ? 'fill-amber-750 font-bold'
                          : p.is_combust
                          ? 'fill-red-600'
                          : 'fill-slate-800'
                      }
                    >
                      {pAbbr}
                      <tspan className="text-[9px] text-red-500 font-bold">{isRetro}</tspan>
                    </tspan>
                  );
                })}
              </text>
            </g>
          );
        })}
      </svg>
      <div className="mt-2 flex justify-between text-[11px] text-slate-500 px-1">
        <span>Click any house to inspect lordship & aspects</span>
        <span>Ⓡ = Retrograde</span>
      </div>
    </div>
  );
};
