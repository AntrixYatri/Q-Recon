import React from 'react';

export default function RuralRoadBackground() {
  // Tree coordinates along the landscape
  const trees = [
    // Top-left sector
    { x: 70, y: 310, size: 20, color: '#3A801C', type: 'pine' },
    { x: 110, y: 330, size: 16, color: '#99CA84', type: 'round' },
    { x: 150, y: 490, size: 22, color: '#2f6917', type: 'round' },
    { x: 220, y: 490, size: 18, color: '#99CA84', type: 'pine' },
    // Mid-left sector
    { x: 280, y: 170, size: 24, color: '#3A801C', type: 'round' },
    { x: 330, y: 150, size: 18, color: '#99CA84', type: 'round' },
    { x: 420, y: 180, size: 22, color: '#2f6917', type: 'pine' },
    // Center sector (kept subtle / away from center text)
    { x: 480, y: 340, size: 16, color: '#3A801C', type: 'round' },
    { x: 530, y: 350, size: 20, color: '#99CA84', type: 'pine' },
    { x: 670, y: 220, size: 22, color: '#2f6917', type: 'round' },
    { x: 720, y: 210, size: 18, color: '#99CA84', type: 'round' },
    // Mid-right sector
    { x: 800, y: 380, size: 24, color: '#3A801C', type: 'round' },
    { x: 860, y: 400, size: 18, color: '#99CA84', type: 'pine' },
    { x: 920, y: 130, size: 22, color: '#2f6917', type: 'round' },
    { x: 980, y: 120, size: 16, color: '#99CA84', type: 'round' },
    // Far-right sector
    { x: 1120, y: 240, size: 24, color: '#3A801C', type: 'pine' },
    { x: 1180, y: 260, size: 18, color: '#99CA84', type: 'round' },
    { x: 1240, y: 170, size: 22, color: '#2f6917', type: 'round' },
    { x: 1320, y: 190, size: 20, color: '#3A801C', type: 'pine' },
    // Bottom road sector
    { x: 180, y: 650, size: 22, color: '#3A801C', type: 'round' },
    { x: 380, y: 620, size: 18, color: '#99CA84', type: 'pine' },
    { x: 630, y: 640, size: 24, color: '#2f6917', type: 'round' },
    { x: 890, y: 610, size: 20, color: '#3A801C', type: 'round' },
    { x: 1150, y: 640, size: 22, color: '#99CA84', type: 'pine' },
    { x: 1300, y: 580, size: 18, color: '#2f6917', type: 'round' },
  ];

  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden z-0 opacity-40 dark:opacity-25 transition-opacity duration-300">
      <svg
        viewBox="0 0 1400 800"
        preserveAspectRatio="xMidYMid slice"
        className="w-full h-full"
      >
        <defs>
          {/* Reusable Curved Road Motion Paths */}
          <path
            id="roadUpper"
            d="M-80,380 C180,450 350,220 600,280 C850,340 1050,180 1480,230"
          />
          <path
            id="roadLower"
            d="M-80,600 C250,520 450,680 750,560 C1050,440 1200,600 1480,520"
          />
          {/* Headlight glow filter */}
          <radialGradient id="headlightGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#FFF200" stopOpacity="0.8" />
            <stop offset="100%" stopColor="#FFF200" stopOpacity="0" />
          </radialGradient>
        </defs>

        {/* 1. Subtle Terrain Fields */}
        <path
          d="M0,200 Q350,120 700,240 T1400,180 L1400,800 L0,800 Z"
          className="fill-emerald-50/30 dark:fill-emerald-950/10"
        />
        <path
          d="M0,450 Q400,380 800,520 T1400,420 L1400,800 L0,800 Z"
          className="fill-slate-100/40 dark:fill-slate-900/30"
        />

        {/* 2. Primary Rural Highway (Upper Curve) */}
        {/* Road Base Shoulder */}
        <use
          href="#roadUpper"
          fill="none"
          strokeWidth="32"
          className="stroke-slate-300 dark:stroke-slate-800"
          strokeLinecap="round"
        />
        {/* Road Surface Asphalt */}
        <use
          href="#roadUpper"
          fill="none"
          strokeWidth="26"
          className="stroke-slate-400/80 dark:stroke-slate-700/90"
          strokeLinecap="round"
        />
        {/* Road Center Dashed Line */}
        <use
          href="#roadUpper"
          fill="none"
          stroke="#FFF200"
          strokeWidth="2"
          strokeDasharray="8 12"
          strokeOpacity="0.7"
        />

        {/* 3. Secondary Rural Connecting Road (Lower Curve) */}
        {/* Road Base Shoulder */}
        <use
          href="#roadLower"
          fill="none"
          strokeWidth="24"
          className="stroke-slate-300 dark:stroke-slate-800"
          strokeLinecap="round"
        />
        {/* Road Surface Asphalt */}
        <use
          href="#roadLower"
          fill="none"
          strokeWidth="18"
          className="stroke-slate-400/70 dark:stroke-slate-700/80"
          strokeLinecap="round"
        />
        {/* Road Center Dashed Line */}
        <use
          href="#roadLower"
          fill="none"
          stroke="#ffffff"
          strokeWidth="1.5"
          strokeDasharray="6 10"
          strokeOpacity="0.6"
        />

        {/* 4. Natural Trees along Road Margins */}
        {trees.map((tree, i) => (
          <g key={i} transform={`translate(${tree.x}, ${tree.y})`}>
            {/* Trunk */}
            <rect
              x="-2"
              y="0"
              width="4"
              height={tree.size * 0.4}
              className="fill-amber-900/60 dark:fill-amber-950/80"
              rx="1"
            />
            {/* Canopy */}
            {tree.type === 'pine' ? (
              <polygon
                points={`0,-${tree.size} -${tree.size * 0.5},0 ${tree.size * 0.5},0`}
                fill={tree.color}
                opacity="0.85"
              />
            ) : (
              <circle
                cx="0"
                cy={-tree.size * 0.4}
                r={tree.size * 0.45}
                fill={tree.color}
                opacity="0.8"
              />
            )}
          </g>
        ))}

        {/* 5. Animated Micro Vehicles (Guaranteed 100% On-Road along exact SVG curve) */}
        
        {/* Car 1: Sky Blue Inspection SUV on upper road */}
        <g>
          {/* Vehicle Body */}
          <rect x="-13" y="-6.5" width="26" height="13" rx="2.5" fill="#53B7E8" stroke="#ffffff" strokeWidth="1" />
          {/* Windshield / Roof */}
          <rect x="-5" y="-4.5" width="9" height="9" rx="1.5" fill="#0c4a6e" opacity="0.8" />
          {/* Headlights */}
          <circle cx="11" cy="-3.5" r="1.8" fill="#FFF200" />
          <circle cx="11" cy="3.5" r="1.8" fill="#FFF200" />
          {/* Headlight beam */}
          <circle cx="15" cy="0" r="6" fill="url(#headlightGlow)" opacity="0.6" />
          <animateMotion
            dur="22s"
            repeatCount="indefinite"
            rotate="auto"
          >
            <mpath href="#roadUpper" />
          </animateMotion>
        </g>

        {/* Car 2: Green Field Van on upper road (staggered start) */}
        <g>
          <rect x="-15" y="-7" width="30" height="14" rx="2.5" fill="#3A801C" stroke="#ffffff" strokeWidth="1" />
          <rect x="-7" y="-5" width="11" height="10" rx="1.5" fill="#14532d" opacity="0.8" />
          <circle cx="13" cy="-3.5" r="1.8" fill="#FFF200" />
          <circle cx="13" cy="3.5" r="1.8" fill="#FFF200" />
          <circle cx="17" cy="0" r="6" fill="url(#headlightGlow)" opacity="0.5" />
          <animateMotion
            dur="26s"
            begin="-11s"
            repeatCount="indefinite"
            rotate="auto"
          >
            <mpath href="#roadUpper" />
          </animateMotion>
        </g>

        {/* Car 3: Yellow Road Patrol Vehicle on lower road */}
        <g>
          <rect x="-12" y="-6" width="24" height="12" rx="2.5" fill="#FFF200" stroke="#0f172a" strokeWidth="0.8" />
          <rect x="-4" y="-4" width="8" height="8" rx="1.5" fill="#713f12" opacity="0.75" />
          <circle cx="10" cy="-3" r="1.8" fill="#ffffff" />
          <circle cx="10" cy="3" r="1.8" fill="#ffffff" />
          <circle cx="14" cy="0" r="5" fill="url(#headlightGlow)" opacity="0.7" />
          <animateMotion
            dur="24s"
            begin="-4s"
            repeatCount="indefinite"
            rotate="auto"
          >
            <mpath href="#roadLower" />
          </animateMotion>
        </g>

        {/* Car 4: Light Green Transport Vehicle on lower road (staggered) */}
        <g>
          <rect x="-14" y="-6.5" width="28" height="13" rx="2.5" fill="#99CA84" stroke="#ffffff" strokeWidth="1" />
          <rect x="-6" y="-4.5" width="10" height="9" rx="1.5" fill="#1e3a1e" opacity="0.75" />
          <circle cx="12" cy="-3.5" r="1.8" fill="#FFF200" />
          <circle cx="12" cy="3.5" r="1.8" fill="#FFF200" />
          <circle cx="16" cy="0" r="5.5" fill="url(#headlightGlow)" opacity="0.5" />
          <animateMotion
            dur="29s"
            begin="-15s"
            repeatCount="indefinite"
            rotate="auto"
          >
            <mpath href="#roadLower" />
          </animateMotion>
        </g>
      </svg>
    </div>
  );
}
