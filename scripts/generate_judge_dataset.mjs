import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(scriptDir, "..");
const outputDir = process.argv[2]
  ? path.resolve(process.argv[2])
  : path.join(repoRoot, "demo-data", "zimbabwe-secondary-judge");

const students = [
  ["PHS-F1A-001", "Tatenda", "Form 1A"], ["PHS-F1A-002", "Rutendo", "Form 1A"],
  ["PHS-F1A-003", "Tanaka", "Form 1A"], ["PHS-F1A-004", "Ropafadzo", "Form 1A"],
  ["PHS-F1A-005", "Farai", "Form 1A"], ["PHS-F2A-001", "Nyasha", "Form 2A"],
  ["PHS-F2A-002", "Tariro", "Form 2A"], ["PHS-F2A-003", "Anesu", "Form 2A"],
  ["PHS-F2A-004", "Kudzai", "Form 2A"], ["PHS-F2A-005", "Tinashe", "Form 2A"],
  ["PHS-F3A-001", "Tendai", "Form 3A"], ["PHS-F3A-002", "Chiedza", "Form 3A"],
  ["PHS-F3A-003", "Simbarashe", "Form 3A"], ["PHS-F3A-004", "Rudo", "Form 3A"],
  ["PHS-F3A-005", "Panashe", "Form 3A"], ["PHS-F4A-001", "Chipo", "Form 4A"],
  ["PHS-F4A-002", "Munashe", "Form 4A"], ["PHS-F4A-003", "Tapiwa", "Form 4A"],
  ["PHS-F4A-004", "Takudzwa", "Form 4A"], ["PHS-F4A-005", "Vimbai", "Form 4A"],
].map(([student_id, first_name, class_name]) => ({ student_id, first_name, class_name }));

const previousDates = ["2026-06-01", "2026-06-02", "2026-06-03", "2026-06-04", "2026-06-05", "2026-06-08", "2026-06-09", "2026-06-10", "2026-06-11", "2026-06-12"];
const currentDates = ["2026-06-29", "2026-06-30", "2026-07-01", "2026-07-02", "2026-07-03", "2026-07-06", "2026-07-07", "2026-07-08", "2026-07-09", "2026-07-10"];
const absences = {
  Tatenda: [0, 0], Rutendo: [1, 0], Tanaka: [0, 0], Ropafadzo: [0, 0], Farai: [1, 1],
  Nyasha: [0, 3], Tariro: [1, 0], Anesu: [0, 0], Kudzai: [1, 1], Tinashe: [0, 0],
  Tendai: [1, 3], Chiedza: [0, 0], Simbarashe: [1, 1], Rudo: [0, 0], Panashe: [0, 0],
  Chipo: [0, 4], Munashe: [1, 1], Tapiwa: [0, 1], Takudzwa: [1, 0], Vimbai: [0, 0],
};

const attendance = [];
for (const student of students) {
  const [previousAbsent, currentAbsent] = absences[student.first_name];
  previousDates.forEach((date, index) => attendance.push({
    ...student,
    date,
    status: index >= previousDates.length - previousAbsent ? "absent" : (index === 2 && previousAbsent === 0 ? "late" : "present"),
  }));
  currentDates.forEach((date, index) => attendance.push({
    ...student,
    date,
    status: index >= currentDates.length - currentAbsent ? "absent" : (index === 4 && currentAbsent === 0 ? "late" : "present"),
  }));
}

const studentByName = Object.fromEntries(students.map((student) => [student.first_name, student]));
const behaviour = [];
function incident(first_name, date, incident_type, severity) {
  behaviour.push({ ...studentByName[first_name], date, incident_type, severity });
}

