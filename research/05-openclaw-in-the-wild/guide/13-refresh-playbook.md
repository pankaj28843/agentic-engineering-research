# Refresh Playbook

## Why this theme needs refreshing

OpenClaw is moving quickly. Public examples, provider policies, channel plugins, browser behavior, and skill catalogs can change within weeks. A static report will become stale if it treats today's showcase as a permanent map. The right posture is to refresh the evidence periodically and preserve the distinction between official claims, technical artifacts, community sentiment, and verified practitioner usage.

This chapter records a repeatable refresh workflow so future research can update the theme without starting over.

## Refresh cadence

Refresh monthly while OpenClaw is changing quickly, or before making a serious adoption decision. Refresh sooner if there is a major release, policy controversy, security report, new channel connector, or browser-tool change. For a personal project, a lightweight refresh may be enough. For a team adopting OpenClaw as infrastructure, refresh the operational and security chapters before deployment.

## Search plan

Run CDP-based browser discovery first, but expect blockers. Use the query family from the research log and add current date terms such as `2026`, `last month`, or release names. Try Google, Bing, Brave, DuckDuckGo, and Kagi through the CDP workflow if supported. Record blocked, empty, or irrelevant results. Do not silently substitute snippets for source content.

Then use source-native discovery. Search GitHub repositories, issues, pull requests, and discussions. Search official docs through docsearch. Search HN through Algolia. Search Reddit and X through the user's social archive when available. Search Stack Overflow through the Stack Exchange API. Search YouTube with CDP-rendered pages, but treat transcript-free or bot-blocked pages as weak evidence.

## What changed since last time

When refreshing, do not only append sources. Ask what changed.

Did the official showcase add new categories? Did existing examples gain repos? Did any showcased repos become archived? Did channel connectors add releases or issues? Did browser docs change profile, CDP, or Playwright behavior? Did deployment samples add hardening, guardrails, or multi-user support? Did issue searches reveal a recurring failure? Did social discussion shift from excitement to complaints or from demos to production reports?

Write those deltas into `research-log.md` and update `briefing.md` if the verdict changes.

## Evidence upgrade rules

Promote evidence when it gains reproducibility. A social post becomes stronger if it links to a repo. A repo becomes stronger if it adds installation commands, tests, release tags, or issue activity. A catalog entry becomes stronger if it links to a maintained skill. A browser demo becomes stronger if it includes traces, code, or a written walkthrough.

Downgrade evidence when it loses support. An archived repo, broken install command, dead link, bot-only issue stream, or extraction failure should reduce confidence. Do not delete stale examples automatically; mark them as stale if they shaped prior conclusions.

## Browser reliability refresh

Always keep browser reliability notes separate from product conclusions. If Google blocks CDP again, record it. If YouTube begins rendering transcripts, record that. If X requires login or produces only short text, record that. If official docs change from static to JS-heavy pages, record extraction quality. The user explicitly asked to capture failure modes for JS-heavy pages; that remains part of the evidence.

A failure to render a page is not evidence that the page lacks content. It is evidence that the research method could not inspect it in that mode. The report should say so.

## Source files to update

Update `sources.json` with new source records. Update `source-index.md` with quality labels and artifact paths. Update `research-log.md` with commands, results, and limitations. Update `briefing.md` if the top-level verdict changes. Update guide chapters only when the user-facing lesson changes, not for every new link.

Keep bulky raw artifacts in `tmp/search-web-cdp/openclaw-in-the-wild/`. Do not commit rendered page dumps. If a future extraction script post-processes articles, note the command and artifact paths.

## Questions for future refreshes

The most important unanswered question is whether OpenClaw develops more independent production case studies. Look for posts that include real duration, failure rates, maintenance burden, and before/after workflow comparisons. Also watch for security incidents, channel-plugin maturity, browser automation reliability, model-provider policy constraints, and whether skill catalogs converge on quality standards.

The second question is whether OpenClaw remains a personal assistant gateway or becomes a broader team/enterprise agent runtime. Deployment samples and enterprise chat connectors point in that direction, but public proof is still uneven.

The third question is whether browser automation remains central. If more workflows move to APIs and CLIs, OpenClaw may become safer and more reliable. If more workflows depend on signed-in browser sessions, the security chapter becomes even more important.
