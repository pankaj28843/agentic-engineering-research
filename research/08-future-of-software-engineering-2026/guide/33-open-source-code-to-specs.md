# 33. Will open source shift from code to specifications?

The audited corpus does not show an open-source ecosystem moving from shared code to shared specifications. Agents can implement some local specifications, and repositories can preserve executable requirements beside code. Those facts do not establish that maintainers can reliably regenerate compatible implementations or that communities can collaborate mainly through ideas and specs.

The [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf) offers a deliberately speculative possibility: if implementation becomes cheap per user, open source might exchange specifications while each consumer generates code. It also recognizes the danger of excluding people without comparable AI or hardware access. Both deserve investigation. Neither is a measured transition.

## A plain-language model: four different rungs

Keep four claims separate:

1. **Local generation:** an agent implements one specification once.
2. **Spec beside code:** a repository treats tests, schemas, models, contracts, examples, or prose as maintained artifacts.
3. **Regeneration:** different teams or tools repeatedly create implementations that remain behaviorally compatible.
4. **Spec-primary ecosystem:** people coordinate, govern, fork, secure, and sustain software mainly through shared specifications rather than a shared reference implementation.

Evidence for an earlier rung does not establish a later one. A successful generated feature proves possibility under its own conditions. It says little about two independent implementations, compatibility across releases, production debugging, or a community’s institutional survival.

“Specification” also hides many forms. A typed interface constrains shapes; tests constrain selected examples; a protocol standard constrains observable interaction; a formal model may prove named properties; prose carries goals and ambiguity. No single artifact completely describes real software. The remaining decisions reappear in generated code or in disputes over the spec.

## What adjacent empirical evidence actually measures

