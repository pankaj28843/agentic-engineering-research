# Browser Automation

## The browser as universal adapter

OpenClaw's browser story matters because many real tasks do not have clean APIs. Shopping sites, school portals, dashboards, financial charts, internal tools, and consumer services often expose the important action only through a web UI. The official [OpenClaw browser documentation](https://docs.openclaw.ai/tools/browser) describes a controlled browser surface that can open tabs, inspect pages, take screenshots, click, type, drag, select, handle downloads, inspect cookies/storage, and route through local, remote, or existing browser profiles. That is the technical foundation underneath showcase examples like Tesco shopping autopilot, TradingView chart analysis, ParentPay school meals, and browser-based account work.

The key practitioner insight is that browser automation should be treated as a last-mile adapter, not as a magic substitute for APIs. If a site has a stable API or local CLI, use that first. If no API exists, a browser may be the only practical way to automate the user's real workflow. But browser automation inherits every fragility of the page: login state, layout changes, modals, consent banners, anti-bot checks, two-factor prompts, slow network, and ambiguous UI labels.

## OpenClaw-managed profile versus user profile

The browser docs describe two major profile modes. The `openclaw` profile is a dedicated OpenClaw-managed browser profile. It is isolated from the user's personal browser and intended as the safer default. The `user` profile attaches to the user's real signed-in Chrome session through Chrome DevTools MCP. OpenClaw also supports custom profiles and remote CDP endpoints.

This distinction is critical. The isolated profile is the right default for repeatable automation because it avoids touching the user's daily browser state. It can have its own cookies, window color, CDP port, and lifecycle. The signed-in user profile is useful when the task needs existing login state, but it is higher risk. It can act inside accounts the user cares about. The docs explicitly note that the user should be present to approve attach prompts for existing sessions and that this path is more sensitive.

The CLI examples make this concrete. The [browser CLI reference](https://docs.openclaw.ai/cli/browser) shows commands such as `openclaw browser profiles`, `openclaw browser --browser-profile openclaw start`, `openclaw browser --browser-profile openclaw open https://example.com`, and `openclaw browser --browser-profile openclaw snapshot`. It also shows existing-session setup using `openclaw browser create-profile --name chrome-live --driver existing-session` and commands against `--browser-profile user`. For practitioners, those commands define a testable smoke path: list profiles, start the browser, open a page, snapshot it, then act only on visible refs.

## Ref-based action is safer than brittle selectors

OpenClaw's docs emphasize snapshots and refs. A browser snapshot returns a representation of the page with references, and actions such as `openclaw browser click <ref>` or `openclaw browser type <ref> "hello"` use those refs. The docs also describe role snapshots with refs like `e12`, interactive snapshots, labels, highlighting, and a warning that refs are not stable across navigations. This is a better practitioner interface than raw CSS selectors because it lets the agent reason from the visible UI tree rather than hidden DOM trivia.

But refs do not eliminate ambiguity. If a page has multiple similar buttons, a snapshot can still be confusing. If content changes after a click, old refs go stale. If an iframe contains the target, the snapshot may need frame scoping. If an action fails because the target is covered or not visible, the docs recommend taking another interactive snapshot, using `highlight`, inspecting errors and requests, or recording a trace. That is a mature reliability story: browser automation requires inspection loops, not blind clicking.

## Security controls

The browser docs include several controls that practitioners should not ignore. Browser control is loopback-only by default, and gateway auth applies to browser routes. Remote CDP URLs and tokens are secrets. The docs describe SSRF policy controls, including a stricter mode where private/internal destinations can be blocked unless allowlisted. They also warn that `evaluate` and wait predicates execute JavaScript in the page context and can be disabled with `browser.evaluateEnabled=false` if not needed.

These details matter because a browser tool can become a network pivot or account-control surface. A malicious page can try to prompt the agent into revealing data or executing unsafe JS. A remote CDP token can provide deep control over a browser session. A default-profile attach can manipulate signed-in accounts. The safe posture is: isolate by default, turn on strict SSRF when browsing untrusted sites, avoid arbitrary page JS unless required, keep tokens out of config files, and require confirmation before irreversible actions.

## Browserless, Browserbase, and remote CDP

The docs describe remote CDP profiles for hosted or remote browsers, including Browserless and direct WebSocket providers such as Browserbase. This is important for server deployments where Chrome cannot or should not run on the gateway machine. It also matters for tasks that need cloud browsers, geographies, or heavier browser infrastructure.

Remote browser control changes the threat model. Local loopback control is easier to reason about. Remote CDP introduces network reliability, token secrecy, provider trust, and cost. If a task only needs a local logged-in site, remote CDP may be the wrong choice. If a task runs in a server-side agent and must browse without a desktop, remote CDP may be necessary. The practitioner should choose the browser location based on data sensitivity and operational needs, not novelty.

## In-the-wild browser examples

The official showcase gives several browser-shaped examples. Tesco shopping autopilot uses weekly meal plans, regular items, delivery slots, and order confirmation without APIs. ParentPay school meals uses mouse coordinates for reliable table-cell clicking. TradingView analysis logs into TradingView through browser automation, screenshots charts, and performs technical analysis. These examples demonstrate a lesson: some workflows are not about scraping public web pages. They are about operating a user's authenticated, stateful web tools.

Comparable data-extraction patterns sharpen the lesson. [SNAG](https://github.com/am-will/snag) turns a selected screen region into Markdown using a vision model. [apify-openclaw-plugin](https://github.com/apify/apify-openclaw-plugin) points toward actor-style data extraction. [Karakeep semantic search](https://github.com/jamesbrooksco/karakeep-semantic-search) turns saved knowledge into searchable vectors. These are not all browser automation in the same sense, but they share a theme: practitioners want agents to convert messy human-facing surfaces into structured, reusable information.

## Reliability notes from this research

The research itself used CDP and hit realistic web reliability problems. Official docs and GitHub pages rendered well. YouTube pages were problematic: one OpenClaw setup video page showed consent or bot-check signals, and two YouTube pages produced zero visible text under headless extraction. X pages initially failed during a parallel extraction batch because of daemon disconnects, then succeeded on retry with lower parallelism, but they still yielded limited visible text. Google SERP pages were blocked entirely by consent/CAPTCHA/bot-check signals.

This is not just a research footnote. It mirrors what OpenClaw users should expect in production browser workflows. The browser is powerful because it sees what humans see, but it also sees what humans suffer: consent dialogs, bot checks, blocked content, slow pages, and JS-heavy surfaces. Good OpenClaw browser workflows should record screenshots, visible text, network errors, and action traces when something fails. They should not silently skip a page and pretend the task completed.

## A safe browser automation checklist

Before trusting an OpenClaw browser workflow, answer these questions. Does it run in the isolated `openclaw` profile unless it truly needs the `user` profile? Does it have a fresh snapshot before each action? Does it require confirmation before purchase, booking, posting, or deletion? Does it log the final URL and screenshot? Does it handle login expiry? Does it expose tokens or remote CDP URLs? Does it disable arbitrary JS evaluation when unnecessary? Does it recover if the page layout changes?

If the answer is no, the workflow may still be a good demo, but it is not yet a dependable personal assistant. Browser automation is one of OpenClaw's most valuable surfaces precisely because it can cross the last mile. It deserves the same caution as any tool that can click inside your accounts.
