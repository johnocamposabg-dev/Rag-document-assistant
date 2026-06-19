/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html",
  "./src/**/*.{js,ts,jsx,tsx}",],
  theme: {
    extend: {
      colors: {
        'creamBg':'#faf6f0',
        'violetText':'#6b4eff',
      },
        fontFamily: {
          'title': ['Playfair Display', 'serif'],
          'body': ['Inter', 'sans-serif' ],
        },
    },
  },
  plugins: [],
}

