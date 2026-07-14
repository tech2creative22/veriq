"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { AppShell } from "../../components/app-shell";
import { uploadAndAnalyse, type EvidencePackage } from "../../lib/veriq-api";
import "./upload.css";

type FileKind = "attendance" | "behaviour" | "assessments";
type UploadFiles = Record<FileKind, File | null>;

const uploadItems: Array<{ id: FileKind; title: string; required: string; description: string }> = [
  { id: "attendance", title: "Attendance", required: "student_id, class_name, date, status", description: "Daily learner attendance records" },
  { id: "behaviour", title: "Behaviour", required: "student_id, class_name, date, incident_type, severity", description: "Behaviour incident records" },
  { id: "assessments", title: "Assessments", required: "student_id, class_name, subject, date, score", description: "Subject assessment results" },
];
const processingSteps = ["Preparing Evidence", "Finding Signals", "Generating School Pulse", "Ready"] as const;

export default function UploadPage() {
  const router = useRouter();
  const [files, setFiles] = useState<UploadFiles>({ attendance: null, behaviour: null, assessments: null });
  const [acknowledged, setAcknowledged] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [stage, setStage] = useState<"idle" | "validating" | "analysing" | "complete">("idle");
  const [processingStep, setProcessingStep] = useState(-1);
  const [result, setResult] = useState<EvidencePackage | null>(null);

  const selectFile = (kind: FileKind, file: File | null) => {
    if (!file) return;
    if (!file.name.toLowerCase().endsWith(".csv")) {
      setError(`${file.name} is not a CSV file. Please choose a .csv file.`);
      return;
    }
    setError(null);
    setFiles((current) => ({ ...current, [kind]: file }));
  };

  const analyse = async () => {
    if (!acknowledged) {
      setError("Confirm the data-use acknowledgement before starting analysis.");
      return;
    }
    if (Object.values(files).some((file) => !file)) {
      setError("Select all three CSV files before starting analysis. Missing files reduce Beacon’s confidence.");
      return;
    }
    setError(null);
    setStage("validating");
    setProcessingStep(0);
    let progressTimer: number | undefined;
    try {
      setStage("analysing");
      progressTimer = window.setInterval(() => setProcessingStep((current) => Math.min(current + 1, 2)), 900);
      const intelligence = await uploadAndAnalyse(files as Record<FileKind, File>, acknowledged);
      setResult(intelligence);
      window.clearInterval(progressTimer);
      setProcessingStep(3);
      setStage("complete");
    } catch (requestError) {
      if (progressTimer) window.clearInterval(progressTimer);
      setStage("idle");
      setProcessingStep(-1);
      setError(requestError instanceof Error ? requestError.message : "Veriq could not analyse these files.");
    }
  };

  return (
    <AppShell activeNavigation="Upload data">
      <main className="upload-page">
        <section className="upload-intro page-reveal">
          <p className="eyebrow">SCHOOL DATA IMPORT</p>
          <h1>Bring today&apos;s school evidence into Veriq.</h1>
          <p>Veriq preserves your raw files, validates their structure, then prepares one persistent intelligence snapshot used across the product.</p>
        </section>

        <section className="upload-brief">
          <span>✦</span>
          <div>
            <p>BEACON GUIDANCE</p>
            <h2>All three files together provide the connected school picture.</h2>
            <small>Attendance, behaviour, and assessment records are stored together so every metric and Beacon response uses the same analysis.</small>
          </div>
        </section>

        <section className="upload-grid">
          {uploadItems.map((item) => (
            <label className="upload-card" key={item.id}>
              <input
                type="file"
                accept=".csv,text/csv"
                disabled={stage !== "idle"}
                onChange={(event) => selectFile(item.id, event.target.files?.[0] ?? null)}
              />
              <span className="upload-icon">↑</span>
              <div>
                <p>{item.title}</p>
                <strong>{files[item.id]?.name ?? "Choose CSV file"}</strong>
                <small>{files[item.id] ? `${Math.ceil(files[item.id]!.size / 1024)} KB ready for validation` : item.description}</small>
              </div>
              <em>{files[item.id] ? "Ready" : "Required"}</em>
              <span className="upload-schema">Required: {item.required}</span>
            </label>
          ))}
        </section>

        <label className="upload-acknowledgement" htmlFor="upload-authority">
          <input
            id="upload-authority"
            type="checkbox"
            checked={acknowledged}
            disabled={stage !== "idle"}
            onChange={(event) => {
              setAcknowledged(event.target.checked);
              if (event.target.checked) setError(null);
            }}
          />
          <span>
            <strong>Data-use acknowledgement</strong>
            <small>I confirm I am authorised to use these files. For this MVP demonstration I will upload fictional or synthetic learner data only—not real learner records.</small>
          </span>
        </label>

        {error ? <p className="upload-error" role="alert">{error}</p> : null}

        <section className="upload-processing">
          <div className="upload-processing-copy">
            <p>IMPORT STATUS</p>
            <h2>{stage === "idle" ? "Ready when you are." : stage === "validating" ? "Validating file structure…" : stage === "analysing" ? "Preparing connected school intelligence…" : "Every workspace is ready."}</h2>
            <small>{stage === "idle" ? "No analysis begins until each file is present, valid and acknowledged." : stage === "validating" ? "Checking required fields, dates, supported values and score ranges." : stage === "analysing" ? "Storing canonical records and calculating verified metrics." : `${result?.data_summary.learners ?? 0} learners across ${result?.data_summary.classes ?? 0} class${result?.data_summary.classes === 1 ? "" : "es"} now share analysis ${result?.analysis_id.slice(-8) ?? ""}.`}</small>
            {processingStep >= 0 ? (
              <ol className="upload-progress" aria-label="Evidence preparation progress">
                {processingSteps.map((step, index) => (
                  <li key={step} className={index < processingStep ? "complete" : index === processingStep ? "active" : ""}>
                    <span>{index < processingStep ? "✓" : index + 1}</span>{step}
                  </li>
                ))}
              </ol>
            ) : null}
          </div>
          {stage === "complete" ? (
            <button type="button" onClick={() => router.push("/")}>View connected School Pulse →</button>
          ) : (
            <button type="button" onClick={analyse} disabled={stage !== "idle" || !acknowledged}>
              {stage === "idle" ? "Validate and analyse →" : "Working…"}
            </button>
          )}
        </section>
      </main>
    </AppShell>
  );
}
