import { z } from "zod";
import { createTRPCRouter, publicProcedure } from "@/server/api/trpc";

export const dashboardRouter = createTRPCRouter({
    getPatientData: publicProcedure
        .input(z.object({ email: z.string().email().optional() }))
        .query(async ({ ctx, input }) => {
            try {
                // Find patient by email or default to the first PATIENT found
                const patient = await ctx.db.user.findFirst({
                    where: input.email ? { email: input.email } : { role: "PATIENT" },
                    include: {
                        vitals: {
                            orderBy: { timestamp: "asc" },
                        },
                        medications: true,
                        appointments: {
                            include: { doctor: true },
                            orderBy: { date: "asc" },
                        },
                    },
                });

                if (!patient) {
                    throw new Error("Patient not found");
                }

                // Process vitals for charts
                const glucoseData = patient.vitals
                    .filter((v: any) => v.type === "GLUCOSE")
                    .map((v: any) => ({ ...v, value: v.value }));

                const heartRateData = patient.vitals
                    .filter((v: any) => v.type === "HEART_RATE")
                    .map((v: any) => ({ ...v, value: v.value }));

                const cholesterolData = patient.vitals
                    .filter((v: any) => v.type === "CHOLESTEROL")
                    .map((v: any) => ({ ...v, value: v.value }));

                return {
                    patient,
                    widgets: {
                        glucose: glucoseData,
                        heartRate: heartRateData,
                        cholesterol: cholesterolData,
                    },
                };
            } catch (error) {
                console.warn("Database fetch failed, using mock data:", error);

                // Mock data for testing when Prisma is not working
                const mockPatient = {
                    id: "mock-1",
                    name: "Sourav",
                    email: "sourav@example.com",
                    role: "PATIENT",
                    medications: [
                        { id: "m1", name: "Hydration Therapy", dosage: "Revitalize", schedule: "Daily", adherence: 90, active: true },
                        { id: "m2", name: "Heart Wellness", dosage: "1 Tab", schedule: "Daily", adherence: 100, active: true },
                        { id: "m3", name: "Neuro Vitality", dosage: "2 Caps", schedule: "AM", adherence: 85, active: true },
                        { id: "m4", name: "Vital Energy Pack", dosage: "1 Pack", schedule: "PM", adherence: 60, active: true },
                        { id: "m5", name: "Paracetamol", dosage: "500mg", schedule: "As needed", adherence: 35, active: true }
                    ],
                    appointments: [
                        { id: "a1", date: new Date(), type: "Cardiologist", status: "UPCOMING", doctor: { name: "Dr. Selena Gomez" } },
                        { id: "a2", date: new Date(Date.now() + 86400000), type: "Neurology Specialist", status: "UPCOMING", doctor: { name: "Dr. Steevan Nicholas" } }
                    ]
                };

                const mockWidgets = {
                    glucose: [
                        { value: 115, timestamp: new Date(Date.now() - 86400000 * 6) },
                        { value: 118, timestamp: new Date(Date.now() - 86400000 * 5) },
                        { value: 122, timestamp: new Date(Date.now() - 86400000 * 4) },
                        { value: 119, timestamp: new Date(Date.now() - 86400000 * 3) },
                        { value: 120, timestamp: new Date(Date.now() - 86400000 * 2) },
                        { value: 118, timestamp: new Date(Date.now() - 86400000) },
                        { value: 127, timestamp: new Date() }
                    ],
                    heartRate: [
                        { value: 72, timestamp: new Date(Date.now() - 3600000 * 9) },
                        { value: 75, timestamp: new Date(Date.now() - 3600000 * 8) },
                        { value: 82, timestamp: new Date(Date.now() - 3600000 * 7) },
                        { value: 78, timestamp: new Date(Date.now() - 3600000 * 6) },
                        { value: 70, timestamp: new Date(Date.now() - 3600000 * 5) },
                        { value: 71, timestamp: new Date(Date.now() - 3600000 * 4) },
                        { value: 74, timestamp: new Date(Date.now() - 3600000 * 3) },
                        { value: 76, timestamp: new Date(Date.now() - 3600000 * 2) },
                        { value: 92, timestamp: new Date(Date.now() - 3600000) },
                        { value: 120, timestamp: new Date() }
                    ],
                    cholesterol: [
                        { value: 145, timestamp: new Date(Date.now() - 86400000 * 6) },
                        { value: 148, timestamp: new Date(Date.now() - 86400000 * 5) },
                        { value: 152, timestamp: new Date(Date.now() - 86400000 * 4) },
                        { value: 150, timestamp: new Date(Date.now() - 86400000 * 3) },
                        { value: 150, timestamp: new Date(Date.now() - 86400000 * 2) },
                        { value: 155, timestamp: new Date(Date.now() - 86400000) },
                        { value: 164, timestamp: new Date() }
                    ]
                };

                return {
                    patient: mockPatient,
                    widgets: mockWidgets
                };
            }
        }),
});
