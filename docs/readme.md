📢 Project Dynamo Update: Project Unpaused & New Tasks Available
First, thank you all for your patience while we worked through a number of updates and improvements to the project. We've made several important changes and clarifications to the task creation and evaluation process:


Key Updates


The reference task.toml is now a single canonical block, identical between the "Write instruction.md and task.toml" step and the "task.toml reference" page:


Top-level artifacts
[task]
[metadata] (grouped into pre-seeded / fixed-dataset / fellow-set fields)
[verifier]
[agent]
[environment] (including mcp_servers)



avg_at_8 has been removed as a task.toml field everywhere. The pass@8 acceptance requirements are now covered under the evaluation process described below.
Updated Difficulty Bar & Evaluation Pipeline


The acceptance bar has been raised:


A task must now produce at least 4 valid failures out of 8 trials, measured using GPT-5.4 at extra-high reasoning effort.

Only genuine failures count.
Timeouts, infrastructure issues, and instruction/verifier misalignment do not count.
Any failure caused by misalignment is considered blocking and must be fixed before proceeding.


Stage 1 — Pass@2


Two trials are run.

At least one valid failure is required.

Includes an LLM analysis of the runs.


Stage 2 — Pass@8


Triggered only after Pass@2 succeeds.

Eight new trials are executed.

At least 4 valid failures are required.


Submissions are blocked until all checks have been successfully cleared.


Additional Changes


[verifier].environment_mode should be left unset.

The verifier runs inside the task's single environment/Dockerfile image (canonical TB2).

Harbor overlays tests/ at verification time.

There is no separate tests/Dockerfile.

Category and subcategory are now pre-seeded by the Dynamo team and should not be modified.


Contributors only set:

task_objective
artifact_type



Both should use lowercase snake_case values from .dynamo/diversity-taxonomy.toml.

instruction.md now has a 1,500-token limit.

Any structured-output schema should be documented directly in the prompt or in a referenced specification file.

The separate structured-output line has been removed.


Added a new "Common errors and examples" subsection containing four worked failure cases, including:



Problem description

Code excerpts


Guidance on how to avoid the issue


Added a new "Before you submit: quick self-check" section with a five-item checklist based on the common failure examples.

Added a fourth justification question (with an accompanying callout) in the proposal step.


📚 Full update details can be found here:

https://project-dynamo.learn.joinhandshake.com/updates


2-Day Push Incentive


We're also kicking off a focused 2-day push to increase high-quality task submissions.

For this period, there will be an additional $50 incentive for every task that reaches the RTD layer.

We appreciate everyone's contributions and are looking forward to seeing the next wave of Dynamo tasks.


Thank you, and happy building!

















Project Dynamo - How to stump the model
A short training + check on how to author Terminal-Bench tasks that a frontier model actually fails (avg@8 ≤ 0.5). Read each panel, then answer. Plan for ~25 minutes.

The bar, and the one idea
The bar: every task must reach avg@8 ≤ 0.5.
Run Opus 4.8 or GPT-5.4 eight times with Terminus-2. The model must fail at least 4 of the 8 attempts. A task it solves 5/8 times is rejected as too easy — no matter how polished.

The single most important idea, drawn from every Dynamo task that cleared the bar: a hard task does not depend on the model not knowing something. It depends on the model being confidently wrong — running the obvious solution, getting output that looks right, and committing to it. Frontier models have read every textbook, CVE, and blog. If a human specialist could name the trick from your description, the model already knows it too. Obscurity is not difficulty.

















Project Dynamo - How to stump the model
A short training + check on how to author Terminal-Bench tasks that a frontier model actually fails (avg@8 ≤ 0.5). Read each panel, then answer. Plan for ~25 minutes.

The five core strategies
Five ways to make the model confidently wrong.
Each strategy is distilled from a delivered Dynamo task that measured avg@8 ≤ 0.5. The green line names the real task it came from.

1. Silent trap — the obvious solution runs clean and is wrong
The naive approach completes without error and produces believable output; the only way to know it is wrong is to understand what the output should mean. Avoid bugs that throw — a model fixes anything that throws.

Delivered — silent-feature-bugs: two refactor-introduced bugs (timezone-agnostic windowing and pre-split target-encoding leakage), invisible at runtime, that must be fixed together because their effects interact. The pipeline emits a plausible feature matrix either way.

