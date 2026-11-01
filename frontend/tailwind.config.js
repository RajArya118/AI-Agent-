/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        chatDark: {
          bg: "#212121",
          sidebar: "#171717",
          card: "#2f2f2f",
          border: "#424242",
          input: "#2f2f2f",
          hover: "#2a2a2a"
        },
        chatLight: {
          bg: "#ffffff",
          sidebar: "#f9f9f9",
          card: "#f4f4f4",
          border: "#e5e5e5",
          input: "#ffffff",
          hover: "#ececec"
        }
      },
      animation: {
        'pulse-subtle': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    },
  },
  plugins: [],
}
