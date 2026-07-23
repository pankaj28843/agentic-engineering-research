# 34. Cameras, drum machines, and centaurs

Historical analogies can reveal mechanisms worth investigating: a new tool may first imitate an old medium, change the valuable skill mix, reorganize a market, or move human work toward selection and interpretation. They cannot estimate software productivity, employment, quality, or the best human–agent arrangement.

The [Thoughtworks retreat report](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf) invokes three hopeful analogies: cameras and Impressionism, drum machines and musicianship, and human–machine chess teams. The evidence audit supports a disciplined historical discussion, but not those statements as simple causal facts. The camera claim is too monocausal, the drum-machine claim lacks a sufficiently reliable source in the captured corpus, and the enduring chess-centaur claim lacks a local evaluation protocol.

The useful conclusion is therefore methodological: **an analogy may open a question; it may not close an empirical gap**.

## A plain-language model: transfer and break

Treat an analogy as a two-column instrument.

In the **transfer** column, name one mechanism that might recur. For example, cheaper production may shift scarcity from execution to selection.

In the **break** column, list material differences between the historical case and software agents:

- labor market and skill pipeline;
- ownership and bargaining power;
- cost of copying and distribution;
- speed of technical change and feedback;
- error visibility, safety, and externalities;
- market structure and customer demand;
- laws, professional institutions, and accountability;
- who receives benefits and who bears transition costs.

If the break column is empty, the analogy is decoration. If it is full, the analogy can still be useful—but only as a generator of hypotheses that need present-day evidence.

## Cameras and art: from execution to interpretation?