2. Test the cases the instructions define but the samples never show
Ship samples / a runbook / a spec that the naive reading reproduces perfectly, then grade on cases that a faithful reading of the instructions still fully determines but the samples never exemplify. The model calibrates to the visible examples and under-generalizes — committing to a confident answer the instructions, read carefully, contradict. The point is not to mislead: the instructions never lie and every graded case must be unambiguously derivable from them (instruction author and verifier must agree on the expected output). You simply decline to hand the model an example of every case.

Delivered — gnss-log-decode: the instructions call for decoding all constellations and leap-second eras the format supports, but the shipped samples contain only GPS fixes in one era; the graded captures add BeiDou (different epoch and offset) and other eras. A solution that merely reproduces every visible sample under-generalizes and is wrong on the hidden-but-specified constellations — and the binary prints only raw fields, so there is no oracle to self-check. (preprocessing-recovery does the same with a schema doc that fully defines every column but only illustrates a subset.)

3. Remove the model’s ability to self-verify
If the environment holds an oracle — a reference binary that prints the answer, a doc that states the rule, a way to check work — the model uses it. Take it away (this is also an anti-cheat requirement).

Delivered — tokenizer-recovery: correct token IDs depend on hidden subsets (no-marker vocab entries, an alternate Unicode normalization, multi-piece segmentation, special-token framing) scattered through 205 inputs. Nothing flags which inputs are affected; the shipped encoder reproduces the naive output — the trap.

4. Compound several corrections that must compose in order
One trap is often guessable. Several independent corrections that overlap on the same records — where fixing some but not all still fails — push the pass rate down hard.

Delivered — slo-breach-recovery: five mixed encodings in one metric dump (millisecond vs second timestamps, cumulative counters, counter resets, per-second rates, failed-scrape sentinels). They overlap (a series can be both millisecond-stamped and cumulative); handling only some still produces wrong counts.

5. Grade exactly, so plausible-but-wrong fails
Loose tolerances let a near-miss pass. Define the tolerance from the context of the problem itself, and require that every valid interpretation of the instructions falls inside it. The trick: some methods appear to follow the instructions but violate an explicit or implicit requirement — those must land outside the band. Use exact match for discrete output; for numbers, set the band wide enough to admit every genuinely-compliant method yet tight enough that any requirement-violating method falls outside it — and justify the band from the problem.

Delivered — migrate-colorkit: the naive sRGB port looks like it follows the spec but violates the gamma requirement and lands ~0.15 off in luminance; the tolerance is 0.02 — wide enough that every correct decode passes, far tighter than the gamma mistake, so the requirement-violating method fails every tile.

















Project Dynamo - How to stump the model
A short training + check on how to author Terminal-Bench tasks that a frontier model actually fails (avg@8 ≤ 0.5). Read each panel, then answer. Plan for ~25 minutes.

The #1 trap: the named gotcha
If a specialist can name the bug, so can the model.
The most common reason a polished proposal comes back too easy: the trap is a recognizable, nameable concept the model has read about. It identifies it on sight and applies the standard fix. The difficulty lived in your description, not in the model’s blind spot. Worked example, from a real in-flight proposal:

Before: “Find and fix an account service that de-duplicates usernames with one Unicode normalization form (NFC) but resolves identities with another (NFKC), allowing an impersonation collision.”

Why the model wins: this is a famous named bug class (the public music-streaming account-takeover). The model spots the normalization-form mismatch instantly and applies the one-line fix. Hard to name, trivial to fix.

Harden it: stop asking the model to FIND a nameable bug. Give a service that looks correct and a seed set of identifiers that all resolve correctly under the naive rule; grade on hidden confusable pairs from scripts the seed never shows, where the correct identity model must be applied to unseen input. Remove the word “normalization” entirely; make the collision observable only through downstream behavior, and grade exact resolution outcomes across many hidden pairs.

The same tell recurs across in-flight proposals — each a named recipe the model executes on sight:

