interface HeartModelProps {
    heartRate: number;
    history: { value: number }[];
}

export function HeartModel({ heartRate, history }: HeartModelProps) {
    return (
        <div className="relative w-full h-[600px] flex flex-col items-center justify-between py-4">
            {/* 3D Model Display */}
            <div className="relative flex-1 w-full flex items-center justify-center">
                <div className="relative w-[500px] h-[500px]">
                    <img
                        src="/images/heart.png"
                        alt="3D Heart Model"
                        className="w-full h-full object-contain filter drop-shadow-[0_25px_25px_rgba(244,63,94,0.2)]"
                    />

                    {/* Anatomical Information Hotspots (As seen in reference) */}
                    <div className="absolute top-[40%] right-[35%]">
                        <div className="w-5 h-5 bg-white rounded-full shadow-lg border-[3px] border-white flex items-center justify-center animate-pulse">
                            <div className="w-2 h-2 bg-slate-300 rounded-full"></div>
                        </div>
                    </div>
                    <div className="absolute top-[55%] left-[30%]">
                        <div className="w-5 h-5 bg-white rounded-full shadow-lg border-[3px] border-white flex items-center justify-center">
                            <div className="w-2 h-2 bg-slate-300 rounded-full"></div>
                        </div>
                    </div>
                    <div className="absolute bottom-[25%] left-[35%]">
                        <div className="w-5 h-5 bg-white rounded-full shadow-lg border-[3px] border-white flex items-center justify-center">
                            <div className="w-2 h-2 bg-slate-200 rounded-full"></div>
                        </div>
                    </div>

                    {/* Heart Rate Glass Card Overlay */}
                    <div className="absolute right-[5%] bottom-[15%] bg-white/40 backdrop-blur-xl p-5 rounded-[2.5rem] shadow-[0_20px_50px_rgba(0,0,0,0.1)] border border-white/60 w-60 transform hover:scale-105 transition-all duration-500 ease-out cursor-default">
                        <div className="flex justify-between items-center mb-4">
                            <div className="flex items-center gap-3">
                                <div className="bg-rose-500 p-1.5 rounded-lg shadow-rose-200 shadow-lg animate-pulse">
                                    <svg className="w-3 h-3 text-white fill-current" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" /></svg>
                                </div>
                                <span className="text-[13px] font-bold text-slate-800 tracking-tight">Heart Rate</span>
                            </div>
                            <button className="text-slate-400 hover:text-slate-600 transition-colors">
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"></path></svg>
                            </button>
                        </div>
                        <div className="flex items-baseline gap-2 mb-4">
                            <span className="text-sm font-bold text-slate-400 uppercase tracking-widest">BPM</span>
                            <span className="text-4xl font-black text-slate-900 tabular-nums tracking-tighter">{heartRate}</span>
                        </div>
                        {/* Smooth Sparkline */}
                        <div className="h-16 w-full bg-blue-50/30 rounded-2xl flex items-end px-1 overflow-hidden group">
                            <svg viewBox="0 0 100 20" preserveAspectRatio="none" className="w-full h-full stroke-blue-500 fill-none stroke-[2.5] opacity-80 group-hover:opacity-100 transition-opacity">
                                <path
                                    d={`M ${history.map((d, i) => `${(i / (history.length - 1)) * 100},${20 - ((d.value - 60) / 70) * 20}`).join(' L ')}`}
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                />
                            </svg>
                        </div>
                    </div>
                </div>
            </div>

            {/* Organ Selectors - Premium Bottom Bar */}
            <div className="flex gap-6 px-8 py-4 bg-white/20 backdrop-blur-md rounded-[2.5rem] border border-white/40 shadow-xl mb-4">
                <div className="w-20 h-20 rounded-[1.8rem] bg-white flex items-center justify-center shadow-lg hover:shadow-2xl hover:-translate-y-2 transition-all duration-300 cursor-pointer group border-2 border-transparent">
                    <img src="/images/brain.png" alt="Brain" className="w-14 h-14 object-contain opacity-50 group-hover:opacity-100 transition-all duration-300" />
                </div>
                <div className="w-20 h-20 rounded-[1.8rem] bg-white flex items-center justify-center shadow-2xl scale-110 border-2 border-blue-500/30 transition-all duration-300 cursor-pointer">
                    <img src="/images/heart.png" alt="Heart" className="w-14 h-14 object-contain" />
                </div>
                <div className="w-20 h-20 rounded-[1.8rem] bg-white flex items-center justify-center shadow-lg hover:shadow-2xl hover:-translate-y-2 transition-all duration-300 cursor-pointer group border-2 border-transparent">
                    <img src="/images/lungs.png" alt="Lungs" className="w-14 h-14 object-contain opacity-50 group-hover:opacity-100 transition-all duration-300" />
                </div>
            </div>
        </div>
    );
}
