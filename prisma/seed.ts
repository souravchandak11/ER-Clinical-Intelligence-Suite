import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function main() {
    // Cleanup
    await prisma.vital.deleteMany()
    await prisma.medication.deleteMany()
    await prisma.appointment.deleteMany()
    await prisma.user.deleteMany()

    // Create Patient "Abraham"
    const abraham = await prisma.user.create({
        data: {
            email: 'abraham@example.com',
            name: 'Abraham',
            role: 'PATIENT',
            medications: {
                create: [
                    { name: 'Hydration Therapy', dosage: 'Revitalize', schedule: 'Daily', adherence: 90 },
                    { name: 'Heart Wellness', dosage: '1 Tab', schedule: 'Daily', adherence: 100 },
                    { name: 'Neuro Vitality', dosage: '2 Caps', schedule: 'AM', adherence: 85, active: true }, // Highlighted in UI
                    { name: 'Vital Energy Pack', dosage: '1 Pack', schedule: 'PM', adherence: 60 },
                    { name: 'Paracetamol', dosage: '500mg', schedule: 'As needed', adherence: 35 }
                ]
            },
            vitals: {
                create: [
                    // Glucose History
                    { type: 'GLUCOSE', value: 115, unit: 'ml', timestamp: new Date(Date.now() - 86400000 * 6) },
                    { type: 'GLUCOSE', value: 118, unit: 'ml', timestamp: new Date(Date.now() - 86400000 * 5) },
                    { type: 'GLUCOSE', value: 122, unit: 'ml', timestamp: new Date(Date.now() - 86400000 * 4) },
                    { type: 'GLUCOSE', value: 119, unit: 'ml', timestamp: new Date(Date.now() - 86400000 * 3) },
                    { type: 'GLUCOSE', value: 120, unit: 'ml', timestamp: new Date(Date.now() - 86400000 * 2) },
                    { type: 'GLUCOSE', value: 118, unit: 'ml', timestamp: new Date(Date.now() - 86400000) },
                    { type: 'GLUCOSE', value: 127, unit: 'ml', timestamp: new Date() },

                    // Cholesterol History
                    { type: 'CHOLESTEROL', value: 145, unit: 'mg', timestamp: new Date(Date.now() - 86400000 * 6) },
                    { type: 'CHOLESTEROL', value: 148, unit: 'mg', timestamp: new Date(Date.now() - 86400000 * 5) },
                    { type: 'CHOLESTEROL', value: 152, unit: 'mg', timestamp: new Date(Date.now() - 86400000 * 4) },
                    { type: 'CHOLESTEROL', value: 150, unit: 'mg', timestamp: new Date(Date.now() - 86400000 * 3) },
                    { type: 'CHOLESTEROL', value: 150, unit: 'mg', timestamp: new Date(Date.now() - 86400000 * 2) },
                    { type: 'CHOLESTEROL', value: 155, unit: 'mg', timestamp: new Date(Date.now() - 86400000) },
                    { type: 'CHOLESTEROL', value: 164, unit: 'mg', timestamp: new Date() },

                    // Heart Rate History
                    { type: 'HEART_RATE', value: 72, unit: 'bpm', timestamp: new Date(Date.now() - 3600000 * 9) },
                    { type: 'HEART_RATE', value: 75, unit: 'bpm', timestamp: new Date(Date.now() - 3600000 * 8) },
                    { type: 'HEART_RATE', value: 82, unit: 'bpm', timestamp: new Date(Date.now() - 3600000 * 7) },
                    { type: 'HEART_RATE', value: 78, unit: 'bpm', timestamp: new Date(Date.now() - 3600000 * 6) },
                    { type: 'HEART_RATE', value: 70, unit: 'bpm', timestamp: new Date(Date.now() - 3600000 * 5) },
                    { type: 'HEART_RATE', value: 71, unit: 'bpm', timestamp: new Date(Date.now() - 3600000 * 4) },
                    { type: 'HEART_RATE', value: 74, unit: 'bpm', timestamp: new Date(Date.now() - 3600000 * 3) },
                    { type: 'HEART_RATE', value: 76, unit: 'bpm', timestamp: new Date(Date.now() - 3600000 * 2) },
                    { type: 'HEART_RATE', value: 92, unit: 'bpm', timestamp: new Date(Date.now() - 3600000) },
                    { type: 'HEART_RATE', value: 120, unit: 'bpm', timestamp: new Date() },
                ]
            }
        }
    })

    // Create Doctor
    const drSelena = await prisma.user.create({
        data: { email: 'selena@hospital.com', name: 'Dr. Selena Gomez', role: 'DOCTOR' }
    })

    const drSteevan = await prisma.user.create({
        data: { email: 'steevan@hospital.com', name: 'Dr. Steevan Nicholas', role: 'DOCTOR' }
    })

    // Appointments
    await prisma.appointment.create({
        data: {
            patientId: abraham.id,
            doctorId: drSelena.id,
            date: new Date(), // Today
            type: 'Cardiologist',
            status: 'UPCOMING'
        }
    })

    await prisma.appointment.create({
        data: {
            patientId: abraham.id,
            doctorId: drSteevan.id,
            date: new Date(Date.now() + 86400000), // Tomorrow
            type: 'Neurology Specialist',
            status: 'UPCOMING'
        }
    })

    console.log('Database seeded with Abraham data!')
}

main()
    .then(async () => {
        await prisma.$disconnect()
    })
    .catch(async (e) => {
        console.error(e)
        await prisma.$disconnect()
        process.exit(1)
    })
