# Work Backends — Git Files vs. Issue Tracker

> **Version:** 1.1 | **Last updated:** 2026-03-07

> **What this document is:** A comprehensive guide to how work artifacts can be tracked using different backends — either as Markdown files in Git (the original model) or as issues in an issue tracker (GitHub Issues, Jira, Linear, etc.).

---

## Why Two Backends?

The operating model defines **what artifacts exist** and **how they flow** between layers and loops. The original framework tracked everything as Markdown files in `work/`. This is fully self-contained and auditable, but creates friction for human collaboration:

- **Visibility:** Scanning 20+ Markdown files to understand mission status is harder than glancing at a labeled issue board.
- **Interaction:** Commenting, assigning, re-labeling, and triaging are native to issue trackers — and clunky via file edits + PRs.
- **Notifications:** Issue trackers have built-in notification, mention, and subscription systems.
- **Mobile:** Issue trackers work well on mobile. Editing Markdown in a repo does not.
- **Collaboration:** Discussion threads, reactions, and cross-references are first-class in issue trackers.

The framework now supports **both backends**. The choice is made at instance configuration time via `CONFIG.yaml → work_backend`.

---

## The Three File Categories

Not everything moves. The framework distinguishes three categories:

### 1. Governance Backbone — Always in Git

These define the **structure, rules, and shape** of the organization. They change slowly and deliberately. They are **never** tracked in an issue system.

| What | Location | Why Git |
|------|----------|---------|
| Org structure | `org/` | Defines layers, divisions, agent types |
| Quality policies | `org/4-quality/policies/` | Law — changes need PR review |
| Agent instructions | `org/*/AGENT.md` | Agent behavior boundary — needs version control |
| Agent type registry | `org/agents/` | Governed lifecycle (proposed → active → deprecated) |
| Process definitions | `process/` | Loop-by-loop guides |
| Integration registry | `org/integrations/` | Governed connections to external tools |
| Configuration | `CONFIG.yaml` | Source of truth for everything configurable |
| Global rules | `AGENTS.md`, `CLAUDE.md` | Non-negotiable agent rules |
| Templates | `_TEMPLATE-*.md` everywhere | Schema definitions — stay in Git as references |

### 2. Persistent Documentation Artifacts — Always in Git

These are **long-lived deliverables** that benefit from version control, code review, and diff history.

| Artifact | Why Git |
|----------|---------|
| **Technical Designs** | Architecture decisions tightly coupled to code — need PR-based review |
| **Asset Registry Entries** | Persistent documentation references — part of the knowledge base |
| **Governance Exceptions** | Audit-critical — time-bounded policy overrides need full traceability |
| **Runbooks** | Operational procedures co-located with service definitions |
| **Signal Digests** | Weekly synthesis artifacts consumed across layers — diffable history matters more than issue interaction |
| **Quality Evaluation Reports** | Immutable evidence artifacts that should not be edited through issue comments |
| **Outcome Reports** | Measured results against the outcome contract — stored as durable mission evidence |
| **Fleet Performance Reports** | Periodic fleet analysis that benefits from file-based version history |

### 3. Operational Work Artifacts — Configurable Backend

These are the **dynamic, frequently-changing** artifacts that track active work. They can live in Git files OR in an issue tracker.

| Artifact | Git Files | Issue Tracker |
|----------|-----------|--------------|
| **Signals** | `work/signals/YYYY-MM-DD-name.md` | Issue with `artifact:signal` label |
| **Missions** | `work/missions/<name>/BRIEF.md` | Issue with `artifact:mission` label |
| **Outcome Contracts** | `work/missions/<name>/OUTCOME-CONTRACT.md` | Section in mission issue body or linked issue |
| **Mission Status** | `work/missions/<name>/STATUS.md` (append-only) | Comments on mission issue |
| **Tasks** | `work/missions/<name>/TASKS.md` | Sub-issues linked to mission issue |
| **Decision Records** | `work/decisions/YYYY-MM-DD-name.md` | Issue with `artifact:decision` label |
| **Release Contracts** | `work/releases/YYYY-MM-DD-name.md` | Issue with `artifact:release` label |
| **Retrospectives** | `work/retrospectives/YYYY-MM-DD-name.md` | Issue with `artifact:retrospective` label |
| **Locks** | `work/locks/<lock-id>.md` | Not applicable — locks stay in Git (concurrency mechanism) |

---

## Configuring the Work Backend

Set the backend in `CONFIG.yaml`:

