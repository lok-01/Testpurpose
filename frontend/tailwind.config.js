/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        vedic: {
          navy: '#0B1B3D',
          darknavy: '#071026',
          gold: '#D4AF37',
          lightgold: '#FDF8E2',
          mutedgold: '#AA8825',
          cream: '#FBFBF9',
          border: '#E2E8F0',
        }
      }
    },
  },
  plugins: [],
}
