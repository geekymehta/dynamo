3 · Fork & Set up the repo
You were assigned a task repo under handshake-project-dynamo. Fork it, clone your fork, and make a working branch — you propose changes back via a pull request.

gh repo fork handshake-project-dynamo/<your-task-repo> --clone
cd <your-task-repo>/task
git checkout -b submission

Copy
The task scaffold lives in the /task folder in the repo. The repo is already scaffolded, with the task under that task/ directory. Confirm the layout (don't rename or move top-level files):

task/
├── task.toml
├── instruction.md
├── solution/solve.sh
├── environment/Dockerfile
├── tests/{Dockerfile, test.sh, test_outputs.py}
├── .dynamo/  .github/  .harbor/   # provided — do not edit
└── README.md

Copy
If your task needs input files, put them under environment/data/; the Dockerfile copies them into the agent's container.

Work through each item.

Checklist
0 of 3 complete


Forked and cloned your task repo; on the submission branch

Layout confirmed — task lives under task/, top-level files intact

Input/seed files (if any) placed under environment/data/