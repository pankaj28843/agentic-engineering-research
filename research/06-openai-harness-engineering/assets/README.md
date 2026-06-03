# Assets

These images are local copies for private study and ebook rendering. They are not original work by this repository. All five assets were exported from OpenAI's February 11, 2026 post, [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/), during the headed CDP evidence capture for this packet.

## OpenAI Blog Diagrams

| File | Dimensions | Source role | Durable interpretation |
|---|---:|---|---|
| `openai/codex-drives-app-cdp.webp` | 1600x1562 | OpenAI diagram of Codex driving an app through browser/CDP-like feedback | Teaches the observe, act, restart, revalidate loop: the agent needs a rendered app surface, not just source files. |
| `openai/local-observability-stack.svg` | 802x469 | OpenAI local observability stack diagram | Teaches that logs, metrics, and traces become agent-readable feedback when scoped to the worktree. |
| `openai/local-observability-stack.png` | 802x469 | Raster copy of the observability SVG for rendering paths that prefer PNG | Same interpretation as the SVG; kept for stable ebook/PDF rendering. |
| `openai/limits-of-agent-knowledge.webp` | 3400x1771 | OpenAI diagram of repo-visible versus off-repo knowledge | Teaches that only repository-local, versioned artifacts reliably exist for the agent during a run. |
| `openai/layered-domain-architecture.webp` | 2576x2617 | OpenAI diagram of domain layering and provider boundaries | Teaches that agent speed needs hard dependency direction and explicit cross-cutting boundaries. |

Visual reasoning artifacts are stored in `tmp/ui-visual-reasoning/openai-harness-diagrams/`, including the generated `report.json`, previews, and contact sheets. Durable conclusions from that inspection are integrated into the guide rather than committing scratch previews.