incident("Tatenda", "2026-06-04", "classroom disruption", "low"); incident("Farai", "2026-06-11", "late to lesson", "low");
incident("Tatenda", "2026-07-02", "classroom disruption", "low"); incident("Farai", "2026-07-09", "late to lesson", "low");
incident("Tariro", "2026-06-04", "late to lesson", "low"); incident("Kudzai", "2026-06-11", "classroom disruption", "low");
incident("Nyasha", "2026-07-02", "defiance", "medium"); incident("Nyasha", "2026-07-02", "classroom disruption", "medium");
incident("Nyasha", "2026-07-09", "bullying", "high"); incident("Nyasha", "2026-07-09", "defiance", "medium"); incident("Kudzai", "2026-07-09", "classroom disruption", "low");
incident("Chiedza", "2026-06-04", "late to lesson", "low"); incident("Simbarashe", "2026-06-11", "classroom disruption", "low");
for (const [date, type, severity] of [
  ["2026-07-02", "defiance", "medium"], ["2026-07-02", "classroom disruption", "medium"], ["2026-07-02", "fighting", "high"],
  ["2026-07-09", "bullying", "high"], ["2026-07-09", "defiance", "medium"], ["2026-07-09", "classroom disruption", "medium"], ["2026-07-09", "property damage", "high"],
]) incident("Tendai", date, type, severity);
incident("Chiedza", "2026-07-02", "late to lesson", "low"); incident("Simbarashe", "2026-07-09", "classroom disruption", "low");
incident("Munashe", "2026-06-04", "late to lesson", "low"); incident("Takudzwa", "2026-06-11", "classroom disruption", "low");
for (const [date, type, severity] of [
  ["2026-07-02", "defiance", "medium"], ["2026-07-02", "classroom disruption", "medium"], ["2026-07-02", "fighting", "high"], ["2026-07-02", "bullying", "high"],
  ["2026-07-09", "defiance", "medium"], ["2026-07-09", "classroom disruption", "medium"], ["2026-07-09", "property damage", "high"], ["2026-07-09", "fighting", "high"],
]) incident("Chipo", date, type, severity);
incident("Munashe", "2026-07-02", "late to lesson", "low"); incident("Takudzwa", "2026-07-09", "classroom disruption", "low");

const subjects = ["Mathematics", "English Language", "Combined Science", "Heritage Studies", "Shona Language"];
const assessmentDates = ["2026-06-05", "2026-06-19", "2026-07-03", "2026-07-10"];
const scoreBase = { Tatenda: 68, Rutendo: 74, Tanaka: 70, Ropafadzo: 63, Farai: 58, Nyasha: 66, Tariro: 72, Anesu: 61, Kudzai: 55, Tinashe: 69, Tendai: 67, Chiedza: 76, Simbarashe: 64, Rudo: 71, Panashe: 59, Chipo: 70, Munashe: 65, Tapiwa: 60, Takudzwa: 54, Vimbai: 68 };
const scoreChange = { Chipo: -12, Tendai: -9, Nyasha: -8, Tanaka: -3, Tapiwa: 1 };
const subjectOffset = { Mathematics: 0, "English Language": 3, "Combined Science": -2, "Heritage Studies": 2, "Shona Language": 4 };
const assessments = [];
for (const student of students) {
  for (const subject of subjects) {
    const previous = scoreBase[student.first_name] + subjectOffset[subject];
    const current = previous + (scoreChange[student.first_name] ?? 2);
    [previous - 1, previous + 1, current - 1, current + 1].forEach((score, index) => assessments.push({
      ...student, subject, date: assessmentDates[index], score,
    }));
  }
}

function toCsv(rows, columns) {
  const quote = (value) => {
    const text = String(value);
    return /[",\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
  };
  return [columns.join(","), ...rows.map((row) => columns.map((column) => quote(row[column])).join(","))].join("\n") + "\n";
}

const files = {
  "attendance.csv": toCsv(attendance, ["student_id", "first_name", "class_name", "date", "status"]),
  "behaviour.csv": toCsv(behaviour, ["student_id", "first_name", "class_name", "date", "incident_type", "severity"]),
  "assessments.csv": toCsv(assessments, ["student_id", "first_name", "class_name", "subject", "date", "score"]),
};

await fs.mkdir(outputDir, { recursive: true });
for (const [name, content] of Object.entries(files)) await fs.writeFile(path.join(outputDir, name), content, "utf8");

const sha256 = (content) => crypto.createHash("sha256").update(content, "utf8").digest("hex");
const manifest = {
  schema_version: "1.0.0",
  dataset_name: "Veriq Zimbabwe Secondary Judge Dataset",
  school: "Prince High (fictional)",
  geography: "Harare, Zimbabwe (scenario only)",
  reporting_period: "Term 2 evidence, June-July 2026",
  generation_method: "Deterministic scenario generator; no source learner records and no random values",
  learners: students.length,
  classes: 4,
  subjects,
  records: { attendance: attendance.length, behaviour: behaviour.length, assessments: assessments.length },
  intended_scenarios: {
    connected_high_attention: ["Chipo", "Tendai", "Nyasha"],
    single_signal_watch: ["Tapiwa", "Tanaka"],
    stable_controls: students.map((student) => student.first_name).filter((name) => !["Chipo", "Tendai", "Nyasha", "Tapiwa", "Tanaka"].includes(name)),
  },
  files: Object.fromEntries(Object.entries(files).map(([name, content]) => [name, { sha256: sha256(content) }])),
};
await fs.writeFile(path.join(outputDir, "dataset_manifest.json"), JSON.stringify(manifest, null, 2) + "\n", "utf8");
console.log(JSON.stringify({ outputDir, ...manifest.records, learners: manifest.learners, classes: manifest.classes }, null, 2));
