import { api } from "@/trpc/server";
import { Sidebar } from "@/components/layout/Sidebar";
import { VitalsCard } from "@/components/dashboard/VitalsCard";
import { MedicationList } from "@/components/dashboard/MedicationList";
import { ScheduleList } from "@/components/dashboard/ScheduleList";
import { HeartModel } from "@/components/dashboard/HeartModel";
import { TriageWidget } from "@/components/dashboard/TriageWidget";
import { NoteWidget } from "@/components/dashboard/NoteWidget";
import { Search, Bell, ChevronDown } from "lucide-react";

export default async function Dashboard() {
  const data = await api.dashboard.getPatientData({});
  // No email = fetches first patient (Sourav)

  const { patient, widgets } = data;

  return (
    <div className="flex min-h-screen bg-[#F8F9FA] text-slate-800 font-sans">
      <Sidebar />

      <main className="flex-1 ml-20 p-8">
        {/* Header */}
        <header className="flex justify-between items-center mb-10">
          <div>
            <h1 className="text-3xl font-bold mb-1">Good Morning, {patient.name}</h1>
            <p className="text-slate-400 text-sm">You have {patient.appointments.length} appointments today</p>
          </div>

          <div className="flex items-center gap-4">
            <div className="bg-white p-2 rounded-xl border border-slate-100 flex items-center gap-2 px-4 shadow-sm">
              <Search className="text-slate-400 w-4 h-4" />
              <input suppressHydrationWarning type="text" placeholder="Search" className="bg-transparent outline-none text-sm w-32" />
            </div>
            <button suppressHydrationWarning className="bg-white p-3 rounded-xl border border-slate-100 shadow-sm relative">
              <Bell className="text-slate-600 w-4 h-4" />
              <div className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full border-2 border-white"></div>
            </button>

            <div className="flex items-center gap-2 bg-blue-600 pl-4 pr-2 py-1.5 rounded-full text-white shadow-lg shadow-blue-200 cursor-pointer">
              <span className="text-sm font-bold">Weekly</span>
              <div className="bg-white rounded-full p-1">
                <ChevronDown className="text-blue-600 w-3 h-3" />
              </div>
            </div>
          </div>
        </header>

        {/* Grid Layout */}
        <div className="grid grid-cols-12 gap-8 h-[calc(100vh-140px)]">

          {/* Left Col: 3D Body Visual */}
          <div className="col-span-12 lg:col-span-4 xl:col-span-5 relative">
            <HeartModel
              heartRate={widgets.heartRate[widgets.heartRate.length - 1]?.value || 0}
              history={widgets.heartRate}
            />
          </div>

          {/* Right Col: Widgets */}
          <div className="col-span-12 lg:col-span-8 xl:col-span-7 flex flex-col gap-6">

            {/* Row 1: Vitals */}
            <div className="grid grid-cols-3 gap-6">
              <VitalsCard
                title="Glucose Level"
                value={127} unit="ml"
                goal="125ml/day"
                color="blue"
                data={widgets.glucose}
              />
              <VitalsCard
                title="Cholesterol Level"
                value={164} unit="mg"
                goal="160ml/day"
                color="indigo"
                data={widgets.cholesterol}
              />
              <VitalsCard
                title="Paracetamol"
                value={35} unit="%"
                goal="40%/day"
                color="blue"
                data={[{ value: 20 }, { value: 35 }]}
              />
            </div>

            {/* Row 2: Medication & Schedule */}
            <div className="grid grid-cols-5 gap-6 flex-1">
              <div className="col-span-2">
                <MedicationList medications={patient.medications} />
              </div>
              <div className="col-span-3">
                <ScheduleList appointments={patient.appointments.map((a: any) => ({
                  id: a.id,
                  doctorName: a.doctor.name || "Unknown",
                  specialty: "Specialist", // In a real app, Doctor would have Specialty field
                  date: a.date
                }))} />
              </div>
            </div>

            {/* Row 3: Clinical AI Tools */}
            <div className="mt-8 mb-8">
              <h3 className="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">
                <span className="w-1 h-6 bg-gradient-to-b from-rose-500 to-indigo-600 rounded-full"></span>
                Clinical AI Tools
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 h-[600px]">
                <TriageWidget />
                <NoteWidget />
              </div>
            </div>

          </div>
        </div>
      </main>
    </div>
  );
}
