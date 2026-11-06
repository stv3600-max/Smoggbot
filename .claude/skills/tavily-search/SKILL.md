---
name: tavily-search
description: |
  Use this skill whenever a task needs the web: searching for information, checking current facts or news, finding sources, reading a URL, finding a page on a site, or collecting many pages from a site. Use it for anything past your training data or anything the user wants verified online.
allowed-tools: Bash(tvly *)
---

# Tavily search

Use the `tavily_search`, `tavily_extract`, `tavily_map` and `tavily_crawl` tools if your tool list has them
(some clients add a prefix such as `mcp__tavily__`). Otherwise run `tvly <command>` directly; there's no
need to check for it first. If neither works, follow [setup](references/setup.md).

Since CLI 0.2.1 the CLI detects that stdout is not a terminal — a pipe or a coding agent's shell — and prints
readable plain text instead of JSON: `search` prints each result's title, full URL and a snippet, `map` prints
one URL per line, `extract` and `crawl` print each page in full with links kept. Add `--json` only when you
need to parse specific fields; for reading, plain text costs far less context.

Parameters are named as in the API (`max_results`). The CLI spells them as flags (`--max-results`) with
comma-separated lists (`--include-domains sec.gov,reuters.com`). For exact parameters, read the tool schema,
run `tvly <command> --help`, or see the [API reference](https://docs.tavily.com/documentation/api-reference/endpoint/search).

| You have | You need | Use |
|---|---|---|
| A question or topic | Sources, facts or news | Search |
| URLs | Their content | Extract |
| A site, not the exact page | The right page's URL | [Map](references/map.md) |
| A site section | Many of its pages | [Crawl](references/crawl.md) |

## Search

**Use advanced search.** Set `search_depth` to `advanced` (`--depth advanced` in the CLI) for every search
unless the user needs a fast answer to a simple lookup. It reaches more sources and ranks the passages that match your query.

**Write queries for a search engine.** Use the names and terms you expect on the page, not the user's whole
request. Split a question with several parts into one focused search per part. For a long written report,
search each part separately and extract the main sources for each before you write.

**Follow your leads.** When a result names a likely answer, test it right away: search that name with the
other details you know, or extract its page. Keep a lead that fits most details until a source contradicts it; a detail you can't confirm doesn't rule it out. When a search misses,
search the details again in their own words before adding names or filters you guessed, and build lists of
candidates from results, not memory. When a detail keeps coming back empty, work out what it refers to, such as
the role, event or term, and search for that.

Each result's `content` is already the passages that match your query; print it whole rather than cutting it
short. In plain-text output `--max-chars` caps how much of each result's content is printed: it defaults to 600
and is shared across queries (300 each for 2, 200 for 3). Pass `--max-chars 0` to print content whole. `--json`
output and `-o` files are never truncated.

**Batch independent searches.** With MCP tools, issue separate `tavily_search` calls in one turn; they run in
parallel. With the CLI, pass up to 5 queries to a single `tvly search` call — they run in parallel with the same
options, so prefer this over several Bash calls, which run one after another:
`tvly search 'Rust 2024 edition release date' 'Rust 2024 edition new features' --depth advanced --max-results 10`.
Use separate calls only when the queries need different options. A lone `-` as the query reads it from stdin.
Don't add pipes, `&`, `$(...)` or other programs to a `tvly` call, which make the client ask for permission.
Put each query in single quotes.

**Ask for 10 results.** Set `max_results` to 10 (`--max-results 10`). **Narrow before you widen.** Filters help more than raising `max_results` further. Use `time_range` or dates for
recent events or a stated period. Use `include_domains` when the answer lives on an official or named site; it
is a hard filter, so search again without it if it doesn't find the page.

**Some parameters are API-only.** The API has `max_age_hours` for content freshness (1-720; `0` always fetches
the page live, `-1` never does) and `include_domains_mode: "prefer"` to boost domains instead of hard-filtering
them. CLI 0.2.1 exposes no flag for either. Run `tvly <command> --help` before assuming a flag exists, and use
an SDK or a direct API call when you need one of these.

**Keep large results on disk.** When a result is long, such as raw page content or a crawl, save it with
`-o <file>` and read the parts you need with your file-reading tool instead of printing it all. Bare `-o` with
no value saves the full JSON under `.tavily/` with a generated name and prints the path; pass an explicit path
when the file belongs somewhere specific, such as a scratch directory. To reuse a file,
use the path you wrote; never look for it with a glob over temp folders, which can read another task's files. An
MCP result lands straight in your context, so keep those calls small.

**Read the results critically.** Count independent sources, not results. Treat a generated answer as a summary
to check, never as a source.

## Extract

Extract returns up to 20 URLs per call as markdown, including pages built with JavaScript.

- Extract only the few results worth reading. Snippets answer most facts.
- Extract full pages by default. Pass `query` (`--query`) only to isolate one fact on a long page; if the passages come
  back cut off near what you need, extract again without it.
- Rerun with `extract_depth` set to `advanced` (`--extract-depth advanced`) when a page is built with JavaScript, the content is in a table, or
  `basic` came back empty. Check `failed_results` every time and say which pages couldn't be read.
- When you find a direct link to the data itself, such as a CSV or JSON file, download it if you can.

## When to stop

- Stop once two independent sources agree on a fact.
- Before you answer, close any gap your draft would mark unconfirmed or fill from memory: run one targeted
  search or reread the saved page.
- For releases, ownership, official figures and decisions by a named body, confirm on the official domain or
  repository. A secondary site or a generated answer is not enough.

## Hand off the job

When the user wants an in-depth report that needs many sources gathered and weighed, such as an analysis, a
comparison across several criteria or an in-depth investigation, use `tavily-research` instead of your own searches.
If it isn't installed, run `npx skills add tavily-ai/skills --skill tavily-research` and read its SKILL.md first. A
single fact or answer to find stays here.

---

**Local copy.** Vendored from `tavily-ai/skills`, then edited for Tavily CLI 0.2.1 (released 2026-10-30) to cover
plain-text output in agent shells, multi-query search, `--max-chars`, bare `-o`, and which parameters remain
API-only. This file therefore diverges from upstream. Re-check it against `tvly search --help` after `tvly update`.