```yaml
work_backend:
  type: "github-issues"    # "git-files" | "github-issues"

  github_issues:
    repo: ""                # empty = same repo; or "org/repo" for separate issue repo
    use_projects: true      # use GitHub Projects for Kanban board views
    use_label_prefixes: true # use artifact:, status:, layer: prefixes

  overrides:
    # Force specific artifacts to a backend regardless of the global type.
    # Useful when most work is in issues but some artifacts must stay in Git.
    technical-design: "git-files"
    governance-exception: "git-files"
    asset-registry: "git-files"
    # lock: "git-files"  ← always git, not configurable
```

When `work_backend.type` is `"git-files"` (the default), the framework behaves exactly as before — all work artifacts are Markdown files in `work/`.

---

## Issue Backend: Label Taxonomy

When using an issue tracker, **labels replace file paths and YAML frontmatter** as the primary metadata mechanism. The following label taxonomy provides the same structural information that the Markdown templates encode.

### Artifact Type Labels (`artifact:`)

| Label | Maps to Template |
|-------|-----------------|
| `artifact:signal` | `_TEMPLATE-signal.md` |
| `artifact:mission` | `_TEMPLATE-mission-brief.md` |
| `artifact:task` | `_TEMPLATE-tasks.md` (individual task) |
| `artifact:decision` | `_TEMPLATE-decision-record.md` |
| `artifact:release` | `_TEMPLATE-release-contract.md` |
| `artifact:retrospective` | `_TEMPLATE-postmortem.md` |
| `artifact:governance-exception` | `_TEMPLATE-governance-exception.md` |

### Status Labels (`status:`)

Status labels are shared across artifact types. Apply the relevant ones:

| Label | Used By |
|-------|---------|
| `status:new` | Signals (freshly filed) |
| `status:proposed` | Missions, Decisions, Governance Exceptions |
| `status:approved` | Missions, Decisions, Releases, Governance Exceptions |
| `status:planning` | Missions |
| `status:active` | Missions |
| `status:paused` | Missions |
| `status:completed` | Missions, Tasks |
| `status:cancelled` | Missions, Tasks |
| `status:pending` | Tasks |
| `status:in-progress` | Tasks |
| `status:blocked` | Tasks |
| `status:proceed` | Signals (disposition: proceed to mission) |
| `status:defer` | Signals |
| `status:monitor` | Signals |
| `status:done` | Signals |
| `status:accepted` | Decisions, Retrospectives |
| `status:deprecated` | Decisions |
| `status:superseded` | Decisions |
| `status:draft` | Releases, Retrospectives |
| `status:deploying` | Releases |
| `status:deployed` | Releases |
| `status:rolled-back` | Releases |
| `status:pass` | Quality Evaluations |
| `status:fail` | Quality Evaluations |
| `status:escalate` | Quality Evaluations |

**Status label rule:** Use exactly one `status:` label per issue. When the artifact advances, remove the old `status:*` label and add the new one in the same action.

### Layer Labels (`layer:`)

Which organizational layer owns or originated this artifact.

| Label | Layer |
|-------|-------|
| `layer:steering` | Layer 0 — Steering |
| `layer:strategy` | Layer 1 — Strategy |
| `layer:orchestration` | Layer 2 — Orchestration |
| `layer:execution` | Layer 3 — Execution |
| `layer:quality` | Layer 4 — Quality |

### Loop Labels (`loop:`)

Which process loop this artifact belongs to.

| Label | Loop |
|-------|------|
| `loop:discover` | Discover & Decide |
| `loop:build` | Design & Build |
| `loop:ship` | Validate & Ship |
| `loop:operate` | Operate & Evolve |

### Priority Labels (`priority:`)

| Label | Meaning |
|-------|---------|
| `priority:critical` | Blocking — immediate action required |
| `priority:high` | Important — next cycle |
| `priority:medium` | Normal priority |
| `priority:low` | Nice to have |

### Signal-Specific Labels

| Label | Meaning |
|-------|---------|
| `urgency:immediate` | Needs action now |
| `urgency:next-cycle` | Next triage cycle |
| `urgency:monitor` | Watch and wait |
| `category:market` | Market signal |
| `category:customer` | Customer signal |
| `category:technical` | Technical signal |
| `category:internal` | Internal signal |
| `category:competitive` | Competitive signal |
| `category:financial` | Financial signal |
| `confidence:high` | High confidence in signal |
| `confidence:medium` | Medium confidence |
| `confidence:low` | Low confidence |

### Division Labels (`division:`)

