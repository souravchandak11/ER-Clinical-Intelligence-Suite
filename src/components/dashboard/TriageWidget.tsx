"use client";

import { useState } from "react";
import { api } from "@/trpc/react";
import { Loader2, AlertTriangle, CheckCircle, Activity } from "lucide-react";

export function TriageWidget() {
    const [complaint, setComplaint] = useState("");
    const [vitals, setVitals] = useState({
        hr: 70,
        bp: "120/80",
        spo2: 98,
        temp: 98.6,
        rr: 16
    });
    const [image, setImage] = useState<string | null>(null);

    const utils = api.useUtils();
    const triageMutation = api.ai.triage.useMutation();

    const handleSubmit = async () => {
        try {
            await triageMutation.mutateAsync({
                chief_complaint: complaint,
                vitals: vitals,
                image_base64: image
            });
        } catch (e) {
            console.error(e);
        }
    };

    const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setImage(reader.result as string);
            };
            reader.readAsDataURL(file);
        }
    };

    return (
        <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-100">
            <div className="flex items-center gap-2 mb-6">
                <div className="bg-rose-100 p-2 rounded-full">
                    <Activity className="text-rose-600 w-4 h-4" />
                </div>
                <h2 className="text-lg font-bold text-slate-800">AI Triage Assistant</h2>
            </div>

            <div className="space-y-4">
                <div>
                    <label htmlFor="chief-complaint" className="block text-xs font-bold text-slate-400 mb-1 uppercase">Chief Complaint</label>
                    <textarea
                        id="chief-complaint"
                        suppressHydrationWarning
                        className="w-full bg-slate-50 border border-slate-100 rounded-xl p-3 text-sm outline-none focus:ring-2 focus:ring-rose-200 transition-all"
                        rows={3}
                        placeholder="Describe patient symptoms..."
                        value={complaint}
                        onChange={(e) => setComplaint(e.target.value)}
                    />
                    <div className="mt-2">
                        <label htmlFor="image-upload" className="block text-xs font-bold text-slate-400 mb-1 uppercase">Attach Photo (X-Ray/Wound)</label>
                        <input
                            id="image-upload"
                            type="file"
                            accept="image/*"
                            onChange={handleImageUpload}
                            className="w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-xs file:font-semibold file:bg-rose-50 file:text-rose-700 hover:file:bg-rose-100"
                        />
                        {image && <p className="text-xs text-green-600 mt-1 flex items-center gap-1"><CheckCircle className="w-3 h-3" /> Image attached</p>}
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                    {Object.entries(vitals).map(([key, val]) => (
                        <div key={key}>
                            <label htmlFor={`vital-${key}`} className="block text-xs font-bold text-slate-400 mb-1 uppercase">{key}</label>
                            <input
                                id={`vital-${key}`}
                                suppressHydrationWarning
                                className="w-full bg-slate-50 border border-slate-100 rounded-xl p-2 text-sm outline-none focus:ring-2 focus:ring-blue-200"
                                value={val}
                                onChange={(e) => setVitals({ ...vitals, [key]: key === 'bp' ? e.target.value : Number(e.target.value) })}
                            />
                        </div>
                    ))}
                </div>

                <button
                    id="run-triage-btn"
                    suppressHydrationWarning
                    onClick={handleSubmit}
                    disabled={triageMutation.isPending}
                    className="w-full bg-rose-600 text-white font-bold py-3 rounded-xl shadow-lg shadow-rose-200 hover:bg-rose-700 transition-all flex justify-center items-center gap-2"
                >
                    {triageMutation.isPending ? <Loader2 className="animate-spin w-4 h-4" /> : "Run Triage Analysis"}
                </button>

                {/* Results */}
                {triageMutation.data && (
                    <div className="mt-6 animate-in fade-in slide-in-from-bottom-4">
                        <div className={`p-4 rounded-xl border-l-4 mb-4 ${triageMutation.data.esi_level === 1 ? "bg-red-50 border-red-500" :
                            triageMutation.data.esi_level === 2 ? "bg-orange-50 border-orange-500" :
                                "bg-green-50 border-green-500"
                            }`}>
                            <div className="flex justify-between items-center mb-2">
                                <h3 className="font-bold text-slate-800">ESI Level {triageMutation.data.esi_level}</h3>
                                <span className="text-xs font-bold px-2 py-1 bg-white rounded border border-slate-100">
                                    Confidence: {(triageMutation.data.confidence * 100).toFixed(0)}%
                                </span>
                            </div>
                            <p className="text-sm text-slate-600 mb-2">{triageMutation.data.reasoning}</p>

                            {/* Red Flags */}
                            {triageMutation.data.red_flags.length > 0 && (
                                <div className="flex gap-2 flex-wrap mt-2">
                                    {triageMutation.data.red_flags.map((flag: string, i: number) => (
                                        <span key={i} className="text-xs font-bold text-red-600 bg-red-100 px-2 py-1 rounded flex items-center gap-1">
                                            <AlertTriangle className="w-3 h-3" /> {flag}
                                        </span>
                                    ))}
                                </div>
                            )}
                        </div>

                        {/* Adaptive Questions */}
                        {triageMutation.data.follow_up_questions?.length > 0 && (
                            <div className="bg-indigo-50 p-4 rounded-xl mb-4 border border-indigo-100">
                                <h4 className="text-xs font-bold text-indigo-600 uppercase mb-2">Recommended Follow-up Questions</h4>
                                <ul className="space-y-2">
                                    {triageMutation.data.follow_up_questions.map((q: string, i: number) => (
                                        <li key={i} className="text-sm text-slate-700 flex items-start gap-2">
                                            <span className="bg-indigo-200 text-indigo-700 w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">{i + 1}</span>
                                            {q}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}

                        <div className="bg-slate-50 p-4 rounded-xl">
                            <h4 className="text-xs font-bold text-slate-400 uppercase mb-2">Patient Explanation</h4>
                            <p className="text-sm text-slate-600 italic">"{triageMutation.data.patient_explanation}"</p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
