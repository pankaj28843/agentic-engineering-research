# 20. Port first, improve second

The safest general answer is **yes, separate behavior preservation from architectural improvement—but treat that as a risk-control heuristic, not a universal law**. The separation reduces the number of explanations for a failure. It does not prove that old behavior is correct, valuable, secure, or worth carrying forward.

The [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf) recommends preserving behavior during a port and improving the design afterward. It even allows deliberate preservation of a known bug when a downstream system depends on it. That is a participant synthesis under Chatham House rules. It establishes that experienced practitioners use the pattern; it is not a controlled comparison showing that the sequence always wins.

## A plain-language model: one question at a time

Imagine moving a complicated kitchen into a new building while also replacing every recipe, appliance, and supplier. When dinner tastes wrong, which change caused it? A port-plus-redesign migration creates the same attribution problem.

“Port first” divides the work into two questions:

1. **Behavior question:** does the new implementation produce the same externally observable results as the old one under the agreed conditions?
2. **Design question:** after equivalence is visible, which behaviors, structures, and operating assumptions should change?

This is not a command to translate every line literally. A behavior-preserving port may use a very different internal structure. What matters is an explicit equivalence boundary: outputs, side effects, timing tolerances, error behavior, data changes, and interactions that stakeholders have agreed to preserve.

The mechanism is experimental control. If a test fails during the first phase, the team investigates a compatibility defect. If it fails during the second, the team investigates an intentional change or regression. Smaller hypothesis sets make diagnosis, review, rollback, and approval easier. AI increases the value of this separation because it can generate many plausible changes quickly, including “helpful” changes that were never requested.

## What the evidence actually supports

The strongest support is convergent practice evidence, not a head-to-head trial of migration sequences.

