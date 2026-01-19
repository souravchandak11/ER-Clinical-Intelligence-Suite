import { LayoutGrid, Calendar, MessageSquare, Settings, LogOut, Activity } from "lucide-react";

export function Sidebar() {
    return (
        <aside className="fixed left-0 top-0 h-screen w-20 bg-white border-r border-slate-100 flex flex-col items-center py-8 z-50">
            <div className="mb-12">
                <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-200">
                    <Activity className="text-white w-6 h-6" />
                </div>
            </div>

            <nav className="flex-1 flex flex-col gap-6 w-full items-center">
                <NavItem icon={LayoutGrid} active />
                <NavItem icon={Calendar} />
                <NavItem icon={MessageSquare} />
                <NavItem icon={Settings} />
            </nav>

            <button suppressHydrationWarning className="p-3 text-slate-300 hover:text-red-500 transition-colors">
                <LogOut className="w-5 h-5" />
            </button>
        </aside>
    );
}

function NavItem({ icon: Icon, active }: { icon: any, active?: boolean }) {
    return (
        <button suppressHydrationWarning className={`p-3 rounded-2xl transition-all ${active ? 'bg-blue-600 text-white shadow-lg shadow-blue-200' : 'text-slate-400 hover:bg-slate-50 hover:text-slate-600'}`}>
            <Icon className="w-5 h-5" />
        </button>
    )
}
