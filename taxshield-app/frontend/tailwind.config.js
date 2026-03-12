module.exports = {
  content: ["./pages/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}", "./layouts/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ubaRed: '#9b111e',
        ubaBlack: '#0b0b0f'
      },
      boxShadow: {
        neon: '0 0 25px rgba(155,17,30,0.35)'
      }
    },
  },
  plugins: [],
};