ECDSA biased-nonce key recovery — the textbook Hidden Number Problem solved by LLL lattice reduction (Minerva / LadderLeak). The model builds the lattice and calls a CAS. (Received in near-duplicate — a diversity problem too.)
Async CDC-FIFO repair — the canonical fix is Gray-code pointers through a two-flop synchronizer, exactly what every model has seen; the proposal even names metastability as the pitfall.
Quartic-oscillator eigenvalue — shooting + Numerov is standard computational physics the model runs fluently; “hard for a human specialist” is not “hard for the model.”






















Project Dynamo - How to stump the model
A short training + check on how to author Terminal-Bench tasks that a frontier model actually fails (avg@8 ≤ 0.5). Read each panel, then answer. Plan for ~25 minutes.

More ways to stump the model
The category taxonomy describes a task's DOMAIN, not its difficulty.
Difficulty is an orthogonal, structural property — the spec’s category/subcategory list says nothing about it. Beyond the core five, these levers each target a documented frontier-model weakness. Each line below is weakness → real example → how to use it.

A. No single wrong line (emergent / cross-component / timing)
Models find a faulty line; they struggle when no file is wrong and the defect lives only in the interaction. Example: an in-flight work-queue task where a stale lease completion recycles a token already reissued to another record — no exception, no error counter, every component locally correct. Use it: design emergent defects (concurrency, event ordering, recycled-resource aliasing); seed the trace so the outcome is deterministic to grade.

B. Bug-for-bug preservation (the helpfulness trap)
Models are trained to improve; tell them to preserve an exact quirk and the instinct to “fix” it breaks the requirement. Example: the in-flight Fortran→Rust port must reproduce the original’s exact behavior (persistent SAVE state, integer division from implicit typing, bit-aliasing), not the clean modern equivalent. Use it: require exact reproduction of legacy behavior, warts included, graded against the legacy output.

C. Minimal-diff / “nothing to change here”
Models over-edit and trip hidden invariants. Example: the correct fix is one line (or a single config value) and a hidden regression suite checks all the untouched behavior. Use it: make the correct change tiny or absent, and grade the whole surface — include a path where the right answer is “no change needed.”

D. Spec-by-environment (underspecified on purpose)
Models lean on the prompt; put the real contract in an opaque artifact they must reverse-engineer. Example: gnss-log-decode and the in-flight firmware-TLV audit — the record layout, vendor CRC parameters, and time conventions are recovered from a stripped binary or a worked example, never read from the prompt. Use it: keep the prompt about WHAT, never HOW.

E. Defeat the iterate-test-fix loop
Agents converge by chasing a failing signal; remove it and the loop can’t self-correct. Example: the naive solution produces no error and no visible failing test (the real check is hidden), so the agent’s run-test-fix cycle ends “successfully” on a wrong answer. Use it: ensure nothing in the environment tells the agent it is wrong; pair with the silent trap and a hidden verifier.

Two more places to look
Underused high-yield subcategories already in the taxonomy: concurrency & synchronization debugging, reverse engineering, compilers/interpreters.
Weak-spots with no taxonomy home: time / timezone / calendar & leap-second arithmetic (the mechanism behind gnss-log-decode), and stateful protocol / handshake correctness.
In-flight proposals that already get it right
Silent trap: a work-queue dispatcher whose token-aliasing loss appears only under a specific interleaving — no error path.
Under-exposed cases: an HTTP edge-cache proxy that returns valid-looking but stale/cross-user responses; the hidden verifier rebuilds the expected transcript and the seed trace under-exposes the instruction-defined cases.
Obscure-and-exact: a vertically-integrated cannabis-tax computation hinging on a narrow tax-court doctrine, graded to the exact dollar.
Self-check before you build: would a frontier model run the obvious thing, see plausible output, and commit to a wrong answer with no way to notice? If yes, it clears the bar.




Project Dynamo - How to stump the model
A short training + check on how to author Terminal-Bench tasks that a frontier model actually fails (avg@8 ≤ 0.5). Read each panel, then answer. Plan for ~25 minutes.

Fair vs unfair
Hard must also be FAIR. A correct, fully-compliant solution must pass.
Two of the strategies have a sharp fairness edge. Cross it and you ship an unsolvable task, not a hard one.

Hidden cases (Strategy 2): fair edge cases vs unfair surprise requirements
The rule: every graded case must be unambiguously determined by the instruction. You may decline to show an example of every case, but you may not grade behavior the prompt doesn’t specify or contradicts.

