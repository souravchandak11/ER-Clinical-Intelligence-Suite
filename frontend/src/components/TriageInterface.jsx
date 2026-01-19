import React, { useState, useRef, useEffect } from 'react';
import {
    Activity,
    Thermometer,
    Heart,
    Wind,
    Droplets,
    Upload,
    Camera,
    AlertTriangle,
    CheckCircle,
    ChevronRight,
    Info,
    Loader2,
    X,
    FileText
} from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Image compression utility
 */
const compressImage = (file, maxWidth = 800, quality = 0.7) => {
    return new Promise((resolve) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = (event) => {
            const img = new Image();
            img.src = event.target.result;
            img.onload = () => {
                const canvas = document.createElement('canvas');
                let width = img.width;
                let height = img.height;

                if (width > maxWidth) {
                    height = (maxWidth / width) * height;
                    width = maxWidth;
                }

                canvas.width = width;
                canvas.height = height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, width, height);

                canvas.toBlob((blob) => {
                    resolve(new File([blob], file.name, { type: 'image/jpeg' }));
                }, 'image/jpeg', quality);
            };
        };
    });
};

/**
 * TriageInterface Component
 * High-fidelity, medical-grade UI for ER patient triage.
 */
export default function TriageInterface() {
    // --- State ---
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [analysis, setAnalysis] = useState(null);

    // Form State
    const [chiefComplaint, setChiefComplaint] = useState('');
    const [vitals, setVitals] = useState({
        heartRate: '',
        bloodPressureSys: '',
        bloodPressureDia: '',
        spO2: '',
        temperature: '',
        respiratoryRate: ''
    });
    const [image, setImage] = useState(null);
    const [imagePreview, setImagePreview] = useState(null);

    // --- Handlers ---
    const handleVitalChange = (e) => {
        const { name, value } = e.target;
        setVitals(prev => ({ ...prev, [name]: value }));
    };

    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            setImage(file);
            const reader = new FileReader();
            reader.onloadend = () => {
                setImagePreview(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleRemoveImage = () => {
        setImage(null);
        setImagePreview(null);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        // Create FormData and map fields to backend expected format
        try {
            const body = new FormData();
            body.append('text', chiefComplaint);
            body.append('hr', vitals.heartRate || 80);
            body.append('bp_sys', vitals.bloodPressureSys || 120);
            body.append('bp_dia', vitals.bloodPressureDia || 80);
            body.append('spo2', vitals.spO2 || 98);
            body.append('temp', vitals.temperature || 98.6);
            body.append('rr', vitals.respiratoryRate || 16);

            if (image) {
                const compressed = await compressImage(image);
                body.append('image', compressed);
            }

            const response = await fetch('http://localhost:8000/triage/multimodal', {
                method: 'POST',
                body: body
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Analysis failed');
            }

            const data = await response.json();

            // Map backend response to interface state
            // backend returns: { clinical_json: { esi_level: 2, ... }, patient_text: "..." }
            setAnalysis({
                urgencyLevel: data.clinical_json.esi_level,
                urgencyLabel: `Level ${data.clinical_json.esi_level}: ${data.clinical_json.esi_level <= 2 ? 'Emergent' : 'Urgent'}`,
                confidence: data.clinical_json.confidence_score,
                redFlags: data.clinical_json.red_flag_conditions,
                summary: data.patient_text,
                followUpQuestions: data.clinical_json.suggested_follow_up
            });
        } catch (err) {
            setError(err.message || 'Analysis failed. Please check backend connection.');
        } finally {
            setLoading(false);
        }
    };

    const resetForm = () => {
        setChiefComplaint('');
        setVitals({
            heartRate: '',
            bloodPressureSys: '',
            bloodPressureDia: '',
            spO2: '',
            temperature: '',
            respiratoryRate: ''
        });
        setImage(null);
        setImagePreview(null);
        setAnalysis(null);
    };

    // --- Helpers ---
    const getUrgencyColor = (level) => {
        const colors = {
            1: 'bg-red-500 text-white',
            2: 'bg-orange-500 text-white',
            3: 'bg-yellow-500 text-slate-900',
            4: 'bg-green-500 text-white',
            5: 'bg-blue-500 text-white'
        };
        return colors[level] || 'bg-slate-500 text-white';
    };

    const cn = (...inputs) => twMerge(clsx(inputs));

    return (
        <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">

            {/* --- Left Column: Input Form --- */}
            <div className="lg:col-span-7 space-y-6">
                <section className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
                    <div className="px-6 py-4 border-b border-slate-100 bg-slate-50/50 flex items-center gap-2">
                        <Activity className="w-5 h-5 text-medical-600" />
                        <h2 className="font-semibold text-slate-800">Triage Assessment</h2>
                    </div>

                    <form onSubmit={handleSubmit} className="p-6 space-y-8">
                        {/* Chief Complaint */}
                        <div className="space-y-3">
                            <label htmlFor="chiefComplaint" className="block text-sm font-medium text-slate-700">
                                Chief Complaint <span className="text-red-500">*</span>
                            </label>
                            <textarea
                                id="chiefComplaint"
                                rows={4}
                                className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-medical-500 focus:border-medical-500 outline-none transition-all placeholder:text-slate-400"
                                placeholder="Describe current symptoms and reason for visit..."
                                value={chiefComplaint}
                                onChange={(e) => setChiefComplaint(e.target.value)}
                                required
                            />
                        </div>

                        {/* Vitals Grid */}
                        <div className="space-y-4">
                            <label className="block text-sm font-medium text-slate-700">Patient Vital Signs</label>
                            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                                {/* Temp */}
                                <div className="space-y-1.5">
                                    <div className="flex items-center gap-1.5 text-xs text-slate-500 mb-1">
                                        <Thermometer className="w-3.5 h-3.5" />
                                        <span>Temp (°C)</span>
                                    </div>
                                    <input
                                        type="number"
                                        step="0.1"
                                        name="temperature"
                                        value={vitals.temperature}
                                        onChange={handleVitalChange}
                                        className="w-full px-3 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-medical-500 outline-none"
                                        placeholder="37.0"
                                    />
                                </div>
                                {/* Heart Rate */}
                                <div className="space-y-1.5">
                                    <div className="flex items-center gap-1.5 text-xs text-slate-500 mb-1">
                                        <Heart className="w-3.5 h-3.5" />
                                        <span>HR (BPM)</span>
                                    </div>
                                    <input
                                        type="number"
                                        name="heartRate"
                                        value={vitals.heartRate}
                                        onChange={handleVitalChange}
                                        className="w-full px-3 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-medical-500 outline-none"
                                        placeholder="75"
                                    />
                                </div>
                                {/* BP Sys */}
                                <div className="space-y-1.5">
                                    <div className="flex items-center gap-1.5 text-xs text-slate-500 mb-1">
                                        <Activity className="w-3.5 h-3.5" />
                                        <span>BP Sys</span>
                                    </div>
                                    <input
                                        type="number"
                                        name="bloodPressureSys"
                                        value={vitals.bloodPressureSys}
                                        onChange={handleVitalChange}
                                        className="w-full px-3 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-medical-500 outline-none"
                                        placeholder="120"
                                    />
                                </div>
                                {/* BP Dia */}
                                <div className="space-y-1.5">
                                    <div className="flex items-center gap-1.5 text-xs text-slate-500 mb-1">
                                        <Activity className="w-3.5 h-3.5" />
                                        <span>BP Dia</span>
                                    </div>
                                    <input
                                        type="number"
                                        name="bloodPressureDia"
                                        value={vitals.bloodPressureDia}
                                        onChange={handleVitalChange}
                                        className="w-full px-3 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-medical-500 outline-none"
                                        placeholder="80"
                                    />
                                </div>
                                {/* SpO2 */}
                                <div className="space-y-1.5">
                                    <div className="flex items-center gap-1.5 text-xs text-slate-500 mb-1">
                                        <Droplets className="w-3.5 h-3.5" />
                                        <span>SpO2 (%)</span>
                                    </div>
                                    <input
                                        type="number"
                                        name="spO2"
                                        value={vitals.spO2}
                                        onChange={handleVitalChange}
                                        className="w-full px-3 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-medical-500 outline-none"
                                        placeholder="98"
                                    />
                                </div>
                                {/* Resp Rate */}
                                <div className="space-y-1.5">
                                    <div className="flex items-center gap-1.5 text-xs text-slate-500 mb-1">
                                        <Wind className="w-3.5 h-3.5" />
                                        <span>Resp Rate</span>
                                    </div>
                                    <input
                                        type="number"
                                        name="respiratoryRate"
                                        value={vitals.respiratoryRate}
                                        onChange={handleVitalChange}
                                        className="w-full px-3 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-medical-500 outline-none"
                                        placeholder="16"
                                    />
                                </div>
                            </div>
                        </div>

                        {/* Multimodal Upload */}
                        <div className="space-y-3">
                            <label className="block text-sm font-medium text-slate-700">Attachments (Optional)</label>
                            <div
                                className={cn(
                                    "border-2 border-dashed rounded-2xl p-8 flex flex-col items-center justify-center transition-all cursor-pointer",
                                    imagePreview ? "border-medical-500 bg-medical-50/30" : "border-slate-200 hover:border-medical-400 hover:bg-slate-50/50"
                                )}
                                onClick={() => document.getElementById('image-upload').click()}
                            >
                                {imagePreview ? (
                                    <div className="relative group w-full max-w-xs">
                                        <img src={imagePreview} alt="Preview" className="w-full h-40 object-cover rounded-xl shadow-md" />
                                        <button
                                            type="button"
                                            onClick={(e) => { e.stopPropagation(); handleRemoveImage(); }}
                                            className="absolute -top-2 -right-2 bg-red-500 text-white p-1.5 rounded-full shadow-lg opacity-0 group-hover:opacity-100 transition-opacity"
                                        >
                                            <X className="w-4 h-4" />
                                        </button>
                                        <div className="mt-2 text-center text-xs text-slate-500 truncate">{image.name}</div>
                                    </div>
                                ) : (
                                    <>
                                        <div className="w-12 h-12 bg-slate-100 rounded-full flex items-center justify-center mb-4">
                                            <Upload className="w-6 h-6 text-slate-400" />
                                        </div>
                                        <div className="text-sm font-medium text-slate-900 text-center">Drag and drop files here, or click to upload</div>
                                        <div className="text-xs text-slate-500 mt-1">Supports PNG, JPG (X-rays, injury photos) or Take Photo</div>
                                        <div className="mt-4 flex gap-3">
                                            <button
                                                type="button"
                                                className="flex items-center gap-2 px-4 py-1.5 text-xs font-semibold bg-white border border-slate-200 rounded-lg shadow-sm hover:bg-slate-50 transition-colors"
                                            >
                                                <Camera className="w-3.5 h-3.5" />
                                                Capture
                                            </button>
                                        </div>
                                    </>
                                )}
                                <input
                                    id="image-upload"
                                    type="file"
                                    accept="image/*"
                                    className="hidden"
                                    onChange={handleImageUpload}
                                />
                            </div>
                        </div>

                        {/* Submit Button */}
                        <div className="pt-4 flex gap-4">
                            <button
                                type="submit"
                                disabled={loading || !chiefComplaint}
                                className="flex-1 bg-medical-600 text-white font-bold py-3 px-6 rounded-xl shadow-lg shadow-medical-500/20 hover:bg-medical-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2"
                            >
                                {loading ? (
                                    <>
                                        <Loader2 className="w-5 h-5 animate-spin" />
                                        <span>Analyzing with MedGemma...</span>
                                    </>
                                ) : (
                                    <>
                                        <span>Perform Triage Analysis</span>
                                        <ChevronRight className="w-5 h-5" />
                                    </>
                                )}
                            </button>

                            <button
                                type="button"
                                onClick={resetForm}
                                className="px-6 py-3 border border-slate-200 rounded-xl hover:bg-slate-50 transition-colors text-slate-600 font-medium"
                            >
                                Clear
                            </button>
                        </div>
                    </form>
                </section>

                {error && (
                    <div className="bg-red-50 border border-red-200 p-4 rounded-xl flex items-center gap-3 text-red-700 animate-in fade-in slide-in-from-top-2">
                        <AlertTriangle className="w-5 h-5 flex-shrink-0" />
                        <p className="text-sm font-medium">{error}</p>
                    </div>
                )}
            </div>

            {/* --- Right Column: Analysis Display --- */}
            <div className="lg:col-span-5 space-y-6">
                {!analysis && !loading && (
                    <div className="bg-white rounded-2xl border border-slate-200 p-12 flex flex-col items-center justify-center text-center space-y-4 opacity-70">
                        <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center">
                            <Activity className="w-8 h-8 text-slate-300" />
                        </div>
                        <div>
                            <h3 className="text-lg font-semibold text-slate-700">Waiting for Data</h3>
                            <p className="text-sm text-slate-500 mt-1 max-w-xs mx-auto">
                                Enter chief complaint and patient vitals to receive real-time AI-powered triage analysis.
                            </p>
                        </div>
                    </div>
                )}

                {loading && !analysis && (
                    <div className="bg-white rounded-2xl border border-slate-200 p-12 flex flex-col items-center justify-center text-center space-y-6">
                        <div className="relative">
                            <div className="w-16 h-16 border-4 border-slate-100 border-t-medical-600 rounded-full animate-spin"></div>
                            <div className="absolute inset-0 flex items-center justify-center">
                                <Activity className="w-6 h-6 text-medical-600" />
                            </div>
                        </div>
                        <div>
                            <h3 className="text-lg font-semibold text-slate-800">Processing Clinical Input</h3>
                            <p className="text-sm text-slate-500 mt-2">
                                MedGemma is analyzing chief complaint, vitals, and multimodal data for ESI urgency scoring...
                            </p>
                        </div>
                    </div>
                )}

                {analysis && (
                    <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
                        {/* Urgency Highlight */}
                        <div className={cn(
                            "rounded-2xl p-6 shadow-sm border-l-8 flex flex-col gap-4 bg-white",
                            analysis.urgencyLevel === 1 ? "border-red-500" :
                                analysis.urgencyLevel === 2 ? "border-orange-500" :
                                    analysis.urgencyLevel === 3 ? "border-yellow-500" :
                                        analysis.urgencyLevel === 4 ? "border-green-500" : "border-blue-500"
                        )}>
                            <div className="flex items-center justify-between">
                                <div>
                                    <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Suggested Urgency</span>
                                    <h3 className="text-2xl font-extrabold text-slate-900 mt-1">{analysis.urgencyLabel}</h3>
                                </div>
                                <div className={cn("px-4 py-2 rounded-xl text-sm font-bold shadow-md", getUrgencyColor(analysis.urgencyLevel))}>
                                    ESI {analysis.urgencyLevel}
                                </div>
                            </div>
                            <div className="flex items-center gap-2">
                                <div className="flex-1 h-3 bg-slate-100 rounded-full overflow-hidden">
                                    <div
                                        className="h-full bg-medical-500 transition-all duration-1000"
                                        style={{ width: `${analysis.confidence * 100}%` }}
                                    />
                                </div>
                                <span className="text-xs font-semibold text-slate-600">{Math.round(analysis.confidence * 100)}% Confidence</span>
                            </div>
                        </div>

                        {/* Red Flags */}
                        <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
                            <div className="px-6 py-4 border-b border-slate-100 flex items-center gap-2 bg-red-50/50">
                                <AlertTriangle className="w-4 h-4 text-red-600" />
                                <h3 className="font-semibold text-slate-800 text-sm">Key Clinical Red Flags</h3>
                            </div>
                            <div className="p-6 space-y-3">
                                {analysis.redFlags.map((flag, idx) => (
                                    <div key={idx} className="flex items-start gap-3 group">
                                        <div className="w-1.5 h-1.5 rounded-full bg-red-400 mt-1.5 flex-shrink-0 group-hover:scale-125 transition-transform" />
                                        <p className="text-sm text-slate-700 leading-tight">{flag}</p>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* AI Summary / Patient-Friendly */}
                        <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
                            <div className="px-6 py-4 border-b border-slate-100 flex items-center gap-2 bg-medical-50/50">
                                <FileText className="w-4 h-4 text-medical-600" />
                                <h3 className="font-semibold text-slate-800 text-sm">Patient Summary Preview</h3>
                            </div>
                            <div className="p-6">
                                <p className="text-sm text-slate-700 leading-relaxed italic">
                                    "{analysis.summary}"
                                </p>
                                <div className="mt-4 flex items-center gap-2 text-xs text-medical-600 font-medium">
                                    <Info className="w-3.5 h-3.5" />
                                    <span>Explain clinical reasoning to patient</span>
                                </div>
                            </div>
                        </div>

                        {/* Follow-up Questions */}
                        <div className="bg-medical-900 rounded-2xl p-6 text-white shadow-xl shadow-medical-900/20">
                            <div className="flex items-center gap-2 mb-4">
                                <CheckCircle className="w-4 h-4 text-medical-400" />
                                <h3 className="font-semibold text-sm">Suggested Follow-up Questions</h3>
                            </div>
                            <div className="space-y-4">
                                {analysis.followUpQuestions.map((q, idx) => (
                                    <button
                                        key={idx}
                                        className="w-full text-left p-3 rounded-xl border border-medical-800 bg-white/5 hover:bg-white/10 transition-colors flex items-center justify-between group"
                                    >
                                        <span className="text-sm text-medical-100 leading-snug">{q}</span>
                                        <ChevronRight className="w-4 h-4 text-medical-500 group-hover:translate-x-1 transition-transform" />
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
