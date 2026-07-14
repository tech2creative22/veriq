export type BeaconContext = {
  id: string;
  label: string;
  title: string;
  summary: string;
  evidence: string;
  questions: readonly [string, string, string];
};

export type Metric = {
  id: string;
  label: string;
  value: string;
  detail: string;
  change: string;
  tone: "positive" | "attention" | "neutral";
  icon: string;
  insight: string;
  beacon: BeaconContext;
};

export type Priority = {
  id: string;
  level: "High" | "Medium" | "Watch";
  title: string;
  description: string;
  action: string;
  href?: string;
  icon: string;
  beacon: BeaconContext;
};

export type Alert = {
  id: string;
  time: string;
  title: string;
  detail: string;
  tone: "success" | "attention" | "neutral";
  beacon: BeaconContext;
};

export type InterventionEvidence = {
  label: string;
  detail: string;
  tone: "critical" | "attention" | "neutral";
};
