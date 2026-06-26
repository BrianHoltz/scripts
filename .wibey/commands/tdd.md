---
name: tdd
description: TDD workflow enforcer — walks through the red-green-refactor cycle with gates, optionally through PR merge.
---

> [!NOTE]
> **Mirror-safe command.** This file contains no Walmart-proprietary content and is
> designed to be manually mirrored to personal laptops. The canonical copy lives in
> [`relationship-shared/.wibey/commands/`](https://gecgithub01.walmart.com/CatalogRelationships/relationship-shared).
> **If you are reading this outside of Walmart GHE, do not edit it here** — make
> changes in relationship-shared and re-sync.

# TDD Workflow

Execute a strict red-green-refactor cycle for the following change request. Steps are sequential — do not skip ahead.

- **Orient.** Read `AGENTS.md` if it exists. Identify the repo's build tool (maven, gradle, npm, etc.), test runner, and coverage tool. Check for postman/newman test collections. See [Running Tests](../docs/WibeyAgentRef.md#running-tests) for tool paths and IDE-specific gotchas.
- **Clarify.** Ask any clarifying questions about the intended behavior change before writing code.
- **Branch.** Pull main (`git pull origin main` on `main` branch), then create or switch to a feature branch. If there are uncommitted code changes, stop and ask the user to ensure a known-good state.
- **Baseline.** Run all unit tests. Verify any failures are pre-existing and expected.
- **Red.** Write test(s) that fail on the behavior being changed/added. Run them and confirm they fail. If they pass, the test isn't testing the right thing — revisit.
- **Green.** Implement the minimum changes to make the new tests pass.
- **Verify.** Run the new tests and closely related tests. If any fail, return to Green.
- **Full suite.** Run the full test suite. If any unexpected failures, return to Green.
- **Newman.** If postman/newman test collections exist for this service, ask the user to start the local server. When it's running, run the postman tests.
- **Coverage.** Run coverage analysis. Identify any new flows/conditions not covered. Add tests until 100% of new code paths are covered. If any are too difficult to test, ask for guidance.
- **Report.** Summarize what was changed, tests added, coverage result, and any remaining concerns.

## Ship It (optional)

After **Report**, ask the user whether they want to proceed to commit, push, and PR. If they decline (or don't mention it), stop here — the workflow is complete. If they authorize it, continue with the steps below. Each step requires explicit user consent before proceeding to the next.

- **Commit.** Stage all changed files and commit. Extract the Jira ticket ID from the branch name (e.g. `CATGTRLSHP-123`) and use it as the commit message prefix. If no ticket ID is in the branch name, use a conventional prefix (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`). Never fabricate a ticket ID. Present the draft commit message to the user for approval before committing.
- **Push.** Push the branch to origin (`git push -u origin <branch>`). If the push is rejected (e.g. force-push needed), stop and ask — never force-push without explicit consent.
- **PR.** Create or update a pull request using `gh pr create` (or `gh pr edit` if one already exists for the branch).
  - **Template discovery:** Look for a PR template in this order: `.github/PULL_REQUEST_TEMPLATE.md`, `docs/templates/pull_request_template.md` (this team's convention — see [pull_request_template.md](../docs/templates/pull_request_template.md)), then the repo root. If found, use it as the PR body skeleton — fill in each section based on the changes made. If no template exists, use a concise summary with sections: Description, Jira Tickets, Unit Testing, and Risk / Blast Radius.
  - **Sonar coverage note:** Include the local coverage percentage in the Unit Testing section so reviewers know what to expect from the Sonar gate.
  - Present the draft PR title and body to the user for approval before creating.

## CICD (optional)

After **PR**, ask whether the user wants to monitor CICD. If they decline, stop here. If they authorize it, continue below.

- **Watch.** Open a headed agent-browser session (follow all rules in [WibeyBrowserPatterns.md](../docs/WibeyBrowserPatterns.md) — `--headed`, own session via `$$`, pre-warmed cookies, never close). Navigate to the PR's checks page and poll for CICD completion:
  - Use `gh pr checks <number> --watch` as the primary polling mechanism (CLI-native, no browser needed for status). Fall back to browser-based polling only if the CLI doesn't surface the checks you need (e.g. Looper/Concord pipelines that report via external status).
  - Poll every 60 seconds. Report status changes to the user as they happen (e.g. "Build passed, Sonar running…").
  - If any check requires deployment approval (e.g. Concord promote form), follow the [Concord promote form detection](../docs/WibeyAgentRef.md#safety-warnings) rules: check the **Status tab** (not just Logs) when a process shows SUSPENDED, use the **custom view** (not the raw form), and **stop at the stg/prod boundary** — alert the user and wait for explicit "yes" before clicking Approve.

- **Sonar.** When the SonarQube/SonarCloud check completes:
  - If coverage meets the project's quality gate, report the score and move on.
  - If coverage is below the gate, identify the uncovered lines by examining the Sonar report (via browser or Sonar API if available). Write additional tests to cover the gaps, targeting as close to 100% new-code coverage as practical. Then: commit the new tests, push, and return to **Watch** to re-poll. Repeat until the Sonar gate passes or coverage gains become impractical (e.g. unreachable branches, framework-generated code). If you plateau, report the remaining gaps and ask the user for guidance.

- **Triage.** If any CICD check fails:
  - Capture the failure details (logs, error messages, screenshots via agent-browser).
  - **Large log files:** CICD logs can be tens of thousands of lines. Do not try to read them in-browser — agent-browser snapshots truncate and the context window fills up fast. Instead, download the log to a local file (via `curl`, `gh api`, or the platform's log-download URL) and then search/grep it on disk for the relevant error. This is faster, more reliable, and lets you re-read specific sections without re-fetching.
  - Diagnose the root cause. Common categories: compilation error, test failure, linting/checkstyle, dependency resolution, infrastructure flake.
  - If it's a code issue you can fix: fix it locally, add tests if needed, commit, push, and return to **Watch**.
  - If it's an infrastructure flake (e.g. timeout, registry unavailable): retry the check if the platform supports it (`gh pr checks --watch` will pick up the re-run). If it fails again, report to the user.
  - If it's something you can't diagnose or fix (permissions, secrets, environment config): report the full error context to the user and stop.
  - Track each triage iteration — don't loop indefinitely. After 5 failed fix attempts on the same check, stop and escalate to the user.

- **Green build.** When all checks pass, report the final status: PR URL, check results summary, Sonar coverage score, and any caveats. Do not merge — merging is a separate decision for the user or reviewers.
