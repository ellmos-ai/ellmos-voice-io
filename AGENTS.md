# Agent instructions

- Keep all voice engines optional and lazily imported.
- Preserve the no-storage, no-telemetry, no-implicit-network boundary.
- Do not embed model files, credentials, account IDs, user paths, or microphone permissions.
- Keep the package LLM-neutral; adapters belong in the consuming MCP or application.
- Run `python -m pytest` and `python -m compileall src` before committing.
