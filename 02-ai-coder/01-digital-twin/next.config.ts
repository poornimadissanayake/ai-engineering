import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // This app lives in a subfolder of a larger repo; pin the root to this folder.
  turbopack: { root: __dirname },
  outputFileTracingRoot: __dirname,
};

export default nextConfig;
