/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#E9EFC0",
        secondary: "#B4E197",
        accent: "#83BD75",
        darkgreen: "#4E944F",
        textmain: "#333333",
        textsub: "#666666",
      },
      fontFamily: {
        main: ["Nanum Gothic", "sans-serif"],
        sub: ["Gaegu", "cursive"],
        logo: ["Single Day", "cursive"],
      },
    },
  },
  plugins: [],
}