FAIR: the prompt says “decode every record type / constellation the format supports” and the sample only shows one — grading the others is fair, because a careful reading already requires them (gnss-log-decode).
UNFAIR: the prompt says “produce the report for the provided log” (or “the solution must be valid for the given data”) and the verifier then grades a different log. The shown solution was compliant; the hidden data is a surprise requirement.
UNFAIR: the verifier checks a column / field / behavior the instruction never mentions.
Fix for the unfair version: state the generality in the prompt (“must handle all X the format allows”) so the hidden cases become instruction-defined — then they’re fair.

Exact grading (Strategy 5): when strict precision is fair
Different valid methods, libraries, approximations, and rounding choices land on slightly different numbers — and you deliberately don’t reveal the method. So the band must admit every valid interpretation.

FAIR exact / very tight: discrete outputs — integer counts, class IDs, exact-dollar amounts, decisions (slo-breach-recovery’s integer breach counts); or a precision the prompt explicitly states (“round to 4 decimals”); or a band calibrated so every valid method passes while a requirement-violating method fails (migrate-colorkit’s 0.02).
UNFAIR: a float with no stated precision graded to 1e-9, so a different-but-valid numerical method / library / rounding fails. If you didn’t justify the precision in the prompt and didn’t calibrate against valid alternatives, leave numerical room.





Project Dynamo - How to stump the model
A short training + check on how to author Terminal-Bench tasks that a frontier model actually fails (avg@8 ≤ 0.5). Read each panel, then answer. Plan for ~25 minutes.

Judge real instructions
Now read three real instructions and judge them.
Each instruction below is the actual instruction.md from a delivered Dynamo task that measured avg@8 ≤ 0.5 — it really did stump Opus 4.8 / GPT-5.4. Each is hard for a different reason, and each is fair (the hidden behavior is fully determined by the instruction). Decide whether it’s hard enough and pick the reason, then explain in your own words.

Instruction A
A fintech feature-engineering pipeline fix:

A fintech feature engineering pipeline at `/app/data/pipeline.py` takes raw transaction data from `/app/data/transactions.csv` (with config at `/app/data/config.json`) and produces a feature matrix for a churn-prediction model. The pipeline runs without errors but contains two silent bugs introduced during a recent refactor that corrupt the output features.

Fix both bugs in the pipeline and write the corrected feature matrix to `/app/features.parquet`. The output must be a Parquet file with the same columns as the original pipeline produces: `user_id`, `transaction_id`, `timestamp`, `amount`, `merchant_category`, `category_encoded`, `region`, `is_train`, `rolling_7d_spend`, `rolling_7d_count`, `rolling_7d_mean`, `rolling_30d_spend`, `rolling_30d_count`, `rolling_30d_mean`.

The `config.json` defines timezone mappings for each region, the train/test split date, and rolling window parameters. Read it carefully. The timestamps in `transactions.csv` are in UTC. Each transaction has a `region` field that maps to a US timezone.

Run the pipeline with: `python3 /app/data/pipeline.py`
Instruction A — is it hard enough to clear the bar, and if so what makes it hard? 


Too easy — fixing two bugs in a Python pipeline is routine work a frontier model handles

Hard enough — it is a silent trap: the pipeline runs without errors and emits a plausible feature matrix either way, so the model commits to corrupted output with nothing signalling the bug

Hard enough — but only because Parquet output and pandas rolling windows are obscure APIs

Hard enough — because it requires a rarely used machine-learning library
Explain your reasoning for Instruction A 
In 2-4 sentences, explain why a frontier model fails Instruction A and name the strategy it uses.
Instruction B
A multi-constellation GNSS binary-log decoder:

A multi-constellation GNSS receiver records its navigation fixes as a binary log. You are given the firmware's log-reading utility /app/gnsslog (a stripped ELF), one sample log /app/capture.bin, and /app/samples.txt showing the expected decoded output for that sample log.

Running the tool:

    /app/gnsslog --version        prints the firmware banner
    /app/gnsslog <capture.bin>    prints the raw navigation fields of each fixed-size record: sys (satellite system), wn (week), tow (time of week), val (raw reading), flags

It prints the fields exactly as stored and does not convert them. Reverse engineer /app/gnsslog and the log format, then write /app/solve.py that fully decodes a log.

