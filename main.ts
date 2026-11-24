// post-meme-entry: carry the entry's X post address into the grading sandbox.
//
// The house grades this bounty by reading POST.json itself (and the post it
// names, through FxTwitter). This program does exactly one job: copy the
// repository's POST.json, byte for byte, into the harness output directory,
// so the sealed scorer finds it there. No network, no timestamps, no
// randomness: two runs write the same bytes.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));

function repoRoot(): string {
  // The entrypoint lives at the repository root; fall back to the working
  // directory so a local run from the repo root behaves the same.
  return HERE;
}

function outputDir(): string {
  const fromEnv = process.env.MAKEFUN_OUTPUT_DIR;
  if (fromEnv !== undefined && fromEnv.length > 0) return fromEnv;
  return "/output";
}

function carryPostFile(): void {
  const source = join(repoRoot(), "POST.json");
  const raw = readFileSync(source);
  const parsed: unknown = JSON.parse(new TextDecoder().decode(raw));
  if (
    typeof parsed !== "object" ||
    parsed === null ||
    typeof (parsed as { url?: unknown }).url !== "string"
  ) {
    throw new Error("POST.json must be a JSON object with a string url");
  }
  const target = outputDir();
  mkdirSync(target, { recursive: true });
  writeFileSync(join(target, "POST.json"), raw);
  console.log(`carried POST.json (${raw.length} bytes) to ${target}`);
}

carryPostFile();
