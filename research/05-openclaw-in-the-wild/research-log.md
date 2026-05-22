# Research Log: OpenClaw in the Wild

## Task framing

The user requested practitioner-first research on how OpenClaw is being used in the wild across education, research, workflows, automation, developer productivity, personal planner behavior, browser automation, and adjacent data-extraction patterns. The work was treated as a durable repository theme, not a chat-only answer.

## CDP and tool preflight

Required tools were available: `cdp`, `jq`, `gh`, and `socli`. `docsearch find "OpenClaw" --json` found an `openclaw` tenant with documentation pages. Headless CDP daemon status and health were green before browser extraction.

Relevant artifacts:

- `tmp/search-web-cdp/openclaw-in-the-wild/cdp-health.json`
- `tmp/search-web-cdp/openclaw-in-the-wild/source-selection-ledger.md`
- `tmp/search-web-cdp/openclaw-in-the-wild/extracted-pages-ledger.md`

## Query batches

Scratch root: `tmp/search-web-cdp/openclaw-in-the-wild/`

### General web CDP batch

```text
OpenClaw being used in the wild practitioners
OpenClaw official docs showcase examples
OpenClaw GitHub examples automation workflow
OpenClaw browser automation data extraction
OpenClaw education research demo lesson plan
OpenClaw personal planner workflow automation
OpenClaw issues discussions workaround
OpenClaw YouTube demo Reddit Hacker News Stack Overflow X
site:github.com OpenClaw
site:reddit.com OpenClaw OR site:news.ycombinator.com OpenClaw
```

Command shape:

```bash
cdp --browser-mode headless workflow web-research serp   --query-file tmp/search-web-cdp/openclaw-in-the-wild/queries.txt   --result-pages 3   --serp google   --max-candidates 120   --candidate-out tmp/search-web-cdp/openclaw-in-the-wild/candidates-google.json   --out-dir tmp/search-web-cdp/openclaw-in-the-wild/google   --parallel 1   --min-visible-words 50   --min-html-chars 1000   --min-markdown-words 50   --json > tmp/search-web-cdp/openclaw-in-the-wild/serp-summary-google.json
```

Google result: all 30 scheduled SERP pages were blocked by consent, CAPTCHA, auth, or bot-check signals. No Google candidates were used.

### Alternate CDP search engines

The same query file was run against `bing`, `brave`, `duckduckgo`, and `kagi` using the same CDP SERP workflow.

Results:

- Bing: completed, zero useful candidates.
- Brave: completed, zero useful candidates.
- DuckDuckGo: returned five generic DuckDuckGo-owned results, rejected as irrelevant.
- Kagi: failed/blocked in this session.

This means the web-search portion had low yield, but the failure itself is documented rather than hidden.

## Native source discovery

Because general SERPs were weak or blocked, source-native discovery carried the research:

- `docsearch find "OpenClaw" --json` and `docsearch search-all "OpenClaw examples showcase automation planner browser" --json` found official docs and showcase pages.
- `gh search repos OpenClaw --limit 50 --json ...` found the main repo, skill catalogs, channel connectors, deployment projects, education/tutorial projects, and many derivatives.
- `gh search issues OpenClaw --limit 80 --json ...` found setup failures, integration requests, bot-generated trending notices, policy bypass reports, and config/crons work.
- HN Algolia found a high-engagement OpenClaw controversy thread but little concrete deployment proof.
- `socli research "OpenClaw" --limit 50 --json` found HN, Reddit, and X discussion. Reddit and X hits mostly showed attention, troubleshooting, model/provider discussion, and policy controversy rather than detailed war stories.
- Stack Overflow API found five relevant or adjacent questions, including WordPress automation curiosity and a broader Django/Docker/Celery AI-workflow question.

## Extraction

Selected source URLs were written to `tmp/search-web-cdp/openclaw-in-the-wild/visit-urls.txt` and extracted with:

```bash
cdp --browser-mode headless workflow web-research extract   --url-file tmp/search-web-cdp/openclaw-in-the-wild/visit-urls.txt   --max-pages 80   --parallel 4   --selector body   --out-dir tmp/search-web-cdp/openclaw-in-the-wild/pages   --min-visible-words 20   --min-html-chars 500   --min-markdown-words 20   --json > tmp/search-web-cdp/openclaw-in-the-wild/extract-summary.json
```

Initial extraction captured 36 pages, then reported daemon disconnect failures for several X URLs and left 28 remaining URLs. A retry with parallel 2 succeeded for the remaining 28 pages:

```bash
cdp --browser-mode headless workflow web-research extract   --url-file tmp/search-web-cdp/openclaw-in-the-wild/pages/remaining-urls.txt   --max-pages 40   --parallel 2   --selector body   --out-dir tmp/search-web-cdp/openclaw-in-the-wild/pages-retry   --min-visible-words 20   --min-html-chars 500   --min-markdown-words 20   --json > tmp/search-web-cdp/openclaw-in-the-wild/extract-retry-summary.json
```

## Browser/headless reliability notes

- CDP headless health was healthy before browsing.
- Google was blocked across the whole SERP batch. Kagi also failed/blocked. Bing and Brave returned no candidates. DuckDuckGo returned irrelevant candidates.
- Official docs rendered cleanly through CDP and provided rich Markdown/visible text.
- GitHub pages rendered well enough for repository and issue evidence.
- YouTube watch pages were unreliable under headless extraction: one showed consent/bot-check warning, and two produced zero visible text. YouTube evidence is therefore treated as official-showcase-linked, not transcript-backed.
- Several X pages initially failed with daemon disconnect during high parallel extraction; retrying remaining URLs with lower parallelism succeeded. X pages still have limited visible text, so the official showcase summaries carry more weight than X captures alone.

## Limitations

- Public search coverage is incomplete because major SERPs were blocked or unproductive in headless CDP.
- Some GitHub search results appear inflated or noisy, including bot-generated trending issues and catalogs. The report avoids using those as proof of production adoption.
- Official showcase examples are valuable but curated by the project. They show what people submitted or what maintainers selected, not unbiased prevalence.
- Social sources are strong for sentiment and controversy but weak for detailed reproducible workflows.
- This research did not install or run OpenClaw locally. It studied published sources, CDP-rendered pages, GitHub metadata, and community artifacts.

## Validation

Repository validation command run after authoring:

```bash
uv run python scripts/validate_research.py
```

Result recorded after completion in the session output.