When run as:

    python3 /app/solve.py <capture.bin>

it must print one line per record, in file order, each line being:

    <UTC timestamp, ISO-8601 'YYYY-MM-DDTHH:MM:SSZ'> <calibrated reading to exactly 4 decimal places> 0x<flags as 4 lowercase hex digits>

i.e. the receiver fix time expressed as a UTC timestamp, the reading converted to its real engineering value, and the flags. Your output for /app/capture.bin must match /app/samples.txt exactly.

/app/solve.py must compute the decode itself and be self-contained: it must not invoke or depend on /app/gnsslog (the utility will not be present when your program is graded) and must not require network access. It will be graded on other log files in the same format, recorded by the same receiver across its operating life, so handle the full range of values the format can carry — not only those resembling the sample.

Do not modify /app/gnsslog or /app/capture.bin. Only /app/solve.py is graded.

You have 3600 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.
Instruction B — is it hard enough to clear the bar, and if so what makes it hard? 


Hard enough — because reverse-engineering any binary is impossible for an agent

Too easy — the expected output for the sample log is provided so the model just matches it

Hard enough — because GNSS time systems are too obscure for a frontier model to know

Hard enough — it is graded on logs the sample never shows (other constellations and eras the format supports) and the decoder tool is absent at grading, so a solution that merely reproduces the sample under-generalizes with no oracle to catch it
Explain your reasoning for Instruction B 
In 2-4 sentences, explain why a frontier model fails Instruction B and name the strategy it uses.
Instruction C
A model-serving preprocessing recovery:

There's a feature pipeline in `/app/checkpoint`. A bad rollout left it unable to reproduce the model's predictions on the eval batch. Can you get them to match up?

Drive it with `servingctl` (`status`, `inspect <column>`, `run-eval`). The server is in `/opt/featserve`, read-only, leave it.

`schema.json` is the operator's preprocessing doc, one entry per column. `/app/checkpoint/bundle/fit_sample.json` is the raw reference data the preprocessing was fit on. `model.json` is the model, including the per-feature input stats it expects. Batch is `eval_batch.json`. The server doesn't preprocess, it only takes vectors. Build each row's input vector and write `/app/vectors.json`, keys the row ids, each value the feature list in column order.

`run-eval` reads `/app/vectors.json` and writes `/app/predictions.json`: a JSON object, key the row id as a string `"0"`-`"199"`, value the class id integer. Grader checks that.
Instruction C — is it hard enough to clear the bar, and if so what makes it hard? 


Hard enough — only because there are 200 rows to process

Too easy — it just says build the input vectors and run the server

