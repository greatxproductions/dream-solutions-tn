// @ts-check
import { defineConfig } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';

import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: "https://dreamsolutionstn.com",
  output: "static",
  adapter: cloudflare(),
  vite: {
    plugins: [tailwindcss()]
  }
});