Created dynamically based on configured divisions in `CONFIG.yaml`. Examples:

- `division:data-foundation`
- `division:core-services`
- `division:customer-experience`
- `division:engineering-foundation`

### Quality Verdict Labels (`verdict:`)

| Label | Meaning |
|-------|---------|
| `verdict:pass` | Quality evaluation passed |
| `verdict:pass-with-notes` | Passed with observations |
| `verdict:fail` | Failed — blocking issues found |
| `verdict:escalate` | Needs human judgment |

### Severity Labels (for retrospectives)

| Label | Meaning |
|-------|---------|
| `severity:sev1` | Critical outage |
| `severity:sev2` | Major impact |
| `severity:sev3` | Moderate impact |
| `severity:sev4` | Minor impact |

---

## Issue Backend: Structural Conventions

For an operational GitHub implementation, including issue forms, human approval steps, and label bootstrap samples, see [docs/GITHUB-ISSUES.md](GITHUB-ISSUES.md).

### Missions as Issue Hierarchies

A **mission** in the issue backend is an issue with `artifact:mission` label. Its structure:

```
Mission Issue (#42)
  ├── artifact:mission, status:active, layer:strategy, loop:build
  ├── Body: Mission brief content (from template structure)
  ├── Comment: Outcome Contract (or linked issue)
  ├── Comment: Status Update 1 (newest first)
  ├── Comment: Status Update 2
  │
  ├── Sub-Issue: Task 1 (#43) — artifact:task, status:in-progress, division:core-services
  ├── Sub-Issue: Task 2 (#44) — artifact:task, status:pending, division:data-foundation
  └── Sub-Issue: Task 3 (#45) — artifact:task, status:blocked, division:engineering-foundation
```

Git-backed companion artifacts still exist alongside the issue hierarchy where required:

- `work/signals/digests/YYYY-WXX-digest.md`
- `work/missions/<name>/evaluations/*.md`
- `work/missions/<name>/OUTCOME-REPORT.md`
- `work/missions/<name>/FLEET-REPORT.md`
- `work/missions/<name>/TECHNICAL-DESIGN.md` (when required)

### Cross-References

- **Signal → Mission:** Mission issue body references signal issue: "Origin: #31"
- **Mission → Tasks:** Tasks are sub-issues of the mission issue
- **Task → PR:** Task issue links to implementing PR(s)
- **Quality Eval → Mission:** Git evaluation report references the mission issue and task issue
- **Retrospective → Signal:** Retro issue references generated signal issues
- **Decision → Mission:** Decision issue references the mission it supports

### Issue Templates

GitHub Issue Templates (`.github/ISSUE_TEMPLATE/`) can mirror the Markdown templates. In this template repository, the operational forms are stored as docs-only samples under `docs/github-issues/forms/` so the framework repo itself does not behave like an instance repo.

- `signal.sample.yml` — maps to `_TEMPLATE-signal.md`
- `mission.sample.yml` — maps to `_TEMPLATE-mission-brief.md`
- `task.sample.yml` — maps to `_TEMPLATE-tasks.md`
- `decision.sample.yml` — maps to `_TEMPLATE-decision-record.md`
- `release.sample.yml` — maps to `_TEMPLATE-release-contract.md`
- `retrospective.sample.yml` — maps to `_TEMPLATE-postmortem.md`

Instance repos should copy these samples into `.github/ISSUE_TEMPLATE/` when enabling the issue backend. Agents can still create issues with structured body text directly.

### GitHub Projects Integration

When `use_projects: true`, create GitHub Projects boards for visual tracking:

| Board | View | Filter |
|-------|------|--------|
| **Signal Triage** | Board (Kanban) | `label:artifact:signal` |
| **Active Missions** | Board (Kanban) | `label:artifact:mission` |
| **Mission Tasks** | Board per mission | `label:artifact:task` + mission reference |
| **Release Pipeline** | Board (Kanban) | `label:artifact:release` |
| **Quality Dashboard** | Table | Mission-linked Git reports + evaluation references |

---

## Agent Behavior Differences by Backend

### Creating Artifacts

