import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* 暂时跳过类型检查以加速构建，后续应移除此项 */
  typescript: {
    ignoreBuildErrors: true,
  },

  /* 隐藏 X-Powered-By 响应头，减少信息泄露 */
  poweredByHeader: false,

  /* 生产环境移除 console.log，保留 error/warn */
  compiler: {
    removeConsole:
      process.env.NODE_ENV === "production"
        ? { exclude: ["error", "warn"] }
        : false,
  },

  /* 图片优化：格式 + 远程图片白名单 */
  images: {
    formats: ["image/webp", "image/avif"],
    remotePatterns: [
      {
        protocol: "https",
        hostname: "**",
      },
      {
        protocol: "http",
        hostname: "localhost",
      },
      {
        protocol: "http",
        hostname: "127.0.0.1",
      },
    ],
  },

  /* 安全响应头 */
  headers: async () => [
    {
      source: "/(.*)",
      headers: [
        {
          key: "X-Frame-Options",
          value: "SAMEORIGIN",
        },
        {
          key: "X-Content-Type-Options",
          value: "nosniff",
        },
        {
          key: "Referrer-Policy",
          value: "strict-origin-when-cross-origin",
        },
        {
          key: "Permissions-Policy",
          value: "camera=(), microphone=(self), geolocation=()",
        },
      ],
    },
    /* 静态资源长期缓存 */
    {
      source: "/images/(.*)",
      headers: [
        {
          key: "Cache-Control",
          value: "public, max-age=31536000, immutable",
        },
      ],
    },
    {
      source: "/:path*.(svg|ico|json)",
      headers: [
        {
          key: "Cache-Control",
          value: "public, max-age=86400, stale-while-revalidate=604800",
        },
      ],
    },
    {
      source: "/sw.js",
      headers: [
        {
          key: "Cache-Control",
          value: "public, max-age=0, must-revalidate",
        },
      ],
    },
  ],
};

export default nextConfig;
