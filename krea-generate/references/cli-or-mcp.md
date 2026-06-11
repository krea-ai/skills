# CLI Or MCP — Surface Check

This file is only an availability gate. It is not a CLI command reference and not an MCP operation cookbook.

Before using Krea, ensure one usable surface is present:

1. An authenticated Krea CLI is installed, or
2. Krea MCP tools are available in the current agent tool list.

If neither surface is present, stop and ask the user to install/authenticate the CLI or connect the Krea MCP. Do not fall back to raw HTTP unless the active workflow explicitly says to use a direct API path, such as LoRA training.

## CLI Surface

Check that `krea` exists and can reach the API:

```bash
command -v krea
krea doctor
```

If CLI auth fails, ask the user to run `krea auth login` or provide the expected Krea API key through their normal environment setup.

When using the CLI, discover command shapes from the installed CLI itself:

```bash
krea --help
krea models --help
krea generate --help
krea jobs --help
```

Then inspect live model schemas before generation. Do not rely on remembered flags, examples from old transcripts, or this skill file as a source of CLI syntax.

## MCP Surface

Use MCP only when Krea MCP tools are actually available in the current tool list. The expected capabilities depend on the workflow, but common Krea workflows need tools equivalent to:

- list models
- get model schema
- upload asset
- generate image, video, or enhance jobs
- get or poll job status

Do not invent MCP tool names. If a Krea MCP tool is available, use the schema exposed by that tool call in the current session. If the needed MCP capability is missing, use the CLI if available; otherwise stop and ask the user to connect the missing Krea MCP capability.

## Surface Choice

Use whichever surface is available and fits the current workflow. If both are available, choose the surface that is easiest to verify and automate in the current agent environment.

Regardless of surface:

1. Discover live models.
2. Inspect the selected model schema.
3. Upload local or arbitrary external media before passing it as generation input.
4. Submit using only fields accepted by the live CLI help/schema or MCP tool schema.
5. Poll long-running jobs with progress updates.
