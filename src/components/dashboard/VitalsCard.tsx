"use client";
import { useState, useEffect } from "react";

import { LineChart, Line, ResponsiveContainer, YAxis } from "recharts";
import { type LucideIcon } from "lucide-react";

interface VitalsCardProps {
    title: string;
    value: number;
    unit: string;
    goal: string;
    data: { value: number }[];
    icon?: LucideIcon;
    color: string;
}

export function VitalsCard({ title, value, unit, goal, data, color }: VitalsCardProps) {
    const [mounted, setMounted] = useState(false);
    useEffect(() => {
        setMounted(true);
    }, []);

    return (
        <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-100 flex flex-col justify-between h-48 relative overflow-hidden group hover:shadow-md transition-all">
            <div className="flex justify-between items-start z-10">
                <div>
                    <h3 className="text-sm font-bold text-slate-500 mb-1">{title}</h3>
                    <p className="text-xs text-slate-400">Your Set Goal: <span className="font-bold text-slate-600">{goal}</span></p>
                </div>
                <button
                    suppressHydrationWarning
                    className="text-xs bg-slate-100 px-2 py-1 rounded-full text-slate-500 font-bold hover:bg-slate-200 transition-colors"
                >
                    Detail
                </button>
            </div>

            <div className="flex items-end justify-between z-10 mt-4">
                <div className="flex items-baseline gap-1">
                    <span className={`text-4xl font-black text-${color}-600`}>{value}</span>
                    <span className="text-sm font-bold text-slate-400">{unit}</span>
                </div>

                <div className="h-16 w-24">
                    {mounted && (
                        <ResponsiveContainer width="100%" height={64}>
                            <LineChart data={data}>
                                <Line
                                    type="monotone"
                                    dataKey="value"
                                    stroke={color === "blue" ? "#3b82f6" : "#6366f1"}
                                    strokeWidth={3}
                                    dot={false}
                                />
                                <YAxis domain={['dataMin', 'dataMax + 10']} hide />
                            </LineChart>
                        </ResponsiveContainer>
                    )}
                </div>
            </div>

            {/* Background decoration */}
            <div className={`absolute -bottom-4 -right-4 w-24 h-24 bg-${color}-50 rounded-full blur-2xl opacity-50 pointer-events-none`} />
        </div>
    );
}
