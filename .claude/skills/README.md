# Committed Agent Skills

## Tavily

Six skills vendored from [`tavily-ai/skills`](https://github.com/tavily-ai/skills),
installed via `npx skills add tavily-ai/skills --skill '*' --agent claude-code`.

| Skill | Purpose |
| --- | --- |
| `tavily-search` | Web search, URL reading, site page discovery |
| `tavily-research` | Cited multi-source research reports |
| `tavily-sdk` | Reference docs for building Tavily into application code |
| `tavily-entity` | Enrich a company/person/org record from the web |
| `tavily-list` | Build a deduplicated table of matches for a set |
| `tavily-monitor` | Recurring search/extraction against a saved baseline |

### Runtime dependency

All except `tavily-sdk` declare `allowed-tools: Bash(tvly *)` and shell out to the
Tavily CLI. **The CLI is not vendored here** — it is a Python package and must be
present in whatever environment the skills run in:

```bash
curl -fsSL https://cli.tavily.com/install.sh | bash   # installs `tvly` to ~/.local/bin
```

`tavily-sdk` is documentation only and needs no CLI.

### Authentication

`tvly search` and `tvly extract` work keyless (rate-limited). `map`, `crawl` and
`research` require a credential. The CLI reads `TAVILY_API_KEY`, or stores a key via
`tvly login`.

Browser OAuth (`tvly login` with no arguments) **cannot complete in a cloud
session** — it waits on a loopback callback that an external browser cannot reach.
In Claude Code cloud sessions, save the key as a network secret on the environment
instead; the egress proxy then attaches it to `api.tavily.com` requests, and
`TAVILY_API_KEY` only needs a format-correct placeholder so the CLI's local check
passes. Never commit a real key.

### Network access

Tavily hosts must be reachable: `api.tavily.com` (API), `cli.tavily.com`
(installer), `mcp.tavily.com` (OAuth bridge).
