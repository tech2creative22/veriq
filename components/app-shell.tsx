"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState, type ReactNode } from "react";
import { getWorkspace, type WorkspaceContext } from "../lib/veriq-api";
import { AppIcon, type AppIconName, VeriqMark } from "./app-icons";

type NavigationItem = "School Pulse" | "Upload data" | "Early Intervention" | "Beacon" | "Decision Brief" | "Settings";
const navigation: Array<{ label: Exclude<NavigationItem, "Settings">; icon: AppIconName; href: string }> = [
  { label: "School Pulse", icon: "home", href: "/" },
  { label: "Upload data", icon: "upload", href: "/upload" },
  { label: "Early Intervention", icon: "trend", href: "/early-intervention" },
  { label: "Beacon", icon: "sparkles", href: "/beacon" },
  { label: "Decision Brief", icon: "clipboard", href: "/decision-brief" },
];
const fallbackWorkspace: WorkspaceContext = { school_name: "Mufakose High", school_location: "Harare, Zimbabwe", user_name: "Tendai Moyo", user_role: "Deputy Head", updated_at: "" };
function initials(name: string) { return name.split(/\s+/).filter(Boolean).slice(0, 2).map((part) => part[0]).join("").toUpperCase(); }

export function AppShell({ children, activeNavigation = "School Pulse" }: { children: ReactNode; activeNavigation?: NavigationItem }) {
  const router = useRouter();
  const [workspace, setWorkspace] = useState(fallbackWorkspace);
  useEffect(() => {
    getWorkspace().then(setWorkspace).catch(() => undefined);
    const syncWorkspace = (event: Event) => setWorkspace((event as CustomEvent<WorkspaceContext>).detail);
    window.addEventListener("veriq:workspace-updated", syncWorkspace);
    return () => window.removeEventListener("veriq:workspace-updated", syncWorkspace);
  }, []);
  const userInitials = initials(workspace.user_name);
  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><VeriqMark /><span>veriq</span></div>
      <button className="school-switcher" type="button" onClick={() => router.push("/settings")} aria-label="Open school settings"><span className="school-dot"><AppIcon name="building" size={16} /></span><div><strong>{workspace.school_name}</strong><small>{workspace.school_location}</small></div><AppIcon name="chevron-down" size={15} /></button>
      <nav aria-label="Primary navigation"><p className="nav-label">WORKSPACE</p>{navigation.map((item) => <Link key={item.label} href={item.href} className={`nav-item ${activeNavigation === item.label ? "active" : ""}`} aria-current={activeNavigation === item.label ? "page" : undefined}><AppIcon name={item.icon} size={19} />{item.label}</Link>)}</nav>
      <div className="sidebar-footer"><Link className={`nav-item ${activeNavigation === "Settings" ? "active" : ""}`} href="/settings" aria-current={activeNavigation === "Settings" ? "page" : undefined}><AppIcon name="settings" size={19} />Settings</Link><div className="profile"><span>{userInitials}</span><div><strong>{workspace.user_name}</strong><small>{workspace.user_role}</small></div><button aria-label="Open profile settings" type="button" onClick={() => router.push("/settings")}><AppIcon name="more" size={18} /></button></div></div>
    </aside>
    <div className="workspace"><header className="topbar"><Link className="mobile-mark" href="/" aria-label="Go to School Pulse"><VeriqMark size={27} /></Link><div className="crumb"><span>Workspace</span><span>/</span><strong>{activeNavigation}</strong></div><div className="topbar-actions"><button className="icon-button" aria-label="Search school evidence with Beacon" title="Search school evidence with Beacon" type="button" onClick={() => router.push("/beacon?focus=1")}><AppIcon name="search" size={18} /></button><button className="icon-button notification" aria-label="View latest findings" title="View latest findings" type="button" onClick={() => router.push("/#latest-findings")}><AppIcon name="bell" size={19} /><i /></button><button className="avatar" type="button" aria-label="Open profile settings" onClick={() => router.push("/settings")}>{userInitials}</button></div></header>{children}</div>
  </div>;
}