| Action | Git Files Backend | Issue Backend |
|--------|-------------------|---------------|
| File a signal | Create `work/signals/YYYY-MM-DD-name.md`, commit, open PR | Create issue with `artifact:signal` + metadata labels |
| Create a mission | Create `work/missions/<name>/BRIEF.md`, commit, open PR | Create issue with `artifact:mission` label, body from template |
| Decompose tasks | Edit `TASKS.md`, commit | Create sub-issues with `artifact:task` labels |
| Update status | Append to `STATUS.md`, commit | Add comment to mission issue, update status labels |
| Quality evaluation | Create `evaluations/*.md`, commit | Create `evaluations/*.md`, commit, and reference the mission/task issues |
| Decision record | Create `work/decisions/*.md`, commit, open PR | Create issue with `artifact:decision` label |
| Close mission | Update status in files, archive folder | Close issue, update labels to `status:completed` |

### Approval Mechanisms

| Mechanism | Git Files Backend | Issue Backend |
|-----------|-------------------|---------------|
| Signal triage | PR merge = approval | Authorized human removes `status:new` and applies exactly one of `status:proceed`, `status:defer`, `status:monitor`, or `status:done` |
| Mission approval | PR merge = approval | Label change (`status:proposed` → `status:approved`) by authorized human |
| Decision approval | PR merge = approval | Label change (`status:proposed` → `status:accepted`) by authorized human |
| Quality gate | Evaluation file with PASS verdict | Evaluation file in Git references the issue-backed mission/task |
| Release go/no-go | PR merge = approval | Label change (`status:draft` → `status:approved`) by authorized human |

### Human Approval Cheat Sheet

When humans are the approval gate in the issue backend, the action should be explicit and mechanical:

| Artifact | Human does this | Approval result |
|----------|-----------------|-----------------|
| Signal | Review the issue, leave a short rationale comment, replace `status:new` with one terminal triage label | Signal is triaged |
| Mission | Confirm scope/outcomes, leave a short approval comment, replace `status:proposed` with `status:approved` | Mission can move to planning |
| Decision | Review context and tradeoffs, leave a short approval comment, replace `status:proposed` with `status:accepted` | Decision becomes active |
| Release | Review rollout and rollback plan, leave a short approval comment, replace `status:draft` with `status:approved` | Deployment may begin |
| Retrospective | Review findings and follow-ups, leave a short approval comment, replace `status:draft` with `status:accepted` | Postmortem is closed |

Do not rely on issue closure alone as approval. Closure archives work; the `status:` label change is the approval event.

### Audit Trail

| Aspect | Git Files Backend | Issue Backend |
|--------|-------------------|---------------|
| Who changed what | Git blame + commit history | Issue activity log + label change history |
| When | Commit timestamps | Issue event timestamps |
| Why | Commit messages + PR descriptions | Issue comments + label change context |
| Completeness | Full — Git captures everything | Full — issue trackers log all events |

---

## Migration Between Backends

### Git Files → Issue Backend

1. Set `work_backend.type: "github-issues"` in `CONFIG.yaml`
2. For each active artifact in `work/`, create a corresponding issue with appropriate labels
3. Keep Git-only artifacts in place (`TECHNICAL-DESIGN.md`, evaluation reports, fleet reports, outcome reports, signal digests, asset registry, governance exceptions, locks)
4. Archive (don't delete) only the Git-file operational artifacts that moved to issues — they remain as historical record
5. Going forward, agents create issues instead of files for configurable artifacts

### Issue Backend → Git Files

1. Set `work_backend.type: "git-files"` in `CONFIG.yaml`
2. For each open issue with `artifact:*` labels, create corresponding files in `work/`
3. Close the issues with a note linking to the Git artifact
4. Going forward, agents create files instead of issues

### Hybrid Operation

Using `overrides` in CONFIG.yaml, you can run both backends simultaneously for different artifact types. For example:
- Signals, Missions, Tasks → issues (high human interaction)
- Technical Designs, Governance Exceptions → git files (need code review)
- Decisions → issues (discussion-heavy)
- Asset Registry → git files (persistent documentation)

---

## Templates as Schema Definitions

Regardless of backend, the `_TEMPLATE-*.md` files in `work/` remain in the repository. They serve as:

1. **Schema definitions** — what fields/sections an artifact must contain
2. **Reference documentation** — what each field means and what values are valid
3. **Fallback** — if no issue backend is configured, they're used directly
4. **Issue template source** — GitHub Issue Templates can be generated from them

Templates are **never** tracked in the issue system. They are framework files, governed by the template lifecycle (Rule 11 in AGENTS.md).

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.1 | 2026-03-07 | Clarified Git-only companion artifacts, added human approval cheat sheet, removed issue-only claims for digests/evaluations/outcome reports/fleet reports, linked GitHub implementation guide |
| 1.0 | 2026-03-07 | Initial version — introduced work backend abstraction concept |
