# Project Dynamo: Mechanical Task Creation Flow

This document provides the minimal, step-by-step mechanical workflow for shipping a Harbor task from start to finish.

## 1. Claim & Propose
1. **Claim a Task:** Pick your favored category, filter for the subcategory, and claim the task. Write down the Category and Subcategory.
2. **Write the Proposal:** Define the idea and pass the automated proposal review *before* you build anything.

## 2. Fork & Scaffold
1. **Fork the Repo:** `gh repo fork handshake-project-dynamo/<your-task-repo> --clone`
2. **Create Branch:** `cd <your-task-repo>/task && git checkout -b submission`
3. **Verify Layout:** Do not rename or move top-level files. The layout must be:
   ```text
   task/
   ├── task.toml
   ├── instruction.md
   ├── solution/solve.sh
   ├── environment/Dockerfile
   ├── tests/{test.sh, test_outputs.py}
   ├── .dynamo/  .github/  .harbor/   # provided — do not edit
   └── README.md
   ```

## 3. Build the Environment & Solution
1. **Input Files:** Place any seed inputs in `environment/data/`.
2. **Dockerfile:** Edit `environment/Dockerfile` to define the task's single image. 
   * Use a strictly pinned, pre-approved base image from `public.ecr.aws` (must include `@sha256` digest).
   * `COPY` the `environment/data/` files in. 
   * Bake all test dependencies (`pytest`, `pytest-json-ctrf`) directly into the image. 
   * **Never** `COPY solution/` or `tests/` into the environment.
3. **Author Reference Solution:** Write `solution/solve.sh`. Keep heavy logic in helpers (e.g., `solution/solve.py`) that `solve.sh` calls. Ensure outputs are written to the absolute paths defined in `instruction.md`.

## 4. Write the Verifier
1. **`tests/test_outputs.py`:** Write one strict, value-based assertion per success criterion. Include a docstring mapping to the instruction.
2. **`tests/test.sh`:** 
   * Run the test suite: `pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA`
   * Write binary success (`1` or `0`) to `/logs/verifier/reward.txt`.
   * Must always conclude with `exit 0`.

## 5. Finalize Manifests
1. **`instruction.md`:** Write the prompt the agent reads. Describe *WHAT*, not *HOW*. Use absolute paths. Must be under 1,500 tokens. End with the exact mandatory timeout suffix (e.g., `"You have 120 seconds..."`).
2. **`task.toml`:** Fill out metadata. Ensure `artifacts` is a top-level array. Ensure `timeout_sec` values sync with your instruction.

## 6. Test & Submit
1. **Run Oracle:** `harbor run -p . -a oracle` (Must pass with Reward 1.0).
2. **Run Nop:** `harbor run -p . -a nop` (Must fail with Reward 0.0).
3. **Submit:** Open your Pull Request. The task must pass the automated Pass@2 and Pass@8 pipelines to be merged.