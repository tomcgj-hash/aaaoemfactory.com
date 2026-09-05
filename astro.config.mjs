import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// 注意：site 域名待用户确认后更新（当前为占位符）
export default defineConfig({
  site: 'https://aaaoemfactory.com',
  integrations: [sitemap()],
  server: {
    allowedHosts: true,
  },
});
