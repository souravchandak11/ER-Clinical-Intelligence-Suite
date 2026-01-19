"use client";

import { useState } from "react";
import { api } from "@/trpc/react";
import { Loader2, FileText, Check, Copy, Mic, User, Stethoscope } from "lucide-react";

export function NoteWidget() {
    const [text, setText] = useState("");
    const [activeTab, setActiveTab] = useState<"clinical" | "patient">("clinical");
    const [isListening, setIsListening] = useState(false);
    const noteMutation = api.ai.generateNote.useMutation();

    const handleMicClick = () => {
        setIsListening(true);
        setTimeout(() => {
            setText(prev => prev + "Patient presents with acute chest pain radiating to left arm. Started 2 hours ago while gardening. Reports nausea and diaphoresis. History of hypertension.");
            setIsListening(false);
        }, 2000);
    };

    const handleGenerate = async () => {
        await noteMutation.mutateAsync({
            encounter_text: text,
            encounter_type: "Emergency"
        });
    };

    return (
        <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-100 h-full">
            <div className="flex items-center gap-2 mb-6">
                <div className="bg-indigo-100 p-2 rounded-full">
                    <FileText className="text-indigo-600 w-4 h-4" />
                </div>
                <h2 className="text-lg font-bold text-slate-800">Auto-Documentation</h2>
            </div>

            <div className="grid grid-cols-2 gap-6 h-[500px]">
                {/* Input */}
                <div className="flex flex-col gap-4">
                    <div className="relative">
                        <textarea
                            suppressHydrationWarning
                            className="w-full h-80 bg-slate-50 border border-slate-100 rounded-xl p-4 text-sm outline-none focus:ring-2 focus:ring-indigo-200 resize-none transition-all"
                            placeholder="Paste raw encounter transcript here..."
                            value={text}
                            onChange={(e) => setText(e.target.value)}
                        />
                        <button
                            onClick={handleMicClick}
                            className={`absolute bottom-4 right-4 p-3 rounded-full text-white transition-all shadow-lg ${isListening ? "bg-red-600 animate-pulse scale-110" : "bg-rose-500 hover:bg-rose-600"}`}
                        >
                            <Mic className={`w-5 h-5 ${isListening ? "animate-bounce" : ""}`} />
                        </button>
                    </div>
                    <button
                        suppressHydrationWarning
                        onClick={handleGenerate}
                        disabled={noteMutation.isPending}
                        className="w-full bg-indigo-600 text-white font-bold py-3 rounded-xl shadow-lg shadow-indigo-200 hover:bg-indigo-700 transition-all flex justify-center items-center gap-2"
                    >
                        {noteMutation.isPending ? <Loader2 className="animate-spin w-4 h-4" /> : "Generate SOAP Note"}
                    </button>
                </div>

                {/* Output */}
                <div className="bg-slate-50 border border-slate-100 rounded-xl p-4 overflow-y-auto relative group">
                    {/* Tabs */}
                    <div className="flex gap-2 mb-4 bg-white p-1 rounded-lg border border-slate-100 w-fit">
                        <button
                            onClick={() => setActiveTab("clinical")}
                            className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-xs font-bold transition-all ${activeTab === "clinical" ? "bg-indigo-100 text-indigo-700" : "text-slate-400 hover:text-slate-600"}`}
                        >
                            <Stethoscope className="w-3 h-3" /> Clinical Note
                        </button>
                        <button
                            onClick={() => setActiveTab("patient")}
                            className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-xs font-bold transition-all ${activeTab === "patient" ? "bg-indigo-100 text-indigo-700" : "text-slate-400 hover:text-slate-600"}`}
                        >
                            <User className="w-3 h-3" /> Patient Handout
                        </button>
                    </div>

                    {noteMutation.data ? (
                        activeTab === "clinical" ? (
                            <div className="space-y-4 text-sm text-slate-700">
                                <div>
                                    <h4 className="font-bold text-indigo-600 uppercase text-xs mb-1">Subjective</h4>
                                    <p>{noteMutation.data.soap_note.subjective}</p>
                                </div>
                                <div>
                                    <h4 className="font-bold text-indigo-600 uppercase text-xs mb-1">Objective</h4>
                                    <p>{noteMutation.data.soap_note.objective}</p>
                                </div>
                                <div>
                                    <h4 className="font-bold text-indigo-600 uppercase text-xs mb-1">Assessment</h4>
                                    <p>{noteMutation.data.soap_note.assessment}</p>
                                </div>
                                <div>
                                    <h4 className="font-bold text-indigo-600 uppercase text-xs mb-1">Plan</h4>
                                    <p>{noteMutation.data.soap_note.plan}</p>
                                </div>

                                {/* Codes */}
                                <div className="pt-4 border-t border-slate-200 mt-4">
                                    <div className="mb-2">
                                        <span className="text-xs font-bold text-slate-400">ICD-10: </span>
                                        {noteMutation.data.icd10?.map((c: string, i: number) => (
                                            <span key={i} className="ml-1 px-1 bg-white border border-slate-200 rounded text-xs px-2">{c}</span>
                                        ))}
                                    </div>
                                    <div>
                                        <span className="text-xs font-bold text-slate-400">CPT: </span>
                                        {noteMutation.data.cpt?.map((c: string, i: number) => (
                                            <span key={i} className="ml-1 px-1 bg-white border border-slate-200 rounded text-xs px-2">{c}</span>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        ) : (
                            <div className="h-full flex flex-col">
                                <h4 className="font-bold text-slate-800 mb-2">Patient Discharge Summary</h4>
                                <p className="text-sm text-slate-600 leading-relaxed p-4 bg-white rounded-xl border border-slate-100 shadow-sm">
                                    {noteMutation.data.patient_handout || "No patient handout generated."}
                                </p>
                            </div>
                        )
                    ) : (
                        <div className="flex flex-col items-center justify-center h-full text-slate-300">
                            <FileText className="w-12 h-12 mb-2 opacity-50" />
                            <p>Generated note will appear here</p>
                        </div>
                    )}

                    <button
                        suppressHydrationWarning
                        className="absolute top-4 right-4 p-2 bg-white rounded-lg shadow-sm opacity-0 group-hover:opacity-100 transition-all text-slate-500 hover:text-indigo-600"
                    >
                        <Copy className="w-4 h-4" />
                    </button>
                </div>
            </div>
        </div >
    );
}
