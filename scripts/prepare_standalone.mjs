import { cpSync, existsSync, mkdirSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const standaloneRoot = resolve(root, ".next", "standalone");
const staticSource = resolve(root, ".next", "static");
const staticTarget = resolve(standaloneRoot, ".next", "static");
const publicSource = resolve(root, "public");
const publicTarget = resolve(standaloneRoot, "public");

if (!existsSync(standaloneRoot)) {
  throw new Error("The Next.js standalone output is missing. Run next build first.");
}

mkdirSync(resolve(standaloneRoot, ".next"), { recursive: true });
cpSync(staticSource, staticTarget, { recursive: true, force: true });
if (existsSync(publicSource)) {
  cpSync(publicSource, publicTarget, { recursive: true, force: true });
}

console.log("Prepared Next.js standalone static assets.");
