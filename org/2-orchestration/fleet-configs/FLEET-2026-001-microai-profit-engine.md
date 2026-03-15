# Fleet Configuration: MISSION-2026-001 microai Profit Engine

> **Template version:** 1.0 | **Last updated:** 2026-03-15  
> **Configuration for OpenClaw fleet deployment focused on rapid profitability.**  
> **Created by:** Orchestration Layer (Mission Lead + Agent Fleet Manager)

---

## Mission

- Mission ID: `MISSION-2026-001`
- Mission brief: [MISSION-2026-001-microai-autonomous-revenue.md](../../../work/missions/MISSION-2026-001-microai-autonomous-revenue.md)
- Status: active

## Orchestration

- Mission Lead: `microai-steering`
- Fleet Manager: `microai-orchestrator`

## Streams

### Stream: Opportunity Discovery and Selection

- Agent pool: `microai-steering + microai-ops`
- Division: Strategy + Revenue Intelligence
- Exclusive: yes

**Working paths:**

- `work/signals/`
- `work/missions/`

**Quality policies:**

- risk-management
- delivery

**Human checkpoints:**

- Trigger: `opportunity_risk_score > 0.7`
- Owner: Human Strategy Owner
- Action: Review whether to proceed

**Success metrics:**

- Qualified opportunities discovered: `>= 3 / week` (measure by signals count)
- Time to selected opportunity: `<= 48 hours` (measure by mission timestamp delta)

### Stream: Offer Build and Monetization

- Agent pool: `microai-builder + microai-quality`
- Division: Autonomous Conversion Optimization
- Exclusive: yes

**Working paths:**

- `work/assets/`
- `work/missions/`
- `process/`

**Quality policies:**

- architecture
- security
- performance

**Human checkpoints:**

- Trigger: `payment_or_legal_risk_detected`
- Owner: Human Legal/Finance Owner
- Action: Approve or stop release

**Success metrics:**

- First paid conversion time: `<= 7 days` (measure from opportunity start to first profit evidence)
- Conversion loop cycle time: `<= 24 hours` (measure by signal-to-release cycle timestamps)

## Dependencies

- Opportunity Discovery and Selection -> Offer Build and Monetization (`blocks`)

## Monitoring

- Quality threshold: `0.8`
- Throughput alert: alert when no deployable output in 24 hours
- Escalation policy: escalate to Strategy + Human Owner when no profit in 7 days

## Profitability and Team Governance Rules (OpenClaw runtime contract)

1. **Profit-first rule:** every mission must define a monetization path before implementation.
2. **7-day pivot rule:** if an active opportunity has no profit evidence within 7 days, terminate it and create a new opportunity signal within the same day.
3. **Underperformer replacement rule:** any AI role with repeated delivery failure, quality failure, or negative ROI for 2 consecutive cycles is decommissioned and replaced with a revised role profile.
4. **Evidence rule:** no claims of success without repository artifacts that show demand signal, shipped offer, and profit evidence.

---

## Changelog

- 1.0 (2026-03-15): Initial mission-specific OpenClaw fleet configuration for profitability objective.
