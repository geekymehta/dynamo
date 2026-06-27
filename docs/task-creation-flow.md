Creating a task
Note down your Category and Sub-category when claiming
When you claim a task, write down the Category and Sub-category you picked — you'll need to enter them in the proposal stage.

You build one Harbor task at the root of your forked task repo. The steps below depend on each other, so it's easiest to work them in order, but there's no required commit structure — commit however you like and iterate freely. Test locally with the oracle before you open a PR.

Before you start, skim Examples & Strategies — reading a good repo end-to-end is the fastest way to get a feel for what a strong task looks like.

Claim a task — pick your favored category, then filter for the appropriate subcategory and claim the task.
Write the proposal — define the idea and pass the automated proposal review before you build anything.
Scaffold & branch — fork your task repo, git checkout -b submission, and review the files already in place (see Task File Structure).
Author solve.sh — your reference solution. Keep real logic in helpers (e.g. solution/solve.py) it calls; write outputs to the absolute paths instruction.md names.
Write the tests — tests/test_outputs.py (one assertion per criterion, each with a docstring) and tests/test.sh (runs pytest, writes the reward to /logs/verifier/reward.txt). Bake test dependencies into the single environment/Dockerfile.
Build the Dockerfile — environment/Dockerfile defines the task's single image (agent + verifier); put inputs in environment/data/ and COPY them in. Never COPY solution/ or tests/.
Write instruction.md and task.toml — the prompt the agent reads (end with the "You have N seconds…" line) and the manifest (see the task.toml reference).
Then run the oracle locally (step 8), clear the wrap-up checklist, and open your PR.

Difficulty comes from reasoning
Make the task hard for a person, not for the computer. Difficulty should come from reasoning — not from cranking up CPU, memory, or wall-clock time. The agent has open internet, so the answer must not be findable online.