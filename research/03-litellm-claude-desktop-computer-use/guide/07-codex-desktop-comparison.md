# 07. Codex Desktop computer use as a separate product path

Codex Desktop computer use should be evaluated, but not as evidence for the Anthropic/LiteLLM computer-use bridge. It is a separate product path with its own app, plugin system, helper process, permissions, feature gates, and failure modes.

OpenAI has an official Codex app computer-use documentation surface ([Codex computer use](https://developers.openai.com/codex/app/computer-use)) and broader Codex app feature docs ([Codex features](https://developers.openai.com/codex/app/features)). The product announcement context also frames Codex as an app-level workflow, not just a generic API endpoint ([Codex for almost everything](https://openai.com/index/codex-for-almost-everything/)).

That makes Codex Desktop a good comparison for user experience. It does not make it a drop-in substitute for Anthropic's `computer_20251124` beta Messages API tool.

## What Codex can answer

Codex Desktop can answer questions like:

- Can a Mac app agent operate local apps well enough for real tasks?
- What permissions does it need?
- Does it steal cursor/focus?
- How stable is the bundled computer-use plugin?
- Does it work with the user's ChatGPT account and region?
- How does it compare with Claude Desktop and open-source runtimes?

Those are valuable product questions.

## What Codex cannot answer

Codex Desktop cannot answer:

- Does LiteLLM preserve `anthropic-beta` headers?
- Does a ChatGPT-backed LiteLLM route accept `computer_20251124` tool definitions?
- Does the Anthropic computer-use demo parse the backend response?
- Does Claude Desktop third-party inference expose a computer-use loop?

Those are Anthropic API / LiteLLM bridge questions. Codex may use related underlying ideas, but the integration boundary is different.

## The plugin-unavailable failure mode

The most important GitHub issue found was `openai/codex#18258`, where users report the Codex app on macOS showing `Computer Use plugin unavailable` ([openai/codex#18258](https://github.com/openai/codex/issues/18258)). The issue body and comments mention several concrete failure clues:

- Settings shows `Computer Use plugin unavailable`.
- Plugin search returns no `computer use` result.
- Bundled plugin files may exist inside the app bundle.
- The expected cache path under `~/.codex/plugins/cache/openai-bundled/computer-use` may be missing.
- The helper app `Codex Computer Use.app` may need local registration.
- Region notes mention unavailability in EEA/UK/Switzerland at launch.
- Some users report partial backend behavior even while the UI still says unavailable.
- Build/architecture issues may affect whether the bundled plugin exists.

This is exactly why Codex Desktop should get its own decision log. A failure could be a region gate, a plugin cache issue, a helper registration issue, a macOS TCC permission issue, an app version issue, or an actual product limitation.

## Permissions and helper state

Computer-use products on macOS often need Accessibility and Screen Recording permissions. The open-source `open-codex-computer-use` README explicitly tells macOS users to grant Accessibility and Screen Recording on first run ([open-codex-computer-use](https://github.com/iFurySt/open-codex-computer-use)). Codex Desktop likely has its own helper and permission story.

A Codex experiment should record:

```text
Codex app version:
Codex CLI version:
macOS version:
CPU architecture:
Region/account:
Computer Use settings state:
Plugin marketplace state:
Helper app present:
Helper app registered:
Accessibility permission:
Screen Recording permission:
App logs inspected:
First task result:
```

That may feel tedious, but it prevents a false conclusion like "Codex computer use does not work" when the real problem is a missing helper app or region gate.

## Safe first task

Like Anthropic computer use, Codex should start with a low-stakes local task:

```text
Open TextEdit, type "codex computer use ok", and stop.
```

Do not start with logging into accounts, checking balances, downloading files, or handling private browser sessions. The OpenClaw issue discussion includes examples like checking a console balance or filling a form, but those should come after basic capability and permission checks ([OpenClaw issue 67776](https://github.com/openclaw/openclaw/issues/67776)).

## Cursor and focus concerns

Computer-use systems that rely on screenshots and coordinate clicks can take over the user's active desktop. A comment in the OpenClaw issue captured the practical problem: coordinate-based screenshot-then-click loops can hijack the user's cursor and focus, while Accessibility APIs can target many real Mac UI elements semantically and avoid cursor theft for many tasks ([OpenClaw issue 67776](https://github.com/openclaw/openclaw/issues/67776)).

Codex Desktop should be judged partly on this UX dimension:

- Does it take over the user's cursor?
- Can it run in a separate desktop/Space?
- Can the user continue working?
- Are actions visible and interruptible?
- Can it target UI semantically or only by coordinates?

This is not a minor UX detail. It determines whether computer use is usable while the human is working.

## Comparing Codex with Claude Desktop

Claude Desktop third-party inference through LiteLLM is a text-routing experiment. Codex Desktop computer use is an app automation experiment. The comparison should be framed like this:

| Question | Claude Desktop through LiteLLM | Codex Desktop computer use |
|---|---|---|
| Main purpose | Route chat/inference through a gateway. | Operate local apps/computer. |
| Evidence source | LiteLLM Claude Desktop docs. | OpenAI Codex docs and app behavior. |
| Key setup | Gateway URL + virtual key. | App/plugin/helper/permissions. |
| Main risk | Gateway/auth/model alias mismatch. | Permission/plugin/region/product instability. |
| Computer-use proof? | No, not by itself. | Product proof only, not Anthropic API proof. |

## When Codex is the better path

Codex may be the better path if the user's goal is immediate Mac desktop automation and the product works in their region/account. A product-built helper may be smoother than adapting a beta API demo through a non-native gateway.

But if the user's goal is to learn or productize Anthropic-compatible computer-use loops, Codex is a comparison, not the main path. The main path remains the official Anthropic demo and API contract.

## What to do with Codex results

Record Codex results in a separate ledger:

```text
Codex Desktop product result: pass/fail/partial
Anthropic computer-use API result: pass/fail/partial
LiteLLM proxy adaptation result: pass/fail/partial
Open-source runtime result: pass/fail/partial
```

Do not merge those into one "computer use works" row. That is how product features and API contracts get confused.