The peer-reviewed study [*Who is using AI to code?*](https://www.science.org/doi/10.1126/science.adz9311) analyzed about 30 million Python contributions from 160,097 developers in six countries between 2019 and 2024. Its classifier estimated that AI generated about 29% of US Python functions by the end of 2024; adoption was associated with roughly 3.6% more quarterly commits, with measurable gains for senior but not junior developers.

This is evidence of diffusion and differentiated association with output, not evidence that code disappeared as the shared artifact. The classifier may shift outside its synthetic validation distribution, commit volume is not quality or useful output, and language, country, platform, contributor, and time choices limit transfer. The study contains no measure of spec-primary repositories or regenerated compatible implementations.

The preprint [*Augmentation with Dilution*](https://arxiv.org/html/2606.26289v1) compares 2,808 agent-adopting public repositories with 8,289 matched controls across 454,977 repository-months. It reports no significant absolute human-contributor change, but lower human-contributor density, a 3.7-point fall in newcomers’ relative share, and about 5.3% greater review depth. Detection, matching, sample, missing review months, and the use of comments per review rather than time or quality bound the result.

That structural change could affect who participates and who absorbs review. It still does not measure which artifact communities share. Indeed, increased review interaction is consistent with code remaining a central negotiation surface.

A cross-sectional study of governance materials from [67 visible open-source projects](https://arxiv.org/html/2603.26487) finds multiple concerns, orientations, and strategies around AI contributions. Its sample favors English, GitHub, explicit policy, and prominent projects and cannot measure enforcement or outcomes. It shows that governance is actively adapting; it does not show convergence on specifications.

GitHub’s platform statement about an open-source [“Eternal September”](https://github.blog/open-source/maintainers/welcome-to-the-eternal-september-of-open-source-heres-what-we-plan-to-do-for-maintainers/) reports shipped repository controls and interaction limits while describing gating and automated triage as exploratory. It warns that restrictions can harm good-faith newcomers. There are no comparative effects. The response centers contribution flow and trust around repositories and pull requests, not a replacement specification ecosystem.

The negative finding is therefore strong: this source set contains no adoption series, repository sample, longitudinal case, or controlled comparison showing movement from shared code to shared specs.

## What code repositories carry besides behavior

Source code is not merely an inefficient encoding of a specification. A shared implementation also carries:

- **Operational exactness:** the actual choices that execute when requirements are incomplete or conflicting.
- **Debuggability:** a concrete artifact against which users can reproduce, inspect, profile, and patch failures.
- **History:** commits and discussions showing why behavior changed and which alternatives failed.
- **Provenance and rights:** authorship, sign-offs, licenses, notices, and dependency lineage.
- **Security response:** a location to disclose, patch, backport, compare, and distribute fixes.
- **Governance:** maintainers, review rules, releases, issue processes, appeals, and decision authority.
- **Forkability:** a runnable starting point when a community or supplier disagrees.
- **Institutional memory:** contributor identity, norms, tacit design knowledge, and accumulated maintenance practice.

A spec-primary system must reproduce these functions or explain why they are unnecessary. A test suite can reveal regression but not the reason for a design. Generated implementations can all inherit the same ambiguous requirement or model blind spot. Many distinct implementations increase diversity only if they are genuinely independent; they can also fragment debugging and multiply attack surfaces.

Compatibility is similarly deeper than passing a fixed conformance suite. Consumers depend on undocumented behavior, performance, timing, failure modes, security properties, deployment format, and operational tooling. Expanding the spec to capture everything can make it resemble another implementation—and create its own maintenance load.

## Openness and access do not follow automatically

The Linux Foundation’s normative discussion of [open-source AI licensing](https://www.linuxfoundation.org/blog/the-open-source-legacy-and-ais-licensing-challenge) separates code, model weights, data and other materials, attribution, downstream use, and outputs. Its proposed licensing framework is not proof of legal sufficiency, adoption, reproducibility, or equal access. It shows that publishing a specification would leave several rights and artifacts unresolved.

A 2026 United Nations University report on [AI systems as digital public goods](https://unu.edu/sites/default/files/2026-06/AI_Systems_as_Digital_Public_Goods_0.pdf) combines a 25-person consultation, 21 purposive expert interviews, and a 37-person targeted survey. Participants treated access, privacy, do-no-harm, transparency, inclusion, adaptability, open source, and free access as distinct. Its small, purposive, English-language expert groups measure views rather than adoption or equity. The conceptual separation matters: visible specs and zero download price do not guarantee practical use.

A peer-reviewed *Nature Communications* comment on [open-source AI and sustainable development](https://www.nature.com/articles/s41467-026-73866-8) likewise distinguishes code, weights, data, and licenses from compute, data centers, energy, water, electronic waste, safety, and geographic infrastructure concentration. It is normative synthesis without an empirical method. It supports a checklist, not a measured ecological or distributional effect.

For a spec-primary ecosystem, access includes the ability to interpret the spec, obtain compatible models and tools, afford inference and verification, run the result on available hardware, audit it, patch it, and participate in governance. If only well-capitalized users can regenerate and validate implementations, public specifications may reduce practical forkability relative to public code.

## Six skeptical tests

Before claiming a transition, ask:

1. **Interoperability:** Can at least two independently produced implementations pass an evolving conformance suite and work with real consumers?
2. **Reproducibility:** Can another team recreate the result with documented models, prompts, tools, versions, data, seeds, hardware, and cost—or obtain an equivalent result without the original supplier?
3. **Maintenance:** Can defects be localized, patched, backported, reviewed, and communicated faster than regenerating introduces divergence?
4. **Governance and provenance:** Who changes the spec, resolves ambiguity, attributes work, records rights, handles vulnerabilities, and accepts accountability?
5. **Access:** Can participants with limited compute, bandwidth, money, language support, disability access, or model availability still use and shape the project?
6. **Lifecycle cost:** Do generation, evaluation, duplicate implementations, storage, compute, energy, review, and security response improve the whole system rather than only initial coding?

A transition claim needs longitudinal evidence across all six, not one impressive implementation.

## A two-implementation pilot

Test the hypothesis without abandoning code.

Choose a small, non-safety-critical component with stable public behavior and no hidden production data. Preserve the existing implementation as a reference and fallback. Create a versioned specification containing goals, interfaces, examples, executable conformance tests, performance and security constraints, error behavior, and known ambiguities.

Give the same public spec to two teams using different toolchains. Isolate implementation work enough to make independence meaningful and record every model, prompt, edit, dependency, license, cost, and artifact. Neither team should silently use the reference code as generated context.

Then:

- run conformance, differential, fuzz, security, performance, and compatibility tests;
- exchange each implementation with real downstream consumers;
- inject one bug and one requirement change, then measure diagnosis and update;
- have an outside contributor attempt a fork with a constrained compute budget;
- simulate a vulnerability disclosure and urgent coordinated release;
- compare review time, defects, divergence, cost, energy-relevant compute use, and participant experience with maintaining the reference code.

Keep a decision log for every ambiguity the spec did not resolve. Those entries reveal whether knowledge moved into a shared specification or remained in people, models, and generated implementations.

A hybrid result may be valuable: executable specs and models can become stronger shared assets while a reference implementation remains the operational anchor. That is an inference and design option, not evidence of an ecosystem transition. The pilot should retain code until regeneration proves compatibility, maintainability, access, and response over multiple changes.

## Evidence judgment

- **Local implementation from a spec:** demonstrably possible in bounded cases, but not generally sufficient for production trust.
- **Specs beside code:** a credible engineering pattern; this audit does not estimate its prevalence or effect.
- **Reliable regeneration:** open. No selected source demonstrates sustained compatible reimplementation across releases.
- **Spec-primary open-source transition:** unsupported. No measured ecosystem movement was found.
- **Access and sustainability:** material unresolved boundaries. Public artifacts do not guarantee compute, skills, rights, reproducibility, or participation.

Cheap generation can lower one cost without replacing the institutions embodied in shared code. The stronger near-term hypothesis is not “code gives way to specs,” but “communities learn which additional specifications make shared code easier to verify, reproduce, and govern.”

Podcast hook: Two teams receive the same perfect-looking specification and produce two passing implementations. Then a vulnerability arrives, an undocumented behavior matters, and the experiment discovers what the shared code had been carrying all along.

Continue reading: [Chapter 34, “Historical human–machine analogies”](34-historical-human-machine-analogies.md), examines how to reason about institutional change without using analogy to fill this evidence gap.
