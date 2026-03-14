# Compliance Remediation Guides

> **Purpose:** Actionable guides for closing P0-critical compliance gaps identified in the [compliance reference docs](../README.md).

These guides are for **adopters deploying the framework** in a real environment. Each guide addresses a specific gap from the compliance reference documents and provides step-by-step remediation instructions.

## P0-Critical Guides

| Guide | Standard | Gap | Issue |
|-------|----------|-----|-------|
| [SOC 2 Operating Effectiveness Evidence](soc2-operating-effectiveness.md) | SOC 2 Type II | No runtime evidence for Type II audit | [#123](https://github.com/wlfghdr/agentic-enterprise/issues/123) |
| [NIST CSF Runtime Security Tooling](nist-csf-runtime-security-tooling.md) | NIST CSF 2.0 | No SIEM/IDS/IPS/EDR provisioned | [#133](https://github.com/wlfghdr/agentic-enterprise/issues/133) |
| [NIST CSF Network Security Architecture](nist-csf-network-security.md) | NIST CSF 2.0 | No network segmentation/firewall/monitoring | [#134](https://github.com/wlfghdr/agentic-enterprise/issues/134) |
| [EU AI Act Conformity Assessment](eu-ai-act-conformity-assessment.md) | EU AI Act | No conformity assessment procedure | [#129](https://github.com/wlfghdr/agentic-enterprise/issues/129) |
| [EU AI Act CE Marking & EU Database](eu-ai-act-ce-marking.md) | EU AI Act | No CE marking or EU database registration | [#130](https://github.com/wlfghdr/agentic-enterprise/issues/130) |

## How to Use These Guides

1. **Identify your deployment context** — which standards apply to your organization
2. **Follow the remediation steps** — each guide provides concrete actions, templates, and configuration examples
3. **Collect evidence** — use the evidence mapping to feed your audit preparation
4. **Validate** — use the verification checklist at the end of each guide to confirm gap closure
