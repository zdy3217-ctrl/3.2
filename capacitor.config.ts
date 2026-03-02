import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.narratorai.omega',
  appName: 'NarratorAI Omega',
  webDir: 'out', // Next.js 静态导出目录（需在 next.config.ts 中设置 output: 'export'）

  // Android 特定配置
  android: {
    // 允许混合内容（HTTP + HTTPS）
    allowMixedContent: true,
    // WebView 背景色（与应用主题一致）
    backgroundColor: '#000000',
  },

  server: {
    // 允许导航到的外部域名（按需添加你的 API 服务器地址）
    allowNavigation: [
      'localhost',
      '*.narratorai.com',
    ],
    // 开发时可指向本地 dev server（生产打包时注释掉）
    // url: 'http://192.168.x.x:3000',
    // cleartext: true,
  },

  plugins: {
    // 如需使用 Capacitor 插件，在此配置
    // 例如 SplashScreen:
    // SplashScreen: {
    //   launchAutoHide: true,
    //   androidScaleType: 'CENTER_CROP',
    // },
  },
};

export default config;