Hard enough — the obvious move is to trust schema.json (the operator's doc) but it has drifted; the true preprocessing must be derived from the fit sample and the model's expected stats so a model that follows the doc is confidently wrong

Hard enough — because the model cannot produce JSON output
Explain your reasoning for Instruction C 
In 2-4 sentences, explain why a frontier model fails Instruction C and name the strategy it uses.


SOL
Instruction A (Fintech pipeline)
Instruction A — is it hard enough to clear the bar, and if so what makes it hard?

✅ Hard enough — it is a silent trap: the pipeline runs without errors and emits a plausible feature matrix either way, so the model commits to corrupted output with nothing signalling the bug
Explain your reasoning for Instruction A This task uses Strategy 1 (Silent trap) and Strategy 4 (Compound corrections). Because the pipeline runs without throwing exceptions and emits a perfectly formatted Parquet file regardless of internal logic errors, the agent is deprived of any failing signal (error trace or stack dump) to drive its iterate-test-fix loop. It will confidently apply a naive fix, see that the script runs cleanly, and submit a fundamentally flawed matrix.

Instruction B (GNSS binary decoder)
Instruction B — is it hard enough to clear the bar, and if so what makes it hard?

✅ Hard enough — it is graded on logs the sample never shows (other constellations and eras the format supports) and the decoder tool is absent at grading, so a solution that merely reproduces the sample under-generalizes with no oracle to catch it
Explain your reasoning for Instruction B This task brilliantly combines Strategy 2 (Hidden cases) and Strategy 3 (Remove self-verification). The prompt explicitly demands the agent handle the "full range of values the format can carry", but the provided sample intentionally only shows a narrow subset. A naive model will overfit to the visible sample, and because the gnsslog oracle is removed, it has no way to check its work against the hidden constellations and eras before committing.

Instruction C (Model-serving preprocessing)
Instruction C — is it hard enough to clear the bar, and if so what makes it hard?

✅ Hard enough — the obvious move is to trust schema.json (the operator's doc) but it has drifted; the true preprocessing must be derived from the fit sample and the model's expected stats so a model that follows the doc is confidently wrong
Explain your reasoning for Instruction C This task leans heavily on Strategy D (Spec-by-environment). Frontier models are highly conditioned to trust provided documentation; presenting schema.json creates a "helpfulness trap" where the obvious path is to simply implement the document. The model will confidently follow the drifted doc and fail, missing the fact that the actual, ground-truth spec must be reverse-engineered from the raw fit_sample.json and model binaries.
























Project Dynamo - How to stump the model
A short training + check on how to author Terminal-Bench tasks that a frontier model actually fails (avg@8 ≤ 0.5). Read each panel, then answer. Plan for ~25 minutes.

Apply it
Now show you can use the strategies.
Two short written answers. There are no exact-match keys — a reviewer (and an LLM grader) looks for whether your reasoning actually applies the strategies above: the silent trap, testing instruction-defined cases the samples never show, removing self-verification, compounding corrections, exact grading, and the additional patterns (no-single-wrong-line, bug-for-bug, minimal-diff, spec-by-environment, defeating the test-fix loop).

Diagnose and harden a too-easy proposal 
A proposal asks the agent to compute the ground-state eigenvalue of a quartic anharmonic oscillator using the shooting method with Numerov integration, graded by a tolerance on the single eigenvalue. In 3-5 sentences: (a) why does a frontier model clear this well above the bar, and (b) give two concrete changes that would push it below the bar.
Turn a mundane task into a trap 
Take an everyday task: parse an HTTP access log into a small JSON summary. Describe how you would design a version that makes a frontier model confidently wrong, and exactly how you would grade it. Name at least two of the strategies you are using.

SOL:
Here are the written responses applying the strategies to both scenarios:

Diagnose and harden a too-easy proposal
(a) Why the model clears it: A frontier model easily clears this because solving a quartic anharmonic oscillator using the shooting method + Numerov integration is a textbook computational physics recipe. This falls directly into the "named gotcha" trap; what seems like difficult domain knowledge to a human is instantly recognizable and executable on-sight by a model that has ingested every physics textbook.

(b) Two concrete changes:

Strategy D (Spec-by-environment): Instead of naming a known oscillator, provide a stripped black-box binary or raw numeric array representing an entirely bespoke, non-standard potential well that the model must empirically reverse-engineer.
Strategy 1 (Silent trap) & Strategy 5 (Grade exactly): Provide boilerplate integration code that runs perfectly but uses a subtly wrong boundary condition or step size for this specific bespoke well. Grade the single eigenvalue to a tight, problem-justified precision (e.g., 1e-6) that exactly excludes the output produced by the naive, uncorrected boilerplate.
Turn a mundane task into a trap (HTTP Access Log)
To turn a basic log-parsing task into a trap that makes a frontier model confidently wrong, I would introduce Strategy 2 (Test cases the instructions define but samples never show) and Strategy 4 (Compound several corrections).

The Design: I would instruct the agent to parse the log and emit a JSON summary of "total strictly compliant HTTP/1.1 requests" and the "unique count of requesting client IPs." However, the log format mixes standard requests with three overlapping edge cases: IPv6 addresses mapped as IPv4 (::ffff:192.0.2.128), HTTP/1.0 downgrade requests, and terminated slow-loris connection drops. The provided seed.log given to the agent would only contain perfectly formatted, standard IPv4 HTTP/1.1 requests.

The Grading: A naive regex script will parse seed.log perfectly, leading the model to lock in its solution. The hidden grading verifier would test against eval.log, exacting a strict integer match (Strategy 5) on the counts.

Because the model under-generalizes to the pristine sample log, its script will silently process eval.log without throwing any Python/bash exceptions (Strategy 1). The overlapping nature of the IPv6 mapping and protocol downgrades means if the model guesses one trap but not the other, the integer count still fails, ensuring a 0.0 reward.