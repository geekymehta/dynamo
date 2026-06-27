# Project Dynamo: Authoring Strategies & Difficulty Design

This document contains the complete and definitive guidance on engineering Terminal-Bench tasks for Project Dynamo. It preserves every rule, strategy, constraint, and example needed to meet the difficulty bar.

---

## 1. Key Updates & Platform Rules

### Manifest (`task.toml`)
The reference `task.toml` is a single canonical block. Do not modify the structure:
* `[task]`
* `[metadata]` (grouped into pre-seeded / fixed-dataset / fellow-set fields)
* `[verifier]`
* `[agent]`
* `[environment]` (including `mcp_servers`)

**Important Changes:**
* `avg_at_8` has been removed as a `task.toml` field. Pass@8 acceptance is evaluated by the pipeline.
* `[verifier].environment_mode` should be left unset. The verifier runs inside the task's single `environment/Dockerfile` image (canonical TB2). Harbor overlays `tests/` at verification time. There is no separate `tests/Dockerfile`.
* `category` and `subcategory` are pre-seeded by the Dynamo team and must not be modified.
* Contributors only set `task_objective` and `artifact_type` (using lowercase `snake_case` from `.dynamo/diversity-taxonomy.toml`).

### Instructions (`instruction.md`)
* Now has a **1,500-token limit**.
* Any structured-output schema should be documented directly in the prompt or in a referenced specification file (the separate structured-output line in TOML is removed).

### Evaluation Pipeline (The Difficulty Bar)
The acceptance bar is high: A task must produce **at least 4 valid failures out of 8 trials**, measured using GPT-5.4 at extra-high reasoning effort (Terminus-2).
* **Valid Failures Only:** Timeouts, infrastructure issues, and instruction/verifier misalignment do NOT count. Any failure caused by misalignment is blocking.
* **Stage 1 (Pass@2):** Two trials are run. At least one valid failure is required. Includes LLM analysis of runs.
* **Stage 2 (Pass@8):** Triggered only after Pass@2 succeeds. Eight new trials are executed. At least 4 valid failures are required. Submissions are blocked until these checks clear.

*(Note: During focused push periods, reaching the RTD layer can carry a bonus incentive—see official update channels).*

---

## 2. The Core Philosophy
**The bar:** Every task must reach `avg@8 ≤ 0.5`.
**The single most important idea:** A hard task does not depend on the model *not knowing* something. It depends on the model being **confidently wrong**—running the obvious solution, getting output that looks right, and committing to it. Frontier models have read every textbook, CVE, and blog. Obscurity is not difficulty.

---

## 3. The Five Core Strategies
These five ways to make a model confidently wrong are distilled from delivered tasks that measured `avg@8 ≤ 0.5`.

### 1. Silent trap — the obvious solution runs clean and is wrong
The naive approach completes without error and produces believable output. Avoid bugs that throw exceptions—a model fixes anything that throws.
* **Delivered Example (`silent-feature-bugs`):** Two refactor-introduced bugs (timezone-agnostic windowing and pre-split target-encoding leakage) are invisible at runtime and must be fixed together because their effects interact. The pipeline emits a plausible feature matrix either way.

### 2. Test cases the instructions define but the samples never show
Ship samples/spec that the naive reading reproduces perfectly, then grade on cases that a faithful reading of the instructions fully determines but the samples never exemplify. The model overfits to the visible examples. Every graded case must be unambiguously derivable from the instructions (no surprise requirements).
* **Delivered Example (`gnss-log-decode`):** Instructions call for decoding all constellations/eras the format supports, but the shipped samples contain only GPS fixes in one era. Graded captures add BeiDou (different epoch/offset) and other eras.

### 3. Remove the model’s ability to self-verify
If the environment holds an oracle (a reference binary, a way to check work), the model uses it. Take it away.
* **Delivered Example (`tokenizer-recovery`):** Correct token IDs depend on hidden subsets (no-marker vocab entries, alternate Unicode normalization, multi-piece segmentation) across 205 inputs. Nothing flags which inputs are affected.

### 4. Compound several corrections that must compose in order
One trap is guessable. Several independent overlapping corrections—where fixing some but not all still fails—push the pass rate down hard.
* **Delivered Example (`slo-breach-recovery`):** Five mixed encodings in one metric dump (millisecond vs second timestamps, cumulative counters, counter resets, per-second rates, failed-scrape sentinels). Handling only some produces wrong counts.

### 5. Grade exactly, so plausible-but-wrong fails
Loose tolerances let a near-miss pass. Set the band wide enough to admit every genuinely-compliant method, yet tight enough that any requirement-violating method falls outside it.
* **Delivered Example (`migrate-colorkit`):** The naive sRGB port violates the gamma requirement and lands ~0.15 off in luminance. The tolerance is 0.02—wide enough that correct decodes pass, but tight enough that the requirement-violating method fails every tile.

