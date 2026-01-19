import { Calendar, MoreHorizontal } from "lucide-react";

interface Appointment {
    id: string;
    doctorName: string;
    specialty: string;
    date: Date;
    active?: boolean;
}

export function ScheduleList({ appointments }: { appointments: Appointment[] }) {
    // Calendar days mock
    const days = Array.from({ length: 7 }, (_, i) => i + 12);
    const activeDay = 15;

    return (
        <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-100 h-full">
            <div className="flex justify-between items-center mb-6">
                <div className="flex items-center gap-2">
                    <div className="bg-blue-50 p-2 rounded-full">
                        <Calendar className="text-blue-600 w-4 h-4" />
                    </div>
                    <h2 className="text-lg font-bold text-slate-800">Schedule</h2>
                </div>
                <div className="flex gap-2">
                    <button suppressHydrationWarning className="p-2 hover:bg-slate-50 rounded-full"><Calendar size={16} className="text-slate-400" /></button>
                    <button suppressHydrationWarning className="p-2 hover:bg-slate-50 rounded-full"><MoreHorizontal size={16} className="text-slate-400" /></button>
                </div>
            </div>

            {/* Date Strip */}
            <div className="flex justify-between mb-8">
                {days.map(d => (
                    <div key={d} className={`flex flex-col items-center justify-center w-10 h-16 rounded-full ${d === activeDay ? 'bg-blue-600 text-white shadow-lg shadow-blue-200' : 'bg-slate-50 text-slate-300'}`}>
                        <span className="text-[10px] font-bold"></span>
                        <span className="text-sm font-bold">{d}</span>
                    </div>
                ))}
            </div>

            <div className="space-y-4">
                {appointments.map((appt) => (
                    <div key={appt.id} className="flex items-center justify-between p-4 bg-white border border-slate-50 rounded-2xl hover:shadow-md transition-shadow">
                        <div className="flex items-center gap-4">
                            <div className="w-10 h-10 rounded-full bg-slate-200 overflow-hidden">
                                {/* Avatar placeholder */}
                                <div className="w-full h-full bg-gradient-to-br from-blue-100 to-indigo-100 flex items-center justify-center text-xs font-bold text-blue-500">
                                    {appt.doctorName[0]}
                                </div>
                            </div>
                            <div>
                                <h4 className="font-bold text-sm text-slate-800">{appt.doctorName}</h4>
                                <p className="text-xs text-slate-400">{appt.specialty}</p>
                            </div>
                        </div>
                        <button suppressHydrationWarning className="text-slate-300 hover:text-slate-500">•••</button>
                    </div>
                ))}
            </div>
        </div>
    );
}
