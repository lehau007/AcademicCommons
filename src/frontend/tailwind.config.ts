import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/**/*.{js,ts,jsx,tsx,mdx}"
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "canvas-base": {
          light: "#F8FAFC",
          dark: "#030712",
          DEFAULT: "var(--canvas-base)"
        },
        "surface-card": {
          light: "#FFFFFF",
          dark: "#0F172A",
          DEFAULT: "var(--surface-card)"
        },
        "charcoal-ink": {
          light: "#0F172A",
          dark: "#F8FAFC",
          DEFAULT: "var(--charcoal-ink)"
        },
        "muted-steel": {
          light: "#64748B",
          dark: "#94A3B8",
          DEFAULT: "var(--muted-steel)"
        },
        "whisper-border": {
          light: "#E2E8F0",
          dark: "#1E293B",
          DEFAULT: "var(--whisper-border)"
        },
        "hust-red": {
          light: "#990000",
          dark: "#EF4444",
          DEFAULT: "var(--hust-red)"
        },
        "pear-yellow": "#F59E0B",
        "system-green": "#22C55E",
        "system-red": "#EF4444"
      },
      fontFamily: {
        display: ["var(--font-display)", "Plus Jakarta Sans", "sans-serif"],
        body: ["var(--font-body)", "Be Vietnam Pro", "sans-serif"],
        mono: ["var(--font-jetbrains-mono)", "JetBrains Mono", "monospace"]
      },
      borderRadius: {
        button: "8px",
        card: "16px"
      }
    }
  },
  plugins: []
};

export default config;
