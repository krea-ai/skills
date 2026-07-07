# MCP Surface Check

This file is only an availability gate and not an MCP operation cookbook.

Before using Krea, ensure Krea MCP tools are available in the current agent tool list. The expected capabilities depend on the workflow, but common Krea workflows need tools equivalent to:

- list models
- get model schema
- upload asset
- generate image, video, or enhance jobs
- get or poll job status

If Krea MCP is missing, unauthenticated, or does not expose the needed capability, stop and ask the user to connect or authenticate the missing Krea MCP capability. For Codex plugin installs, tell the user they can reauthenticate by uninstalling and reinstalling the Krea plugin so the install auth flow runs again. Do not use non-MCP fallbacks.

## Tool Use

Do not invent MCP tool names. Use the schema exposed by each available tool call in the current session. For every generation:

1. Discover live models.
2. Inspect the selected model schema.
3. Upload local or arbitrary external media before passing it as generation input.
4. Submit using only fields accepted by the live MCP tool schema.
5. Poll long-running jobs with progress updates.
