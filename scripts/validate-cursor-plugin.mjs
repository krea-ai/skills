#!/usr/bin/env node

import { promises as fs } from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const manifestPath = path.join(repoRoot, ".cursor-plugin", "plugin.json");
const mcpPath = path.join(repoRoot, "mcp.json");
const expectedSkills = new Set([
  "./krea-generate",
  "./krea-marketing",
  "./krea-motion",
  "./product-packaging-design",
]);
const allowedManifestFields = new Set([
  "name",
  "displayName",
  "version",
  "description",
  "author",
  "homepage",
  "repository",
  "license",
  "keywords",
  "logo",
  "rules",
  "agents",
  "skills",
  "commands",
  "hooks",
  "mcpServers",
  "variables",
]);
const errors = [];

function addError(message) {
  errors.push(message);
}

async function readJson(filePath, label) {
  let raw;
  try {
    raw = await fs.readFile(filePath, "utf8");
  } catch (error) {
    addError(`${label} is missing: ${path.relative(repoRoot, filePath)}`);
    return null;
  }

  try {
    return JSON.parse(raw);
  } catch (error) {
    addError(`${label} contains invalid JSON: ${error.message}`);
    return null;
  }
}

function resolveSafeRelativePath(rawPath, label) {
  if (typeof rawPath !== "string" || rawPath.length === 0 || path.isAbsolute(rawPath)) {
    addError(`${label} must be a non-empty relative path`);
    return null;
  }

  const resolved = path.resolve(repoRoot, rawPath);
  const relative = path.relative(repoRoot, resolved);
  if (relative.startsWith("..") || path.isAbsolute(relative)) {
    addError(`${label} must stay within the plugin root: ${rawPath}`);
    return null;
  }
  return resolved;
}

async function assertFile(filePath, label) {
  try {
    const stat = await fs.stat(filePath);
    if (!stat.isFile()) {
      addError(`${label} is not a file: ${path.relative(repoRoot, filePath)}`);
    }
  } catch {
    addError(`${label} does not exist: ${path.relative(repoRoot, filePath)}`);
  }
}

function parseFrontmatter(markdown) {
  const normalized = markdown.replace(/\r\n/g, "\n");
  if (!normalized.startsWith("---\n")) return null;
  const end = normalized.indexOf("\n---\n", 4);
  if (end === -1) return null;

  const fields = {};
  for (const line of normalized.slice(4, end).split("\n")) {
    const separator = line.indexOf(":");
    if (separator === -1) continue;
    const key = line.slice(0, separator).trim();
    const value = line.slice(separator + 1).trim().replace(/^(["'])(.*)\1$/, "$2");
    fields[key] = value;
  }
  return fields;
}

async function validateSkill(rawPath) {
  const skillRoot = resolveSafeRelativePath(rawPath, `skills entry ${rawPath}`);
  if (!skillRoot) return;

  const skillMdPath = path.join(skillRoot, "SKILL.md");
  let markdown;
  try {
    markdown = await fs.readFile(skillMdPath, "utf8");
  } catch {
    addError(`${rawPath} must contain SKILL.md`);
    return;
  }

  const frontmatter = parseFrontmatter(markdown);
  if (!frontmatter) {
    addError(`${rawPath}/SKILL.md must contain YAML frontmatter`);
    return;
  }
  if (!frontmatter.name || !/^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/.test(frontmatter.name)) {
    addError(`${rawPath}/SKILL.md has an invalid or missing frontmatter name`);
  }
  if (!frontmatter.description) {
    addError(`${rawPath}/SKILL.md is missing a frontmatter description`);
  }
}

async function validateManifest(manifest) {
  if (!manifest || typeof manifest !== "object" || Array.isArray(manifest)) return;

  for (const field of Object.keys(manifest)) {
    if (!allowedManifestFields.has(field)) {
      addError(`Cursor manifest contains undocumented field: ${field}`);
    }
  }

  if (manifest.name !== "krea") addError('Cursor manifest name must be "krea"');
  if (typeof manifest.description !== "string" || !manifest.description.trim()) {
    addError("Cursor manifest description is required for marketplace review");
  }
  if (typeof manifest.version !== "string" || !/^\d+\.\d+\.\d+$/.test(manifest.version)) {
    addError("Cursor manifest version must be semantic versioning");
  }
  if (!manifest.author || typeof manifest.author.name !== "string" || !manifest.author.name.trim()) {
    addError("Cursor manifest author.name is required");
  }
  if (manifest.license !== "MIT") addError('Cursor manifest license must be "MIT"');

  if (!Array.isArray(manifest.skills)) {
    addError("Cursor manifest skills must explicitly list the top-level skill directories");
  } else {
    const actualSkills = new Set(manifest.skills);
    if (actualSkills.size !== manifest.skills.length) {
      addError("Cursor manifest skills must not contain duplicate paths");
    }
    for (const expected of expectedSkills) {
      if (!actualSkills.has(expected)) addError(`Cursor manifest is missing skill path: ${expected}`);
    }
    for (const actual of actualSkills) {
      if (!expectedSkills.has(actual)) addError(`Cursor manifest has an unexpected skill path: ${actual}`);
    }
    await Promise.all(manifest.skills.map(validateSkill));
  }

  const logoPath = resolveSafeRelativePath(manifest.logo, "Cursor manifest logo");
  if (logoPath) await assertFile(logoPath, "Cursor manifest logo");
}

async function validateMcp(mcp) {
  const krea = mcp?.mcpServers?.krea;
  if (!krea || typeof krea !== "object" || Array.isArray(krea)) {
    addError('mcp.json must define an "mcpServers.krea" object');
    return;
  }
  if (krea.url !== "https://api.krea.ai/mcp") {
    addError("mcp.json must point Krea at https://api.krea.ai/mcp");
  }
  const unsupportedFields = Object.keys(krea).filter((field) => field !== "url");
  if (unsupportedFields.length > 0) {
    addError(`Cursor Krea MCP config contains unnecessary fields: ${unsupportedFields.join(", ")}`);
  }

  for (const providerPath of [".mcp.json", ".codex-plugin/.mcp.json"]) {
    const providerConfig = await readJson(path.join(repoRoot, providerPath), providerPath);
    if (providerConfig?.mcpServers?.krea?.url !== krea.url) {
      addError(`${providerPath} Krea MCP URL does not match mcp.json`);
    }
  }
}

const [manifest, mcp] = await Promise.all([
  readJson(manifestPath, "Cursor plugin manifest"),
  readJson(mcpPath, "Cursor MCP config"),
]);

await validateManifest(manifest);
await validateMcp(mcp);

if (errors.length > 0) {
  console.error("Cursor plugin validation failed:");
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log("OK Cursor plugin manifest, skills, logo, and Krea MCP configuration");
