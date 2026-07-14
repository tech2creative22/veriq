"use client";

import { FormEvent, useEffect, useState } from "react";
import { AppShell } from "../../components/app-shell";
import { getLatestEvidence, getWorkspace, updateWorkspace, type EvidencePackage, type WorkspaceContext } from "../../lib/veriq-api";
import "./settings.css";

const emptyWorkspace: WorkspaceContext = { school_name: "", school_location: "", user_name: "", user_role: "", updated_at: "" };

export default function SettingsPage() {
  const [workspace, setWorkspace] = useState(emptyWorkspace);
  const [evidence, setEvidence] = useState<EvidencePackage | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  useEffect(() => {
    Promise.all([getWorkspace(), getLatestEvidence(true)]).then(([currentWorkspace, currentEvidence]) => { setWorkspace(currentWorkspace); setEvidence(currentEvidence); }).catch((requestError) => setError(requestError instanceof Error ? requestError.message : "Workspace settings could not be loaded."));
  }, []);
  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault(); setSaving(true); setError(null); setStatus(null);
    try {
      const saved = await updateWorkspace({ school_name: workspace.school_name, school_location: workspace.school_location, user_name: workspace.user_name, user_role: workspace.user_role });
      setWorkspace(saved); setStatus("Workspace identity saved. New uploads and Beacon responses will use this context.");
      window.dispatchEvent(new CustomEvent("veriq:workspace-updated", { detail: saved }));
    } catch (requestError) { setError(requestError instanceof Error ? requestError.message : "Workspace settings could not be saved."); }
    finally { setSaving(false); }
  };
  const change = (field: keyof WorkspaceContext, value: string) => setWorkspace((current) => ({ ...current, [field]: value }));

  return <AppShell activeNavigation="Settings"><main className="settings-page">
    <header className="settings-intro"><p className="eyebrow">WORKSPACE SETTINGS</p><h1>Keep Veriq aligned with your school.</h1><p>This identity is stored locally and becomes part of every new intelligence analysis.</p></header>
    <div className="settings-grid"><form className="settings-form" onSubmit={submit}><div className="settings-section-heading"><div><p>SCHOOL AND LEADERSHIP</p><h2>Active workspace identity</h2></div><span>SQLite persisted</span></div>
      <label><span>School name</span><input value={workspace.school_name} onChange={(event) => change("school_name", event.target.value)} minLength={2} maxLength={120} required /></label>
      <label><span>School location</span><input value={workspace.school_location} onChange={(event) => change("school_location", event.target.value)} minLength={2} maxLength={160} required /></label>
      <label><span>Your name</span><input value={workspace.user_name} onChange={(event) => change("user_name", event.target.value)} minLength={2} maxLength={100} required /></label>
      <label><span>Your role</span><input value={workspace.user_role} onChange={(event) => change("user_role", event.target.value)} minLength={2} maxLength={100} required /></label>
      {error ? <p className="settings-error" role="alert">{error}</p> : null}{status ? <p className="settings-success" role="status">{status}</p> : null}
      <button type="submit" disabled={saving || !workspace.school_name.trim() || !workspace.user_name.trim()}>{saving ? "Saving workspace…" : "Save workspace"}</button>
    </form>
    <aside className="settings-intelligence"><p>CONNECTED INTELLIGENCE</p><h2>{evidence?.source === "csv_import" ? "Latest uploaded evidence" : "Prepared example evidence"}</h2><dl><div><dt>Analysis</dt><dd>{evidence?.analysis_id.slice(-8) ?? "Loading…"}</dd></div><div><dt>Learners</dt><dd>{evidence?.data_summary.learners ?? "—"}</dd></div><div><dt>Classes</dt><dd>{evidence?.data_summary.classes ?? "—"}</dd></div><div><dt>Confidence</dt><dd>{evidence ? `${evidence.confidence}%` : "—"}</dd></div></dl><small>Changing the school name updates the active Beacon context. It does not alter attendance, behaviour or assessment calculations.</small></aside></div>
  </main></AppShell>;
}
