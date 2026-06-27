# Project Dynamo: Proposal Writing Guide

Before you build a task, you must submit a short proposal describing your idea. An automated reviewer will return specific feedback (Pass/Fail). You must revise and resubmit until it passes before scaffolding the repository. 

A proposal is judged on the idea, not on polished prose. Do not include solution or test code.

## The Four Requirements
Every proposal must comprehensively answer the following four questions:

1. **The Difficulty:** What the task is and why it's genuinely hard for an expert. Name the specific reasoning, domain knowledge, or multi-step problem-solving involved. Detail who in the real world does this work, where the data comes from (synthetic vs real), and how it reflects realistic complexity. Avoid vague statements like "this is hard."
2. **The Intended Approach:** A high-level strategy and the key insight required to solve it. Provide enough detail that another expert immediately understands the path to victory. Include a best-case expert-time estimate (focused hours for a senior practitioner who already knows the approach).
3. **How it will be Verified:** What exact output the agent must produce and how a program will deterministically check it. If you accept a range/tolerance instead of an exact answer, state exactly what the band brackets and justify why it admits valid variations while rejecting flawed methods.
4. **Category & Sub-category Justification:** A brief justification for why this task fits the chosen category/subcategory. Ground it in the task's actual reasoning and domain. *Note: Do not edit the pre-filled Category/Sub-category input fields in the template; put your justification in the final answer box.*

## Why Proposals Fail
The automated reviewer holds ideas to a very high bar. The most common rejection reasons are:
* Difficulty stated vaguely ("requires expertise").
* Claiming a solution exists without actually conveying the key insight/strategy.
* Tolerances or numeric ranges provided without mathematical/domain justification.
* Missing expert-time estimate.
* The task is a standard textbook problem or a "named gotcha" with a well-known solution.
* Grading that mandates *how* the agent solves it, rather than inspecting the final result.

## Worked Example — A Passing Proposal
**Task:** Implement a concurrent C++ larger-than-memory key-value store that beats Microsoft FASTER on the YCSB-A benchmark, in one shot, inside a 4-CPU / 2 GB container.

**1. Difficulty:** The ~3 GB dataset exceeds the 2 GB container, so a naive approach thrashes or runs out of memory — a real larger-than-memory architecture (compact in-memory index + on-disk value log) is mandatory just to load. Beating a 7-year-optimized production system is genuine storage-systems R&D, the day-job of engineers who build databases and caches.

**2. Approach (Key Insight):** Specialization beats generality. Exploit the fixed, known workload — fixed-size values, integer keys, a small hot key-set, fixed core count — to shed the overhead FASTER pays for being general-purpose (variable-length records, full recovery, general garbage collection). A senior systems engineer who holds this design could implement it in ~2–3 focused days.

**3. Verification:** Deterministic gates — correctness/anti-cheat tests, proof that values are actually on disk, and a throughput comparison run in the same harness as FASTER (median of 5 runs, run-phase only, identical traces). The pass bar allows a small margin to absorb measured run-to-run jitter while still rejecting a genuinely slower solution.

**4. Category Justification:** Belongs in `software_engineering` / `systems_programming` because it relies heavily on native memory management, POSIX disk I/O, and concurrent data structures.