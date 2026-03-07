# GitHub Issues Backend Guide

> **Version:** 1.0 | **Last updated:** 2026-03-07

> **What this document is:** The concrete implementation guide for running operational work artifacts in GitHub Issues. Use this when `CONFIG.yaml → work_backend.type` is `github-issues`.

---

## Goal

This guide makes the GitHub issue backend operational without implicit knowledge.

If a human needs to approve something, the required label change is written out explicitly.
If GitHub needs configuration, the exact repo settings, labels, and issue forms are listed here.

Use this guide together with [WORK-BACKENDS.md](WORK-BACKENDS.md) and [REQUIRED-GITHUB-SETTINGS.md](REQUIRED-GITHUB-SETTINGS.md).

---

## Minimum Setup Checklist

Complete these steps before using the issue backend in a real fork:

1. Set `work_backend.type: "github-issues"` in `CONFIG.yaml`.
2. Enable GitHub Issues and Issue Forms in the repository settings.
3. Copy the sample forms from `docs/github-issues/forms/` into `.github/ISSUE_TEMPLATE/` in your instance repository.
4. Copy `docs/github-issues/config.sample.yml` to `.github/ISSUE_TEMPLATE/config.yml` in your instance repository and customize the links.
5. Create the required labels listed below.
6. Tell humans who approve work to use the approval transitions exactly as written in the approval table.
7. Keep Git-backed companion artifacts in the repository: signal digests, technical designs, quality evaluations, fleet reports, outcome reports, asset registry entries, governance exceptions, and locks.

---

## CONFIG.yaml Sample

Use this as the minimal GitHub-backed configuration:

```yaml
work_backend:
  type: "github-issues"

  github_issues:
    repo: ""                    # empty = same repo
    use_projects: true
    use_label_prefixes: true

  overrides:
    technical-design: "git-files"
    governance-exception: "git-files"
    asset-registry: "git-files"
```

Example for a dedicated issue repository:

```yaml
work_backend:
  type: "github-issues"

  github_issues:
    repo: "acme/operating-work"
    use_projects: true
    use_label_prefixes: true

  overrides:
    technical-design: "git-files"
    governance-exception: "git-files"
    asset-registry: "git-files"
```

---

## Required Labels

These labels are the minimum viable set for the issue backend.

### Artifact Labels

- `artifact:signal`
- `artifact:mission`
- `artifact:task`
- `artifact:decision`
- `artifact:release`
- `artifact:retrospective`

### Status Labels

- `status:new`
- `status:proposed`
- `status:approved`
- `status:planning`
- `status:active`
- `status:paused`
- `status:completed`
- `status:cancelled`
- `status:pending`
- `status:in-progress`
- `status:blocked`
- `status:proceed`
- `status:defer`
- `status:monitor`
- `status:done`
- `status:accepted`
- `status:superseded`
- `status:deprecated`
- `status:draft`
- `status:deploying`
- `status:deployed`
- `status:rolled-back`

### Layer Labels

- `layer:steering`
- `layer:strategy`
- `layer:orchestration`
- `layer:execution`
- `layer:quality`

### Loop Labels

- `loop:discover`
- `loop:build`
- `loop:ship`
- `loop:operate`

### Priority Labels

- `priority:critical`
- `priority:high`
- `priority:medium`
- `priority:low`

### Recommended Additional Labels

- `urgency:immediate`
- `urgency:next-cycle`
- `urgency:monitor`
- `category:market`
- `category:customer`
- `category:technical`
- `category:internal`
- `category:competitive`
- `category:financial`
- `confidence:high`
- `confidence:medium`
- `confidence:low`

### Label Rule

Use exactly one `status:` label per issue.
When the state changes, remove the old `status:*` label and add the new one in the same action.

---

## Label Bootstrap Sample

If you manage labels as code, this YAML structure is a practical starting point:

