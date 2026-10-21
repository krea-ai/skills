#!/usr/bin/env node

import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const readJson = (file) => JSON.parse(readFileSync(path.join(root, file), "utf8"));
const manifest = readJson(".claude-plugin/plugin.json");
const marketplace = readJson(".claude-plugin/marketplace.json");
const mcp = readJson(".mcp.json");
const version = readFileSync(path.join(root, "VERSION"), "utf8").trim();

assert.equal(manifest.name, "krea");
assert.equal(manifest.version, version);
assert.equal(manifest.mcpServers, "./.mcp.json");
assert.ok(manifest.description.trim());
assert.equal(marketplace.plugins.length, 1);
assert.equal(marketplace.plugins[0].name, manifest.name);
assert.equal(marketplace.plugins[0].source, "./");
assert.equal(marketplace.plugins[0].version, version);
assert.equal(marketplace.plugins[0].description, manifest.description);

for (const config of [manifest, marketplace.plugins[0]]) {
  for (const field of ["skills", "commands", "agents", "hooks", "lspServers"]) {
    assert.ok(!(field in config), `Claude connector must not load ${field}`);
  }
}

for (const entry of ["skills", "commands", "agents", "hooks", "SKILL.md", ".lsp.json"]) {
  assert.ok(!existsSync(path.join(root, entry)), `Claude must not auto-load ${entry}`);
}

assert.deepEqual(mcp, {
  mcpServers: {
    krea: {
      type: "http",
      url: "https://api.krea.ai/claude-mcp",
      oauth_resource: "https://api.krea.ai/claude-mcp",
    },
  },
});

for (const file of ["mcp.json", ".codex-plugin/.mcp.json"]) {
  assert.equal(readJson(file).mcpServers.krea.url, "https://api.krea.ai/mcp");
}

console.log("OK Claude connector scope, marketplace, OAuth resource, and client isolation");