---

## 4. The #1 Trap: The Named Gotcha
If a specialist can name the bug, so can the model. The most common reason a proposal is too easy: the trap is a recognizable concept.

**Example 1: Unicode Normalization**
* **Before:** “Find and fix an account service that de-duplicates usernames with NFC but resolves with NFKC, allowing an impersonation collision.” (The model spots this famous music-streaming bug instantly).
* **Harden it:** Stop asking the model to *find* a nameable bug. Give a service that looks correct. Grade on hidden confusable pairs from scripts the seed never shows. Remove the word “normalization” entirely and grade exact downstream resolution outcomes.

**Other famous named recipes to avoid spelling out:**
* ECDSA biased-nonce key recovery (Textbook Hidden Number Problem solved by LLL / Minerva).
* Async CDC-FIFO repair (Metastability / Gray-code pointers).
* Quartic-oscillator eigenvalue (Shooting method + Numerov). *Instead: give a stripped binary potential well (Spec-by-environment) and a clean but subtly wrong boilerplate.*

---

## 5. More Ways to Stump the Model

* **A. No single wrong line (emergent / timing):** Models struggle when no file is wrong locally. Example: A work-queue task where a stale lease completion recycles a token already reissued to another record (no exception, no error counter).
* **B. Bug-for-bug preservation (the helpfulness trap):** Models want to "improve" code. Example: A Fortran→Rust port must reproduce exact legacy behavior (persistent SAVE state, integer division, bit-aliasing), not the clean modern equivalent.
* **C. Minimal-diff / “nothing to change here”:** The correct fix is tiny (or absent) and a hidden regression suite checks untouched behavior.
* **D. Spec-by-environment (underspecified on purpose):** Put the contract in an opaque artifact. Example: `gnss-log-decode` requires recovering vendor CRC parameters and time conventions from a stripped binary, never read from the prompt.
* **E. Defeat the iterate-test-fix loop:** Ensure the agent's run-test-fix cycle ends "successfully" on a wrong answer without visible failing signals.

**Underused High-Yield Domains:** Concurrency & synchronization debugging, reverse engineering, compilers/interpreters, time/calendar arithmetic, and stateful protocol handshakes.
**Winning Proposal Examples:** An HTTP edge-cache proxy returning stale responses (hidden cases); a vertically-integrated cannabis-tax computation hinging on narrow doctrine graded to the exact dollar.

---

## 6. Fair vs. Unfair Verifiers

**Hidden Cases (Strategy 2):**
* **FAIR:** Prompt says “decode every record type,” sample shows one, grader tests the others.
* **UNFAIR:** Prompt says “produce the report for the provided log,” but the verifier grades a different log (Surprise requirement).
* **UNFAIR:** The verifier checks a column/behavior the instruction never mentions.

**Exact Grading (Strategy 5):**
* **FAIR:** Discrete outputs (integer counts, exact dollars, class IDs) or precisions the prompt explicitly states ("round to 4 decimals").
* **UNFAIR:** A float graded to `1e-9` with no stated precision, failing alternative valid numerical libraries.

---

## 7. Real Instruction Examples (Why they stump models)

**Instruction A (Fintech pipeline)**
* **Why it passes the bar:** It uses Strategy 1 (Silent Trap) and Strategy 4 (Compound Corrections). The pipeline runs cleanly and emits a Parquet file regardless of internal logic errors. The model gets no error trace, applies a naive fix, sees it run cleanly, and confidently submits a corrupted matrix.

**Instruction B (GNSS binary decoder)**
* **Why it passes the bar:** It combines Strategy 2 (Hidden Cases) and Strategy 3 (Remove Self-Verify). The prompt demands full constellation support, but the sample only shows GPS. The oracle `gnsslog` tool is removed at grading. The model overfits to the visible sample and has no way to check its work against hidden constellations.

**Instruction C (Model-serving preprocessing)**
* **Why it passes the bar:** Uses Strategy D (Spec-by-environment). Frontier models trust documentation blindly. Providing a drifted `schema.json` creates a "helpfulness trap." The model implements the out-of-date document rather than reverse-engineering the true spec from the raw `fit_sample.json`.

**Instruction D (HTTP Access Log parsing)**
* **Design Trap:** Mix standard requests with overlapping edge cases (IPv6 mapped as IPv4, HTTP/1.0 downgrades, terminated slow-loris). Give a `seed.log` with only standard IPv4 HTTP/1.1 requests.
* **Grading:** A naive regex passes the seed log. The hidden verifier tests `eval.log` with a strict integer match (Strategy 5). The model's script silently drops the traps without crashing (Strategy 1), failing the exact count.