Aaron Hertzmann’s historical essay [*When Machines Change Art*](https://aaronhertzmann.com/2022/12/17/when-tech-changes-art.html) surveys photography, film, recorded music, sampling, computer art, animation, and visual effects. It identifies recurring patterns: early imitation of an older medium, development of a medium-specific language, backlash, changes in artistic categories, employment recomposition, and socioeconomic objections expressed partly as aesthetic objections.

This is a named researcher’s critical work in progress, not a formal systematic review or an employment-effects study. Hertzmann explicitly acknowledges selection, survivorship, and uncertainty about net employment. The source supports a mechanism-level intuition: when a technical capability becomes cheaper, people may develop new forms and contest what counts as valued work. It also insists that distribution and ownership matter.

That is narrower than saying photography “caused” Impressionism because a camera could reproduce reality perfectly. The audited source does not establish that singular causal chain, and photography itself is not perfect neutral replication. Art movements have multiple technological, economic, institutional, and intellectual causes.

**Possible transfer to software:** if agents make some forms of code production cheap, value may move toward choosing problems, specifying consequences, composing systems, reviewing behavior, and creating a distinctive product. New software forms may emerge rather than merely imitating today’s applications.

**Where it breaks:** software is operational infrastructure, not only cultural expression. Defects can expose data, move money, deny services, or create physical harm. Code is copied globally at near-zero marginal cost; production is organized through firms, platforms, licenses, and regulation unlike art markets. Feedback may be fast for compilation and very slow for social or safety consequences. Ownership of models, repositories, data, and distribution channels can concentrate gains. The analogy predicts neither developer employment nor a durable premium for “taste.”

It also does not show that displaced tasks automatically become more sophisticated jobs. A market can expand, recombine, deskill, concentrate, and eliminate roles at the same time for different groups.

## Drum machines: an evidentiary stop sign

The retreat says drummers became more sophisticated rather than obsolete after drum machines. The source trail examined for this audit did not justify that proposition. A descriptive [Research Catalogue history](https://www.researchcatalogue.net/view/2206275/2206274) was rejected because it had no formal method, relied heavily on popular or tertiary material, and moved from anecdotal history to broad reassurance.

Rejecting that source does not prove the opposite. It means the chapter should not use the claim as historical evidence.

Hertzmann’s broader treatment of recorded music and sampling still suggests testable mechanisms: tools can alter production practices, enable new forms, and trigger conflicts over authorship, authenticity, and economic control. It does not establish what happened to drummers’ employment, wages, skill distributions, or bargaining power.

**Possible transfer to software:** programmable generation may become an instrument used differently by experts, novices, and new roles. Skill may move from manually producing every element to arranging, constraining, editing, and performing with a system.

**Where it breaks:** music has live performance, recording, royalties, genre communities, and audience judgments that differ from software procurement and operations. A drum sound’s defect is not equivalent to a corrupted financial transaction. Copying and reuse exist in both domains, but rights, liability, and dependency chains differ. Agent platforms may control the tool, telemetry, and distribution in ways unlike ownership of a standalone instrument. Rapid model replacement can destabilize skills and workflows faster than an instrument’s interface changes.

The drum-machine case is valuable here as a lesson in epistemic hygiene: a memorable analogy can feel true long after its population, outcome, and counterfactual have disappeared.

## Chess and centaurs: a powerful but closed world

A [New Atlantis essay on chess and AI](https://www.thenewatlantis.com/publications/can-chess-survive-artificial-intelligence) draws on five named interviews, books, and secondary analyses. It documents changes in preparation, spectatorship, learning, creativity, and elite roles. It also cites a historical analysis in which draws rose substantially over a long period but declined slightly from around 1990, complicating a simple “engines made chess drawish” story.

The essay’s generic claims about human–machine teams beating standalone systems do not include a local protocol or result. An ICML position paper on [centaur evaluations](https://digitaleconomy.stanford.edu/app/uploads/2025/06/CentaurEvaluations.pdf) is explicit that hybrid performance is task dependent, that fair comparison must account for human time and compute, and that examples exist where AI alone beats a hybrid. It also notes that the chess-centaur advantage disappeared. The paper proposes an evaluation contract; it provides no new experiment proving augmentation.

**Possible transfer to software:** tools change preparation, search, learning, division of labor, and what experts attend to. Human–agent performance should be evaluated as a configured system, including interface, human time, compute, process, and outcomes—not assumed superior because a human is present.

**Where it breaks:** chess is closed, stable, feedback-rich, and low-externality. Rules and success are comparatively clear; positions are fully observable; games end; a bad move usually harms the player rather than an uninvolved public. Software requirements change, outputs interact with institutions and people, feedback can arrive months later, and correctness has multiple contested dimensions. Organizations also divide decision rights among developers, managers, vendors, operators, regulators, and users. “Human plus machine” does not specify who owns the decision or bears liability.

Even the word *centaur* hides different interaction modes. An [HBS working paper](https://www.hbs.edu/ris/Publication%20Files/26-036_e7d0e59a-904c-49f1-b610-56eb2bdfe6f9.pdf) observed fused, directed, and abdicated patterns among junior consultants using GPT-4 on one fictional investment task. The modes were not randomized, there was no human-only or AI-only arm, and the reported category counts and percentages contain inconsistencies. It gives useful vocabulary, not evidence that one mode improves software outcomes.

## Automation history: tasks, power, and distribution

Judy Wajcman’s [critical review, *Automation: is it really different this time?*](https://researchonline.lse.ac.uk/id/eprint/69811/1/Wajcman_Automation%20is%20it%20really%20different%20this%20time.pdf), challenges occupation-level forecasts, anthropomorphic accounts of machines, acceleration narratives, and technological determinism. It redirects attention to task composition and to the distribution of work, time, money, and ownership. The 2017 essay predates modern LLM agents, reviews four books, and offers no developer-employment estimate. Its durable contribution is the question “who organizes and benefits from the change?” rather than a reassuring historical cycle.

The audit also located an American Economic Association page for [a task-level analysis of nineteenth-century manufacturing automation](https://www.aeaweb.org/articles?id=10.1257/jep.33.2.51), but only the abstract and citation metadata were captured. No sample, estimate, identification strategy, or robustness result was locally available. It remains a lead; no empirical result from it is used here.

**Possible transfer:** occupations are bundles of tasks, so automation may reshape roles unevenly rather than remove them as indivisible units.

**Where it breaks:** nineteenth-century machinery and 2026 software agents differ in capital intensity, copying cost, update cadence, global reach, credentialing, intellectual property, workplace surveillance, and ability to operate across cognitive tasks. Institutions and ownership decide whether saved time becomes leisure, more output, lower headcount, or higher returns. History gives alternatives, not a forecast.

## The analogy audit card

Before using a historical analogy in a strategy document, complete this card:

1. **Exact claim:** What present decision is the analogy meant to support?
2. **Historical source:** Is it original research, synthesis, critical history, practitioner recollection, or folklore?
3. **Unit and outcome:** Task, occupation, firm, market, quality, wage, employment, or cultural value?
4. **Mechanism:** What exactly transfers—lower production cost, new medium, complementary expertise, changed coordination, or concentrated ownership?
5. **Difference pass:** Compare labor market, ownership, copying, safety, feedback, institutions, market structure, and distribution.
6. **Counterhistory:** Who lost work, status, income, autonomy, or access? What did the optimistic version omit?
7. **Present test:** What current software evidence would confirm or disconfirm the proposed mechanism?
8. **Decision limit:** What may the analogy motivate, and what may it not estimate?

Run the exercise twice: first with the preferred analogy, then with an analogy pointing the other way. If the strategy survives only the comforting history, it is not yet evidence-led.

## Evidence judgment

- **Confidence in recurring mechanisms:** moderate for imitation, recombination, role change, and distributional conflict as useful questions.
- **Confidence in the retreat’s specific histories:** low. The singular camera causation, drummer outcome, and enduring centaur-superiority claims are not established by the audited sources.
- **Predictive power for software:** very low. No analogy supplies a software productivity, employment, quality, or team-design estimate.
- **Best-supported caution:** task composition, ownership, institutions, and distribution mediate technical change; human participation is not automatically effective.
- **Unresolved question:** which present-day longitudinal evidence can distinguish augmentation, task transfer, deskilling, and role loss across different software labor markets?

Use history to enlarge the hypothesis space, including uncomfortable possibilities. Then return to contemporary measurement before making a decision.

Podcast hook: Three irresistible stories—a camera, a drum machine, and a chessboard—enter a strategy meeting. Each survives only after its comforting ending is removed and its broken assumptions are named.

Continue reading: Chapter 35 owns the normative question of human judgment and the evidence on human–agent work; [Chapter 25](25-productivity-hype-bubble.md) shows why neither history nor analogy supplies a productivity forecast.
