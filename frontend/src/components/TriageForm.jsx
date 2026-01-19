import React, { useState } from 'react';

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

const TriageForm = () => {
    const [formData, setFormData] = useState({
        text: '',
        hr: 80,
        bp_sys: 120,
        bp_dia: 80,
        spo2: 98,
        temp: 98.6,
        rr: 16
    });
    const [image, setImage] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleFileChange = (e) => {
        setImage(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const body = new FormData();
            Object.entries(formData).forEach(([key, value]) => {
                body.append(key, value);
            });
            if (image) {
                const compressed = await compressImage(image);
                body.append('image', compressed);
            }

            const response = await fetch('http://localhost:8000/triage/multimodal', {
                method: 'POST',
                body: body
            });

            const data = await response.json();
            setResult(data);
        } catch (error) {
            console.error('Triage failed:', error);
            alert('Triage service error');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="triage-form p-6 bg-white rounded-xl shadow-lg">
            <h2 className="text-2xl font-bold mb-4 text-slate-800">Multimodal Triage</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block text-sm font-medium text-slate-600">Chief Complaint & Clinical Notes</label>
                    <textarea
                        name="text"
                        value={formData.text}
                        onChange={handleInputChange}
                        className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 h-32"
                        placeholder="Describe the patient's condition..."
                        required
                    />
                </div>

                <div className="grid grid-cols-3 gap-4">
                    <div>
                        <label className="block text-xs text-slate-500">HR (bpm)</label>
                        <input type="number" name="hr" value={formData.hr} onChange={handleInputChange} className="w-full p-2 border rounded" />
                    </div>
                    <div>
                        <label className="block text-xs text-slate-500">BP (Sys/Dia)</label>
                        <div className="flex gap-1">
                            <input type="number" name="bp_sys" value={formData.bp_sys} onChange={handleInputChange} className="w-1/2 p-2 border rounded" />
                            <input type="number" name="bp_dia" value={formData.bp_dia} onChange={handleInputChange} className="w-1/2 p-2 border rounded" />
                        </div>
                    </div>
                    <div>
                        <label className="block text-xs text-slate-500">SpO2 (%)</label>
                        <input type="number" name="spo2" value={formData.spo2} onChange={handleInputChange} className="w-full p-2 border rounded" />
                    </div>
                </div>

                <div>
                    <label className="block text-sm font-medium text-slate-600">Chest X-ray (Optional)</label>
                    <input type="file" onChange={handleFileChange} className="w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100" />
                </div>

                <div className="flex gap-2">
                    <button
                        type="button"
                        onClick={() => setFormData({
                            text: 'Severe crushing chest pain radiating to left arm. Diaphoretic and pale.',
                            hr: 135,
                            bp_sys: 180,
                            bp_dia: 110,
                            spo2: 88,
                            temp: 98.4,
                            rr: 28
                        })}
                        className="w-1/3 py-3 rounded-lg font-bold text-blue-600 bg-blue-50 hover:bg-blue-100 border border-blue-200 transition-all"
                    >
                        Load Demo Data
                    </button>
                    <button
                        type="submit"
                        disabled={loading}
                        className={`w-2/3 py-3 rounded-lg font-bold text-white transition-all ${loading ? 'bg-slate-400' : 'bg-blue-600 hover:bg-blue-700'}`}
                    >
                        {loading ? 'Analyzing with MedGemma...' : 'Run Triage Analysis'}
                    </button>
                </div>
            </form>

            {result && (
                <div className="mt-6 p-4 border-t border-slate-100 space-y-4">
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-bold uppercase text-slate-500">ESI Level Suggested</span>
                        <div className="flex items-center gap-2">
                            <span className="text-xs text-slate-400 font-mono">Confidence: {(result.clinical_json.confidence_score * 100).toFixed(0)}%</span>
                            <span className={`px-3 py-1 rounded-full text-white font-bold ${result.clinical_json.esi_level <= 2 ? 'bg-red-500' : 'bg-orange-500'}`}>
                                {result.clinical_json.esi_level}
                            </span>
                        </div>
                    </div>

                    <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
                        <h4 className="text-xs font-bold text-slate-500 uppercase mb-2">Patient Explanation</h4>
                        <p className="text-slate-700 text-sm font-medium">{result.patient_explanation}</p>
                    </div>

                    {result.clinical_json.red_flag_conditions.length > 0 && (
                        <div className="bg-red-50 p-4 rounded-lg border border-red-100">
                            <h4 className="text-xs font-bold text-red-600 uppercase mb-2 flex items-center gap-2">
                                <span className="text-lg">⚠️</span> Red Flags Detected
                            </h4>
                            <ul className="list-disc list-inside text-sm text-red-700 space-y-1">
                                {result.clinical_json.red_flag_conditions.map((flag, i) => <li key={i}>{flag}</li>)}
                            </ul>
                        </div>
                    )}

                    <div className="grid grid-cols-2 gap-4">
                        <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">
                            <h4 className="text-xs font-bold text-blue-700 uppercase mb-2">Adaptive Questions</h4>
                            <ul className="list-disc list-inside text-sm text-blue-800 space-y-1">
                                {result.clinical_json.follow_up_questions?.map((q, i) => <li key={i}>{q}</li>) || <li className="text-slate-400 italic">No specific follow-up needed.</li>}
                            </ul>
                        </div>

                        <div className="bg-green-50 p-4 rounded-lg border border-green-100">
                            <h4 className="text-xs font-bold text-green-700 uppercase mb-2">Recommended Next Steps</h4>
                            <ul className="list-disc list-inside text-sm text-green-800 space-y-1">
                                {/* This field was missing in the frontend mapping, adding fallback */}
                                {(result.clinical_json.recommended_next_steps || ['Review vitals', 'Physician assessment']).map((step, i) => <li key={i}>{step}</li>)}
                            </ul>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default TriageForm;
