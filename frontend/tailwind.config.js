/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                medical: {
                    50: '#f0f9ff',
                    100: '#e0f2fe',
                    200: '#bae6fd',
                    300: '#7dd3fc',
                    400: '#38bdf8',
                    500: '#0ea5e9',
                    600: '#0284c7',
                    700: '#0369a1',
                    800: '#075985',
                    900: '#0c4a6e',
                },
                urgency: {
                    1: '#ef4444', // Resuscitation (Red)
                    2: '#f97316', // Emergent (Orange)
                    3: '#eab308', // Urgent (Yellow)
                    4: '#22c55e', // Less Urgent (Green)
                    5: '#3b82f6', // Non-Urgent (Blue)
                }
            }
        },
    },
    plugins: [],
}
