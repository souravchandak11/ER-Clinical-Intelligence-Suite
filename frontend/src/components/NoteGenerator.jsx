import React, { useState, useEffect, useCallback } from 'react';
import './NoteGenerator.css';

const NoteGenerator = () => {
    const [rawText, setRawText] = useState('');
    const [isRecording, setIsRecording] = useState(false);
    const [soapNote, setSoapNote] = useState({
        subjective: '',
        objective: '',
        assessment: '',
        plan: ''
    });
    const [isApproved, setIsApproved] = useState(false);

    // Web Speech API initialization
    const [recognition, setRecognition] = useState(null);

    useEffect(() => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRecognition) {
            const recog = new SpeechRecognition();
            recog.continuous = true;
            recog.interimResults = true;
            recog.lang = 'en-US';

            recog.onresult = (event) => {
                let interimTranscript = '';
                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    if (event.results[i].isFinal) {
                        setRawText((prev) => prev + ' ' + event.results[i][0].transcript);
                    } else {
                        interimTranscript += event.results[i][0].transcript;
                    }
                }
            };

            recog.onerror = (event) => {
                console.error('Speech recognition error', event.error);
                setIsRecording(false);
            };

            recog.onend = () => {
                setIsRecording(false);
            };

            setRecognition(recog);
        }
    }, []);

    const toggleRecording = () => {
        if (isRecording) {
            recognition?.stop();
            setIsRecording(false);
        } else {
            recognition?.start();
            setIsRecording(true);
        }
    };

    const [loading, setLoading] = useState(false);

    const generateSOAP = async () => {
        if (!rawText) return;
        setLoading(true);
        try {
            const response = await fetch(`http://localhost:8000/document/soap?notes=${encodeURIComponent(rawText)}`, {
                method: 'POST'
            });
            const data = await response.json();
            // Flatten the response so the UI can access fields directly
            setSoapNote({
                ...data.json.soap_note,
                icd10: data.json.icd10,
                cpt: data.json.cpt,
                handoff: data.json.handoff
            });
        } catch (error) {
            console.error('SOAP generation failed:', error);
            alert('Service error');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        // Debounced or manual trigger? Let's use manual for stability
    }, []);

    const copyToClipboard = () => {
        const formattedNote = `
SUBJECTIVE: ${soapNote.subjective}
OBJECTIVE: ${soapNote.objective}
ASSESSMENT: ${soapNote.assessment}
PLAN: ${soapNote.plan}
    `.trim();

        navigator.clipboard.writeText(formattedNote).then(() => {
            alert('Note copied to clipboard!');
        });
    };

    const handlePrint = () => {
        window.print();
    };

    return (
        <div className="note-generator">
            <header className="header">
                <h2>Clinical Note Generator</h2>
                <div className="controls">
                    <button
                        className={`btn btn-record ${isRecording ? 'recording' : ''}`}
                        onClick={toggleRecording}
                    >
                        {isRecording ? 'Stop Recording' : 'Start Voice Input'}
                    </button>
                    <button
                        className={`btn btn-primary ${loading ? 'loading' : ''}`}
                        onClick={generateSOAP}
                        disabled={loading}
                    >
                        {loading ? 'Processing...' : 'Generate SOAP'}
                    </button>
                    <button className="btn btn-secondary" onClick={() => setRawText('')}>
                        Clear
                    </button>
                    <button
                        className="btn btn-secondary"
                        onClick={() => setRawText("Pt is a 45yo male presenting with 2 days of worsening RLQ pain, associated with nausea and vomiting. Exam shows rebound tenderness at McBurney's point. CT scan confirms inflamed appendix. Plan for lap appy.")}
                    >
                        Load Sample
                    </button>
                </div>
            </header>

            <main className="main-content">
                <section className="input-section">
                    <label className="section-label">Unstructured Encounter Text</label>
                    <textarea
                        id="raw-input"
                        value={rawText}
                        onChange={(e) => setRawText(e.target.value)}
                        placeholder="Type or use voice input to record encounter details..."
                    />
                </section>

                <section className="preview-section">
                    <label className="section-label">Real-time SOAP Preview</label>
                    <div className="soap-preview">
                        <div className="soap-section">
                            <div className="soap-title">SUBJECTIVE</div>
                            <div className="soap-content">{soapNote.subjective || 'Waiting for input...'}</div>
                        </div>
                        <div className="soap-section">
                            <div className="soap-title">OBJECTIVE</div>
                            <div className="soap-content">{soapNote.objective || '...'}</div>
                        </div>
                        <div className="soap-section">
                            <div className="soap-title">ASSESSMENT</div>
                            <div className="soap-content">{soapNote.assessment || '...'}</div>
                        </div>
                        <div className="soap-section">
                            <div className="soap-title">PLAN</div>
                            <div className="soap-content">{soapNote.plan || '...'}</div>
                        </div>

                        {/* Billing and Handoff Section */}
                        {(soapNote.icd10 || soapNote.cpt || soapNote.handoff) && (
                            <div className="mt-8 pt-6 border-t-2 border-slate-100 grid grid-cols-2 gap-6">
                                <div>
                                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3">Billing Codes</h4>
                                    <div className="space-y-4">
                                        <div>
                                            <span className="text-xs font-semibold text-slate-500 block mb-1">ICD-10 (Diagnosis)</span>
                                            <div className="flex flex-wrap gap-2">
                                                {soapNote.icd10?.map((code, i) => (
                                                    <span key={i} className="px-2 py-1 bg-purple-50 text-purple-700 text-xs font-bold rounded border border-purple-100">{code}</span>
                                                )) || <span className="text-xs text-slate-400">None detected</span>}
                                            </div>
                                        </div>
                                        <div>
                                            <span className="text-xs font-semibold text-slate-500 block mb-1">CPT (Procedure)</span>
                                            <div className="flex flex-wrap gap-2">
                                                {soapNote.cpt?.map((code, i) => (
                                                    <span key={i} className="px-2 py-1 bg-indigo-50 text-indigo-700 text-xs font-bold rounded border border-indigo-100">{code}</span>
                                                )) || <span className="text-xs text-slate-400">None detected</span>}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div className="bg-amber-50 p-4 rounded-lg border border-amber-100">
                                    <h4 className="text-xs font-bold text-amber-700 uppercase mb-2">Shift Handoff Summary</h4>
                                    <p className="text-amber-900 text-sm italic">
                                        "{soapNote.handoff || 'No summary generated.'}"
                                    </p>
                                </div>
                            </div>
                        )}
                    </div>
                </section>
            </main>

            <footer className="footer">
                <button className="btn btn-secondary" onClick={copyToClipboard}>
                    Copy to EHR
                </button>
                <button className="btn btn-secondary" onClick={handlePrint}>
                    Save as PDF
                </button>
                <button
                    className={`btn ${isApproved ? 'btn-secondary' : 'btn-primary'}`}
                    onClick={() => setIsApproved(!isApproved)}
                >
                    {isApproved ? 'Approved' : 'Approve Note'}
                </button>
            </footer>
        </div>
    );
};

export default NoteGenerator;