```yaml
labels:
  - name: "artifact:signal"
    color: "1D76DB"
    description: "Operational signal"
  - name: "artifact:mission"
    color: "5319E7"
    description: "Mission issue"
  - name: "artifact:task"
    color: "0E8A16"
    description: "Mission task"
  - name: "artifact:decision"
    color: "0052CC"
    description: "Decision record"
  - name: "artifact:release"
    color: "FBCA04"
    description: "Release contract"
  - name: "artifact:retrospective"
    color: "B60205"
    description: "Incident retrospective"
  - name: "status:new"
    color: "D4C5F9"
    description: "Freshly filed"
  - name: "status:proposed"
    color: "C2E0C6"
    description: "Awaiting human approval"
  - name: "status:approved"
    color: "0E8A16"
    description: "Approved by authorized human"
  - name: "status:active"
    color: "1D76DB"
    description: "Work is in flight"
  - name: "status:completed"
    color: "5319E7"
    description: "Work completed"
  - name: "status:blocked"
    color: "B60205"
    description: "Blocked pending action"
  - name: "status:draft"
    color: "F9D0C4"
    description: "Draft awaiting approval"
```

If you prefer GitHub CLI, create labels with `gh label create` using the same names.

---

## Human Approval Table

Humans should not have to guess what “approve” means.

Use these approval actions exactly:

| Artifact | Human action | Approval result |
|----------|--------------|-----------------|
| Signal | Review the issue, leave a short rationale comment, replace `status:new` with one of `status:proceed`, `status:defer`, `status:monitor`, or `status:done` | Signal is triaged |
| Mission | Review scope and outcome contract, leave a short approval comment, replace `status:proposed` with `status:approved` | Mission may move to planning |
| Decision | Review context and tradeoffs, leave a short approval comment, replace `status:proposed` with `status:accepted` | Decision is accepted |
| Release | Review rollout and rollback plan, leave a short approval comment, replace `status:draft` with `status:approved` | Deployment may begin |
| Retrospective | Review findings and follow-ups, leave a short approval comment, replace `status:draft` with `status:accepted` | Postmortem is closed |

Do not use issue closure as the approval signal.
Closure archives completed work. The label transition is the approval event.

---

## Human Operating Rules

These rules keep the issue backend consistent:

1. Never leave multiple `status:` labels on one issue.
2. Always leave a short comment when approving, rejecting, or cancelling.
3. Close completed work only after the final status label is applied.
4. Close child task issues before closing the parent mission issue.
5. For missions, keep the issue body as the current mission brief and use comments for running status updates.
6. For tasks, put acceptance criteria directly in the task issue body so execution and quality agents can evaluate against them.

---

## Sample Files To Copy Into An Instance Repo

This template repository keeps the operational GitHub issue forms as documentation samples so the framework repo itself does not behave like an instance repo.

Copy these into `.github/ISSUE_TEMPLATE/` in your company fork when you enable the issue backend:

- `docs/github-issues/config.sample.yml`
- `docs/github-issues/forms/signal.sample.yml`
- `docs/github-issues/forms/mission.sample.yml`
- `docs/github-issues/forms/task.sample.yml`
- `docs/github-issues/forms/decision.sample.yml`
- `docs/github-issues/forms/release.sample.yml`
- `docs/github-issues/forms/retrospective.sample.yml`

These samples pre-apply the base artifact labels and ask for the fields humans typically forget.

---

## GitHub Projects Recommendation

If `use_projects: true`, create these minimum views:

| Project View | Filter |
|--------------|--------|
| Signal Triage | `label:artifact:signal is:open` |
| Active Missions | `label:artifact:mission is:open` |
| Mission Tasks | `label:artifact:task is:open` |
| Release Pipeline | `label:artifact:release is:open` |

---

## Companion Git Artifacts That Still Matter

Even with GitHub Issues enabled, these stay in Git:

- `work/signals/digests/`
- `work/missions/<name>/TECHNICAL-DESIGN.md`
- `work/missions/<name>/evaluations/`
- `work/missions/<name>/FLEET-REPORT.md`
- `work/missions/<name>/OUTCOME-REPORT.md`
- `work/assets/`
- `work/decisions/EXC-*.md`
- `work/locks/`

The issue backend is for operational coordination.
Git still holds the durable review-heavy artifacts.

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-03-07 | Initial version — concrete GitHub issue-backend implementation guide |