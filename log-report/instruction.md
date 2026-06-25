Parse the Apache-style access log at `/app/access.log` and write a JSON report to `/app/report.json`.

The report must be a JSON object with exactly these keys:

1. `total_requests` — the total number of log lines (integer).
2. `unique_ips` — the count of distinct client IP addresses (integer).
3. `top_path` — the most frequently requested URL path (string).

Do not modify `/app/access.log`.

You have 120 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.