[Thoughtworks’ account of AI-assisted COBOL modernization](https://www.thoughtworks.com/insights/articles/claude-code-cobol-modernization-reality) describes a much larger process than code translation: discovery, static and dynamic analysis, local summaries, relationship mapping, tacit constraints, data migration, synchronization, dual running, and cutover. It warns that direct translation can carry technical debt forward and overlook infrastructure, integration, operations, and people. This is a consultancy account, so its claims are not independent experimental estimates. Its value here is the mechanism: teams need to establish what the system does before deciding what it should become.

Microsoft reports similar limits in an [official account of agent-assisted COBOL migration](https://devblogs.microsoft.com/all-things-azure/how-we-use-ai-agents-for-cobol-migration-and-mainframe-modernization/). Bankdata has more than 70 million lines of COBOL, yet only some modules are suitable candidates; batch behavior, I/O, job-control language, and service-level requirements can force redesign. In a small donated-module exercise, GPT-4 guessed and hallucinated, context coherence weakened across a call chain, and deterministic tests were essential. This is vendor practice evidence involving a small exercise, not proof of completed modernization at Bankdata. It nevertheless shows why an executable compatibility target matters.

Repository-scale evidence adds a useful boundary. [RepoRescue](https://arxiv.org/html/2607.01213v1) tested agents on 193 Python and 122 Java repositories, including unmaintained projects and “time-travel” environments. Full-environment access generally helped, and the union of attempts rescued more repositories than a single model did. But an audit of 34 apparently successful unmaintained Python repairs found only 12 meaningful compatibility patches; five had regressions and seven failed a more realistic scenario. The work was compatibility rescue rather than replatforming, and the original test suites defined success. The result supports environment feedback and staged validation while showing that a green inherited suite is not a complete behavioral oracle.

Small-program research makes the risk more concrete. In [*Articulate but Wrong*](https://arxiv.org/html/2605.21537v1), 11 models translated 60 hand-crafted Python 2 snippets of at most ten lines. Across 1,980 calls, semantic drift appeared far more often than benign syntactic changes, and same-model self-review missed 83 of 262 drift cases. The corpus is tiny and artificial, so it cannot estimate enterprise migration failure rates. It does show that fluent explanations and self-review do not establish semantic preservation.

A practitioner essay on [executable oracles for rewrites](https://vinny.dev/blog/2026-07-17-everyone-knows-you-never-rewrite/) recommends characterization tests, golden outputs, differential testing, shadow traffic, and staged rollout. This is secondary practitioner guidance, not comparative research. It is useful because it turns “preserve behavior” into observable checks and also admits that passing tests may be incomplete.

Together, these sources support a bounded claim: separating compatibility from redesign improves causal legibility when the old system can serve as an oracle and when the team can observe the behavior that matters. They do **not** show a universal reduction in cost, elapsed time, or defects.

## The bug-preservation trap

“Preserve known bugs deliberately” sounds perverse until “bug” is split into categories.

- A downstream consumer may rely on an odd rounding rule or error code. Changing it silently during a port creates an unplanned interface change.
- A defect may corrupt data, violate regulation, expose secrets, or create unsafe behavior. Reproducing it can be unacceptable.
- A behavior may be merely accidental and have no remaining consumer. Carrying it forward creates avoidable validation and maintenance cost.
- The team may not know which category applies. In that case, preservation is a temporary uncertainty-management decision, not endorsement.

The key word is **deliberately**. Record the behavior, known consumers, risk owner, expiration condition, and test. A “compatibility quarantine” can reproduce it behind an adapter while the consumer is repaired. That preserves attribution without normalizing the defect. Security, safety, legal, and data-integrity failures need explicit exception handling and may force improvement during the port.

Deferring redesign also has costs. A literal translation can encode assumptions from the old runtime in a new language, duplicate obsolete batch boundaries, and make the transitional architecture harder to remove. Parallel operation consumes money and attention. If the old environment cannot run, its outputs are untrustworthy, or the migration is driven by an urgent vulnerability, the old system is a poor oracle. The evidence audit found no comparative study telling us where these costs overtake the diagnostic benefit. Teams must make that boundary visible rather than turn the heuristic into dogma.

## A two-ledger migration exercise

Before authorizing a migration slice, create two short ledgers. This is a review exercise, not a full implementation playbook.

### Ledger A: preservation contract

- Name the slice and its observable boundary.
- List representative inputs, outputs, side effects, error states, and timing tolerances.
- Identify each oracle: old-system differential run, characterization test, golden data, domain expert, protocol specification, or production trace.
- Mark oracle blind spots, especially security, data quality, concurrency, performance, and rarely exercised branches.
- List known defects as **preserve temporarily**, **quarantine**, **fix now**, or **retire with the consumer**.
- Name the person authorized to accept a difference.
- Define the rollback and evidence-retention path.

### Ledger B: improvement backlog

- Record every tempting cleanup the port reveals.
- State the user or operational value, not only the code smell.
- Identify the prerequisite compatibility evidence.
- Give the improvement its own acceptance tests and decision owner.
- Set a date or trigger so “later” does not become permanent.

Run a tabletop exercise with one real behavior. Ask the agent to produce both an equivalent version and an improved version. Reviewers must classify every difference before seeing which version is which. If the team cannot explain the boundary, it is not ready to automate that slice. If the improvement backlog has no owner or trigger, the organization is at risk of preserving debt indefinitely.

## Evidence judgment

- **Confidence in the mechanism:** moderate. Experimental control, deterministic feedback, and smaller change sets are well grounded by the practice accounts and migration studies.
- **Confidence in universal outcome improvement:** low. No audited source directly compares “port then improve” with combined transformation across representative enterprise programs.
- **Generalizability:** strongest for systems with executable old versions, stable interfaces, recoverable test data, and reversible deployment. Weakest for unsafe, unavailable, poorly observable, or fundamentally obsolete systems.
- **Important conflict:** behavior fidelity lowers migration ambiguity, while literal preservation can retain debt and harmful behavior. The right unit is a consciously chosen compatibility boundary, not a line-by-line rewrite.
- **Unresolved question:** what mix of differential tests, production traces, domain review, and nonfunctional checks predicts safe cutover for different legacy-system classes?

The durable lesson is sequence discipline: preserve enough to make change explainable, then improve under a separately reviewable contract. The slogan fails when “enough,” “behavior,” and the exception path remain undefined.

Podcast hook: An AI can rewrite a system faster than a team can decide which of its bugs are actually interfaces. The episode follows one odd legacy behavior through preservation, quarantine, redesign, and cutover.

Continue reading: [Chapter 21, “Bespoke compilers become affordable”](21-bespoke-compilers-affordable.md), tests whether the tools behind such migrations have really crossed an economic threshold; Chapter 37 turns sequence discipline into a delivery pattern.
