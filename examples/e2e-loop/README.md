# End-to-End Loop Example

This folder demonstrates a complete lifecycle through the Agentic Enterprise operating model — from initial observation to shipped release and back to new observations. It also serves as a **validation test fixture**: every work artifact conforms to the framework's templates and passes the CI validation scripts.

## The Story

A customer-experience agent detects that 34% of new customers abandon onboarding at Step 3. This observation flows through the operating model and results in a fix that reduces drop-off to 16%.

## Directory Structure

```
e2e-loop/
├── README.md                 ← You are here
├── work/
│   ├── signals/
│   │   ├── 2026-03-01-onboarding-step3-dropoff.md          ← Discover (original signal)
│   │   ├── 2026-03-15-mobile-onboarding-dropoff.md         ← Discover (consequential — from retro)
│   │   └── 2026-03-20-funnel-alerting-gap.md               ← Discover (consequential — from retro)
│   ├── missions/
│   │   ├── MISSION-2026-008-onboarding-step3/
│   │   │   ├── BRIEF.md                                     ← Decide (completed)
│   │   │   ├── technical-design.md                          ← Design
│   │   │   └── STATUS.md                                    ← Track (mission progress log)
│   │   └── MISSION-2026-009-mobile-onboarding/
│   │       └── BRIEF.md                                     ← Decide (proposed — human-to-decide)
│   ├── decisions/
│   │   └── DR-2026-008-simplify-over-redesign.md            ← Decide
│   ├── releases/
│   │   └── 2026-03-18-onboarding-step3-release-contract.md  ← Ship
│   └── retrospectives/
│       └── 2026-03-20-onboarding-step3-regression.md        ← Operate
├── work-items.md             ← Build (illustrative task tracking)
└── example-pr.md             ← Ship (illustrative PR pattern)
```

## Reading Order

| # | File | Loop Stage | What It Shows |
|---|------|-----------|--------------|
| 1 | [Signal](work/signals/2026-03-01-onboarding-step3-dropoff.md) | Discover | An observation filed as a structured signal |
| 2 | [Mission Brief](work/missions/MISSION-2026-008-onboarding-step3/BRIEF.md) | Decide | The signal converted to scoped work with clear outcomes |
| 3 | [Decision Record](work/decisions/DR-2026-008-simplify-over-redesign.md) | Decide | Why progressive disclosure was chosen over alternatives |
| 4 | [Technical Design](work/missions/MISSION-2026-008-onboarding-step3/technical-design.md) | Design | Full technical design with observability plan |
| 5 | [Work Items](work-items.md) | Build | Tasks decomposed and tracked through execution |
| 6 | [Mission Status](work/missions/MISSION-2026-008-onboarding-step3/STATUS.md) | Build | Progress tracking with fleet performance metrics |
| 7 | [Example PR](example-pr.md) | Ship | A governed pull request with quality gates |
| 8 | [Release Contract](work/releases/2026-03-18-onboarding-step3-release-contract.md) | Ship | Release with rollout plan, rollback plan, and outcome measurement |
| 9 | [Retrospective](work/retrospectives/2026-03-20-onboarding-step3-regression.md) | Operate | Postmortem on the original regression + lessons learned |
| 10 | [Mobile Signal](work/signals/2026-03-15-mobile-onboarding-dropoff.md) | Discover | Consequential signal filed from retrospective follow-up |
| 11 | [Alerting Gap Signal](work/signals/2026-03-20-funnel-alerting-gap.md) | Discover | Systemic observation filed from retrospective analysis |
| 12 | [Mobile Mission](work/missions/MISSION-2026-009-mobile-onboarding/BRIEF.md) | Decide | New mission in `proposed` state — awaiting human approval |

## The Loop

```
Signal          →  "We see a 34% drop-off"
Decision        →  "Simplify via progressive disclosure, not full redesign"
Mission         →  "We will fix it by simplifying Step 3"
Technical Design →  "Here's the implementation plan with observability"
Work Items      →  "Here are the 8 tasks to get it done"
Status Tracking →  "Progress log with fleet metrics"
PR              →  "Here is the governed code change"
Release         →  "Drop-off reduced to 16%. All targets met."
Retrospective   →  "Why did the regression happen? How do we prevent it?"
                →  New signals filed → next missions begin (nothing stalls)
```

## Work Continuity (Nothing Stalls)

This example also demonstrates that **every work item has a clear next actor**:

| Artifact | State | Next Actor | Why It's Not Stalled |
|----------|-------|-----------|---------------------|
| Original signal | Proceed → mission created | — (terminal) | Resolved by MISSION-2026-008 |
| MISSION-2026-008 | completed | — (terminal) | All targets met, release deployed |
| Mobile signal | Proceed → mission proposed | Human (VP Product) | Awaiting sponsor approval on MISSION-2026-009 |
| Alerting gap signal | Monitor (follow-up: 2026-04-15) | Agent (next cycle) | SRE team assessing scope; will re-evaluate |
| MISSION-2026-009 | proposed | Human (VP Product) | Clearly in human-to-decide state |
| Retro follow-ups | 2 done, 2 open (assigned) | Human (VP Product) | Open items have owners and due dates |

The validation script (`validate_work_artifacts.py`) enforces this by checking:
1. Every signal has a disposition checked (no undecided signals)
2. Signals with "Proceed" are referenced by at least one mission brief
3. Signals listed in retrospective "Signals Filed" sections exist as actual files
4. Active missions have STATUS.md for progress tracking

## Using This as a Validation Test Fixture

Every work artifact in `work/` conforms to the framework's template schemas. You can run the validation scripts against this directory to verify they work correctly:

```bash
# Validate signals, mission briefs, and release contracts (schema validation)
python3 scripts/validate_schema.py --root examples/e2e-loop

# Validate decision records, retrospectives, and technical designs
python3 scripts/validate_work_artifacts.py --root examples/e2e-loop

# Run both to verify the full artifact suite
python3 scripts/validate_schema.py --root examples/e2e-loop && \
python3 scripts/validate_work_artifacts.py --root examples/e2e-loop
```

Expected output: all artifacts pass validation — including work continuity checks (no stalled work).

This makes the e2e-loop example a regression test: if a template schema change breaks existing artifacts, the example will fail first.

## Key Takeaways

1. **Every piece of work traces back to an observation.** Nothing is done "just because."
2. **Scope is explicit.** The mission says what's in and out of scope before work begins.
3. **Decisions are documented.** The decision record captures alternatives considered and why they were rejected.
4. **Observability is designed, not bolted on.** The technical design includes a full observability plan before implementation begins.
5. **PRs are governed.** CODEOWNERS defines reviewers. Quality policies are checked. CI enforces standards.
6. **Outcomes are measured.** The release records whether targets were actually met.
7. **Failures are analyzed.** The retrospective explains the original regression and prevents recurrence.
8. **The loop never stops.** Every release generates new observations that feed back into the system.
9. **Nothing stalls silently.** Every work item is either in a terminal state, picked up by an agent cycle, or clearly waiting for a human decision. The validation script enforces this.
