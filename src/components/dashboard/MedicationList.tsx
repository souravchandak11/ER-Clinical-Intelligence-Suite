import { Pill, Zap, Heart, Brain } from "lucide-react";

interface Medication {
    id: string;
    name: string;
    dosage: string;
    schedule: string;
    active: boolean;
}

const ICONS: Record<string, any> = {
    "Neuro": Brain,
    "Heart": Heart,
    "Hydration": Pill,
    "Energy": Zap,
    "default": Pill
};

export function MedicationList({ medications }: { medications: Medication[] }) {
    return (
        <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-100 h-full">
            <div className="flex justify-between items-center mb-6">
                <div className="flex items-center gap-2">
                    <div className="bg-blue-100 p-2 rounded-full">
                        <Pill className="text-blue-600 w-4 h-4" />
                    </div>
                    <h2 className="text-lg font-bold text-slate-800">Medication List</h2>
                </div>
                <button suppressHydrationWarning className="text-slate-400 hover:text-slate-600">
                    <span className="sr-only">More</span>
                    •••
                </button>
            </div>

            <div className="space-y-4">
                {medications.map((med) => {
                    // Determine icon logic based on name roughly
                    const Icon = Object.entries(ICONS).find(([k]) => med.name.includes(k))?.[1] || ICONS.default;

                    return (
                        <div
                            key={med.id}
                            suppressHydrationWarning
                            className={`flex items-center p-4 rounded-2xl transition-all cursor-pointer ${med.active
                                ? "bg-blue-600 text-white shadow-lg shadow-blue-200"
                                : "bg-white hover:bg-slate-50 border border-slate-50"
                                }`}
                        >
                            <div className={`p-3 rounded-full mr-4 ${med.active ? "bg-white/20" : "bg-orange-100"}`}>
                                <Icon className={`w-5 h-5 ${med.active ? "text-white" : "text-orange-500"}`} />
                            </div>
                            <div>
                                <h4 className={`font-bold text-sm ${med.active ? "text-white" : "text-slate-700"}`}>{med.name}</h4>
                                <p className={`text-xs ${med.active ? "text-blue-200" : "text-slate-400"}`}>{med.dosage} • {med.schedule}</p>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
