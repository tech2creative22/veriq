export type AppIconName =
  | "home"
  | "trend"
  | "sparkles"
  | "clipboard"
  | "upload"
  | "settings"
  | "search"
  | "bell"
  | "building"
  | "chevron-down"
  | "more"
  | "plus"
  | "send"
  | "arrow-right";

type AppIconProps = {
  name: AppIconName;
  size?: number;
  className?: string;
};

const paths: Record<AppIconName, React.ReactNode> = {
  home: <><path d="M3 10.5 12 3l9 7.5" /><path d="M5.5 9.5V21h13V9.5" /><path d="M9.5 21v-6h5v6" /></>,
  trend: <><path d="M4 17.5 9 12l4 3 7-9" /><path d="M16 6h4v4" /><circle cx="4" cy="17.5" r="1.5" /><circle cx="9" cy="12" r="1.5" /><circle cx="13" cy="15" r="1.5" /></>,
  sparkles: <><path d="m12 3 1.3 3.7L17 8l-3.7 1.3L12 13l-1.3-3.7L7 8l3.7-1.3L12 3Z" /><path d="m18.5 13 1 2.5L22 16.5l-2.5 1-1 2.5-1-2.5-2.5-1 2.5-1 1-2.5Z" /><path d="m5.5 14 .8 2.2 2.2.8-2.2.8L5.5 20l-.8-2.2-2.2-.8 2.2-.8.8-2.2Z" /></>,
  clipboard: <><rect x="5" y="5" width="14" height="16" rx="2" /><path d="M9 5.5V3h6v2.5" /><path d="M9 10h6M9 14h6M9 18h4" /></>,
  upload: <><path d="M12 16V4" /><path d="m7.5 8.5 4.5-4.5 4.5 4.5" /><path d="M5 14v6h14v-6" /></>,
  settings: <><circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1-2.8 2.8-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.6v.2h-4V21a1.7 1.7 0 0 0-1-1.6 1.7 1.7 0 0 0-1.9.3l-.1.1L4.2 17l.1-.1a1.7 1.7 0 0 0 .3-1.9A1.7 1.7 0 0 0 3 14H2.8v-4H3a1.7 1.7 0 0 0 1.6-1 1.7 1.7 0 0 0-.3-1.9L4.2 7 7 4.2l.1.1a1.7 1.7 0 0 0 1.9.3A1.7 1.7 0 0 0 10 3V2.8h4V3a1.7 1.7 0 0 0 1 1.6 1.7 1.7 0 0 0 1.9-.3l.1-.1L19.8 7l-.1.1a1.7 1.7 0 0 0-.3 1.9 1.7 1.7 0 0 0 1.6 1h.2v4H21a1.7 1.7 0 0 0-1.6 1Z" /></>,
  search: <><circle cx="10.5" cy="10.5" r="6.5" /><path d="m16 16 4 4" /></>,
  bell: <><path d="M18 9a6 6 0 0 0-12 0c0 7-3 7-3 8.5h18C21 16 18 16 18 9Z" /><path d="M10 21h4" /></>,
  building: <><path d="M4 21V8l8-4 8 4v13" /><path d="M2 21h20M8 11h2M14 11h2M8 15h2M14 15h2M10 21v-3h4v3" /></>,
  "chevron-down": <path d="m7 9 5 5 5-5" />,
  more: <><circle cx="5" cy="12" r="1" fill="currentColor" /><circle cx="12" cy="12" r="1" fill="currentColor" /><circle cx="19" cy="12" r="1" fill="currentColor" /></>,
  plus: <><path d="M12 5v14M5 12h14" /></>,
  send: <><path d="m3 11 18-8-8 18-2.5-7.5L3 11Z" /><path d="M10.5 13.5 21 3" /></>,
  "arrow-right": <><path d="M5 12h14" /><path d="m14 7 5 5-5 5" /></>,
};

export function AppIcon({ name, size = 20, className }: AppIconProps) {
  return <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{paths[name]}</svg>;
}

export function VeriqMark({ size = 34 }: { size?: number }) {
  return <svg className="veriq-mark" width={size} height={size} viewBox="0 0 36 36" fill="none" aria-hidden="true">
    <defs><linearGradient id="veriq-mark-gradient" x1="4" y1="3" x2="31" y2="33" gradientUnits="userSpaceOnUse"><stop stopColor="#8B6CFF" /><stop offset="1" stopColor="#4B2CDD" /></linearGradient></defs>
    <path d="M7.1 6.2c1.7-1 3.8-.4 4.8 1.3l6.4 11.1-5.2 9a2.6 2.6 0 0 1-4.5 0L3.3 18.4a5.1 5.1 0 0 1 0-5.1l3.8-7.1Z" fill="url(#veriq-mark-gradient)" />
    <path d="M24.1 6.6a4.7 4.7 0 0 1 8.1 4.7L23.4 27a2.6 2.6 0 0 1-4.5 0l-3.1-5.4 8.3-15Z" fill="url(#veriq-mark-gradient)" opacity=".96" />
  </svg>;
}
