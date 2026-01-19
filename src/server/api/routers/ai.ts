import { z } from "zod";
import { createTRPCRouter, publicProcedure } from "@/server/api/trpc";

// Define input types matching the Python API
const TriageInputSchema = z.object({
    chief_complaint: z.string(),
    vitals: z.object({
        hr: z.number(),
        bp: z.string(),
        spo2: z.number(),
        temp: z.number(),
        rr: z.number()
    }),
    image_base64: z.string().optional().nullable()
});

const NoteInputSchema = z.object({
    encounter_text: z.string(),
    patient_context: z.string().optional(),
    encounter_type: z.string().default("Emergency")
});

export const aiRouter = createTRPCRouter({
    triage: publicProcedure
        .input(TriageInputSchema)
        .mutation(async ({ input }) => {
            try {
                // Parse BP string "120/80" -> bp_sys, bp_dia
                const [sysStr, diaStr] = input.vitals.bp.split("/");
                const bp_sys = parseInt(sysStr || "0", 10);
                const bp_dia = parseInt(diaStr || "0", 10);

                const payload = {
                    chief_complaint: input.chief_complaint,
                    vitals: {
                        hr: input.vitals.hr,
                        bp_sys,
                        bp_dia,
                        spo2: input.vitals.spo2,
                        temp: input.vitals.temp,
                        rr: input.vitals.rr
                    },
                    image_base64: input.image_base64
                };

                const response = await fetch("http://127.0.0.1:8000/api/triage", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload),
                });

                if (!response.ok) {
                    const errText = await response.text();
                    throw new Error(`AI Service Error (${response.status}): ${errText}`);
                }

                return await response.json();
            } catch (error: any) {
                console.error("Triage API Error:", error);
                throw new Error(`Failed to connect to AI Triage Service: ${error.message || error}`);
            }
        }),

    generateNote: publicProcedure
        .input(NoteInputSchema)
        .mutation(async ({ input }) => {
            try {
                const response = await fetch("http://127.0.0.1:8000/api/generate-note", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(input),
                });

                if (!response.ok) {
                    throw new Error(`AI Service Error: ${response.statusText}`);
                }

                const data = await response.json();
                return data.json;
            } catch (error: any) {
                console.error("Note API Error:", error);
                throw new Error(`Failed to connect to AI Note Service: ${error.message || error}`);
            }
        }),

});
