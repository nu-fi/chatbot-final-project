/** @type {import('tailwindcss').Config} */ 
module.exports = {
  content: [
    "./../../templates/**/*.{html,js}",
    "./js/**/*.js",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {
      zIndex: {
        '12345': '12345',
      },
      spacing: {
        '30px': '30px',
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/line-clamp'),
    require("flowbite/plugin")
  ],
}