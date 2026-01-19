import React, { lazy, Suspense } from 'react'

const TriageInterface = lazy(() => import('./components/TriageInterface'))

const LoadingFallback = () => (
    <div className="flex items-center justify-center p-20">
        <div className="w-12 h-12 border-4 border-slate-200 border-t-medical-600 rounded-full animate-spin"></div>
    </div>
)

function App() {
    return (
        <div className="min-h-screen bg-slate-50">
            <header className="bg-white border-b border-slate-200 py-4 px-6 mb-8">
                <div className="max-w-7xl mx-auto flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <div className="w-8 h-8 bg-medical-600 rounded-lg flex items-center justify-center">
                            <span className="text-white font-bold text-xl">+</span>
                        </div>
                        <h1 className="text-xl font-semibold text-slate-900">ER Clinical Suite</h1>
                    </div>
                    <nav className="flex gap-4">
                        <span className="text-sm font-medium text-medical-600 border-b-2 border-medical-600 pb-1">Triage Workflow</span>
                        <span className="text-sm font-medium text-slate-500 hover:text-slate-700 cursor-not-allowed">Patient Records</span>
                    </nav>
                </div>
            </header>

            <main>
                <Suspense fallback={<LoadingFallback />}>
                    <TriageInterface />
                </Suspense>
            </main>

            <footer className="mt-12 py-8 px-6 border-t border-slate-200 bg-white text-center text-slate-500 text-sm">
                &copy; 2026 ER Clinical Intelligence Suite. HIPAA Compliant & Offline-Capable.
            </footer>
        </div>
    )
}

export default App
