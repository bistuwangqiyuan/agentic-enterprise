# EU AI Act — CE Marking & EU Database Registration Guide

> **Closes gap:** CE marking (Art. 48) and EU database registration (Art. 49, 71)
> **Regulation:** EU AI Act (Regulation 2024/1689)
> **Severity:** Critical — mandatory prerequisites for EU market entry
> **Related issue:** [#130](https://github.com/wlfghdr/agentic-enterprise/issues/130)
> **Related compliance doc:** [EU AI Act Compliance Reference](../eu-ai-act.md)
> **Companion guide:** [Conformity Assessment](eu-ai-act-conformity-assessment.md) — must be completed first

## 1. Gap Summary

CE marking is the visible declaration that a high-risk AI system conforms with EU AI Act requirements. EU database registration makes the system discoverable to market surveillance authorities and the public. Both are **mandatory legal prerequisites** before placing a high-risk AI system on the EU market or putting it into service.

The framework currently provides governance scaffolding (policies, controls, observability) but does not include guidance on the CE marking process or EU database registration procedure. This guide closes that gap.

## 2. Prerequisites

Before CE marking and registration, the following must be complete:

| Prerequisite | Article | Guide |
|-------------|---------|-------|
| Risk classification (confirm system is high-risk) | Art. 6 | [Conformity Assessment Guide](eu-ai-act-conformity-assessment.md) §2 |
| Conformity assessment completed | Art. 43 | [Conformity Assessment Guide](eu-ai-act-conformity-assessment.md) §3–4 |
| Technical documentation package | Art. 11, Annex IV | [Conformity Assessment Guide](eu-ai-act-conformity-assessment.md) §3c |
| Quality management system | Art. 17 | [Conformity Assessment Guide](eu-ai-act-conformity-assessment.md) §6 |
| Risk management system operational | Art. 9 | [Risk Management Policy](../../../org/4-quality/policies/risk-management.md) |
| Human oversight mechanisms designed | Art. 14 | AGENTS.md Rule 2: "Humans decide, agents recommend" |
| Logging capability verified | Art. 12 | [OTel Contract](../../otel-contract.md) |

## 3. Declaration of Conformity (Art. 47)

The declaration of conformity is the legal document in which the provider states that the AI system meets all applicable requirements. It must be issued **before** CE marking is affixed.

### 3a. Required Content

Per Art. 47 and Annex V, the declaration must contain:

1. **AI system identification** — name, type, version, and any additional unambiguous reference (e.g., serial number, software version hash)
2. **Provider identification** — legal name, registered address, contact details
3. **Sole responsibility statement** — "This declaration of conformity is issued under the sole responsibility of the provider"
4. **Conformity statement** — "The AI system described above is in conformity with Regulation (EU) 2024/1689"
5. **Standards applied** — reference to harmonized standards, common specifications, or other technical specifications used
6. **Notified body details** (if applicable) — name, identification number, certificate reference
7. **Place and date of issue**
8. **Signatory** — name, function, and signature of the person authorized to sign on behalf of the provider

### 3b. Declaration Template

```
═══════════════════════════════════════════════════════════
          EU DECLARATION OF CONFORMITY
    pursuant to Regulation (EU) 2024/1689
         (European Artificial Intelligence Act)
═══════════════════════════════════════════════════════════

1. AI SYSTEM IDENTIFICATION
   Name:           {{AI_SYSTEM_NAME}}
   Type:           {{AI_SYSTEM_TYPE}}
   Version:        {{VERSION}}
   Unique ID:      {{UNIQUE_IDENTIFIER}}

2. PROVIDER
   Legal name:     {{COMPANY_LEGAL_NAME}}
   Address:        {{REGISTERED_ADDRESS}}
   Contact:        {{CONTACT_EMAIL}}

3. EU AUTHORIZED REPRESENTATIVE (if provider outside EU)
   Legal name:     {{EU_REP_NAME}}
   Address:        {{EU_REP_ADDRESS}}

4. RESPONSIBILITY STATEMENT
   This declaration of conformity is issued under the sole
   responsibility of the provider named above.

5. CONFORMITY STATEMENT
   The AI system described above is in conformity with
   Regulation (EU) 2024/1689 of the European Parliament
   and of the Council.

6. STANDARDS AND SPECIFICATIONS APPLIED
   - {{HARMONIZED_STANDARD_1}} (e.g., ISO/IEC 42001:2023)
   - {{HARMONIZED_STANDARD_2}} (e.g., ISO/IEC 27001:2022)
   - {{COMMON_SPECIFICATION_IF_ANY}}

7. CONFORMITY ASSESSMENT
   Type:           Internal (Annex VI) / Third-party (Annex VII)
   Notified body:  {{NAME_AND_NUMBER}} (if applicable)
   Certificate:    {{CERTIFICATE_REFERENCE}} (if applicable)

8. ADDITIONAL INFORMATION
   Risk classification: High-risk (Art. 6, Annex III area {{AREA_NUMBER}})
   Intended purpose:    {{INTENDED_PURPOSE_SUMMARY}}

Signed at {{PLACE}} on {{DATE}}

{{SIGNATORY_NAME}}
{{SIGNATORY_FUNCTION}}
{{SIGNATURE}}

═══════════════════════════════════════════════════════════
```

### 3c. Maintenance Obligations

- **Retention:** Keep for **10 years** after the AI system is placed on the market or put into service
- **Availability:** Must be made available to national competent authorities on request
- **Updates required when:**
  - The AI system undergoes a **substantial modification** (Art. 3(23))
  - Referenced standards are updated
  - Notified body certificate is renewed or changed
- **Language:** Must be available in the official language(s) of each member state where the system is placed on the market

## 4. CE Marking (Art. 48)

### 4a. What CE Marking Means

CE marking indicates that the AI system has undergone the applicable conformity assessment procedure and meets the requirements of the EU AI Act. It is:
- A **legal compliance indicator**, not a quality mark
- The **provider's declaration of responsibility** for conformity
- **Required by law** for high-risk AI systems before EU market entry

### 4b. Physical Products with AI Components

For AI systems embedded in physical products:
- CE marking is affixed **visibly, legibly, and indelibly** to the product
- If affixing to the product is not possible, affix to the packaging or accompanying documentation
- Minimum height: **5mm** (unless the nature of the product makes this impracticable)
- Must follow the general principles of Regulation (EC) No 765/2008 Art. 30

### 4c. Software-Only AI Systems

For standalone software AI systems (the typical case for this framework):

**Digital CE marking** is affixed in one or more of the following locations:

| Location | Implementation | Priority |
|----------|---------------|----------|
| User interface | Visible CE mark on startup, about screen, or settings page | Required (if UI exists) |
| API documentation | CE marking section in API reference docs | Required (if API-based) |
| System documentation | Dedicated section in technical/deployment docs | Required |
| Machine-readable metadata | Structured metadata in system configuration | Recommended |

**Machine-readable implementation:**

```json
{
  "eu_ai_act_compliance": {
    "ce_marking": true,
    "regulation": "Regulation (EU) 2024/1689",
    "provider": "{{COMPANY_LEGAL_NAME}}",
    "ai_system_name": "{{AI_SYSTEM_NAME}}",
    "ai_system_version": "{{VERSION}}",
    "risk_classification": "high-risk",
    "annex_iii_area": "{{AREA_NUMBER}}",
    "conformity_assessment": "internal",
    "declaration_of_conformity_ref": "DoC-{{YEAR}}-{{NUMBER}}",
    "conformity_date": "{{YYYY-MM-DD}}",
    "eu_database_registration_id": "{{REGISTRATION_ID}}",
    "notified_body": null,
    "eu_representative": null
  }
}
```

**CONFIG.yaml integration:**

```yaml
# Add to CONFIG.yaml under a new eu_ai_act section
eu_ai_act:
  risk_classification: high-risk
  annex_iii_area: "{{AREA_NUMBER}}"
  ce_marking:
    enabled: true
    conformity_date: "{{YYYY-MM-DD}}"
    declaration_ref: "DoC-{{YEAR}}-{{NUMBER}}"
  eu_database:
    registration_id: "{{REGISTRATION_ID}}"
    registration_date: "{{YYYY-MM-DD}}"
  eu_representative:
    required: false  # set to true if provider is outside EU
    name: null
    address: null
```

### 4d. What CE Marking Does NOT Mean

- It is not an endorsement by the EU
- It is not a product quality certification
- It does not guarantee the AI system is "safe" in absolute terms
- It means the provider has followed the conformity assessment procedure and taken responsibility for compliance

### 4e. Penalties for Non-Compliance

- **Affixing CE marking without conformity:** Up to €15 million or 3% of worldwide annual turnover
- **Misleading CE marking:** Up to €7.5 million or 1% of worldwide annual turnover
- Member states may impose additional penalties under national law

## 5. EU AI Database Registration (Art. 49, 71)

### 5a. Who Must Register

| Actor | Obligation | Timing |
|-------|-----------|--------|
| **Providers** of high-risk AI systems | Register each system before placing on market | Before market entry |
| **Deployers** who are public authorities (or acting on their behalf) | Register their use of high-risk AI systems | Before putting into service |
| **Providers** of AI systems under Art. 50 (transparency obligations) | Register in a separate section of the database | Before placing on market |

### 5b. Registration Data Requirements (Annex VIII)

The following data must be provided for each high-risk AI system:

**Provider information:**
- Legal name, address, contact details
- Where applicable: name and contact of EU authorized representative
- Trade name(s) used

**AI system information:**
- AI system name and version
- Unique identifier
- Status: on the market / withdrawn / recalled
- Member states where the system is/will be placed on the market
- Risk classification and Annex III area (e.g., "Area 4 — Employment")
- Intended purpose (concise description)

**Conformity information:**
- Conformity assessment type: internal (Annex VI) or third-party (Annex VII)
- Harmonized standards or common specifications applied
- Notified body name and number (if applicable)
- URL for instructions for use
- URL or reference to declaration of conformity

**Operational information:**
- Categories of natural persons and groups likely to be affected
- Whether the system processes special categories of personal data (Art. 9 GDPR)
- Description of the AI system in plain language

### 5c. Registration Process

1. **Access the EU AI database** — managed by the EU AI Office (to be operational before August 2026)
2. **Create provider account** — verify legal entity identity, appoint database administrator
3. **Submit registration** for each high-risk AI system with all Annex VIII data
4. **Receive confirmation** — unique registration number assigned
5. **Include registration number** in system documentation and declaration of conformity
6. **Publication:** Most registration data will be publicly accessible; some fields may be restricted for security reasons

### 5d. Update Obligations

Registration must be updated **without undue delay** when:
- Any registered information changes (e.g., new version, change in intended purpose)
- The AI system undergoes a **substantial modification** — a new registration may be required
- The system is **withdrawn from the market** or **recalled**
- The system is **no longer available** on the EU market
- The declaration of conformity is updated

### 5e. Database Not Yet Operational

As of early 2026, the EU AI database is being established by the EU AI Office. Providers should:
- Prepare all registration data in advance (use the checklist in §5b)
- Monitor the EU AI Office website for database launch announcements
- Plan for registration as part of market entry timeline
- Budget for administrative effort (initial registration + ongoing updates)

## 6. Timeline Relative to Market Entry

```
Month   Action                                          Article
─────   ──────                                          ───────
-12     Begin conformity assessment                     Art. 43
 -9     Engage notified body (if biometric ID system)   Art. 43(1)
 -6     Complete technical documentation package         Art. 11
 -4     Complete quality management system evidence      Art. 17
 -3     Complete conformity assessment                   Art. 43
 -2     Issue declaration of conformity                  Art. 47
 -1     Affix CE marking (digital)                       Art. 48
 -1     Submit EU database registration                  Art. 49
  0     ══ MARKET ENTRY ══
 +0     Post-market monitoring system operational        Art. 72
 +0     Serious incident reporting procedure active      Art. 62
+120    Ongoing: update registration as needed           Art. 49
```

**Key deadline:** High-risk AI system obligations apply from **August 2, 2026**.

## 7. Post-Market Obligations

Once the AI system is on the market, the provider must maintain:

| Obligation | Article | Frequency | Action |
|-----------|---------|-----------|--------|
| Declaration of conformity | Art. 47 | Ongoing (10-year retention) | Keep current, update on substantial modification |
| CE marking | Art. 48 | Ongoing | Ensure visible and accurate in all system interfaces |
| EU database registration | Art. 49 | Ongoing | Update without undue delay on any change |
| Post-market monitoring | Art. 72 | Continuous | Systematic collection and analysis of field data |
| Serious incident reporting | Art. 62 | As incidents occur | Report within 15 days (2 days for widespread incidents) |
| Technical documentation | Art. 11 | Ongoing (10-year retention) | Keep updated, make available to authorities on request |
| Cooperation with authorities | Art. 21 | On request | Provide information, documentation, access |

### Serious Incident Reporting (Art. 62)

A "serious incident" includes death, serious damage to health, property, or environment, or serious and irreversible disruption to critical infrastructure management.

**Reporting timeline:**
- **Initial report:** Within 15 days of becoming aware of the incident
- **Widespread incidents:** Within 2 days (e.g., affecting multiple persons or member states)
- **Report to:** National market surveillance authority of the member state where the incident occurred
- **Follow-up:** Update the report as investigation progresses

## 8. Provider Outside the EU

If the provider is established outside the European Union:

| Requirement | Detail |
|-------------|--------|
| **EU authorized representative** | Must appoint one (Art. 22), established in an EU member state |
| **Representative obligations** | Keep documentation available, provide information to authorities, cooperate with competent authorities, terminate mandate if provider acts contrary to obligations |
| **Registration** | Representative's name and address must appear in EU database registration alongside provider's |
| **Written mandate** | Must be formalized in a written mandate specifying scope and powers |
| **Liability** | Representative may be held liable alongside the provider for non-compliance |

## 9. Framework Artifacts Supporting CE Marking

Existing framework artifacts that provide evidence for CE marking and registration:

| EU AI Act Requirement | Framework Artifact | Path |
|----------------------|-------------------|------|
| Risk management (Art. 9) | Risk Management Policy | [risk-management.md](../../../org/4-quality/policies/risk-management.md) |
| Data governance (Art. 10) | Data Classification Policy | [data-classification.md](../../../org/4-quality/policies/data-classification.md) |
| Logging (Art. 12) | OTel Contract | [otel-contract.md](../../otel-contract.md) |
| Transparency (Art. 13) | Agent instruction hierarchy, OPERATING-MODEL.md | [OPERATING-MODEL.md](../../../OPERATING-MODEL.md) |
| Human oversight (Art. 14) | AGENTS.md Rule 2, PR-based governance | [AGENTS.md](../../../AGENTS.md) |
| Accuracy/robustness (Art. 15) | Quality policies, CI/CD gates | [quality policies](../../../org/4-quality/policies/) |
| QMS (Art. 17) | 19 quality policies, 4-loop process | [process/](../../../process/) |
| Change management | PR-based governance, delivery policy | [delivery.md](../../../org/4-quality/policies/delivery.md) |
| Incident response | Incident Response Policy | [incident-response.md](../../../org/4-quality/policies/incident-response.md) |

## 10. Verification Checklist

### Declaration of Conformity
- [ ] All required content per Art. 47 and Annex V included
- [ ] Signed by authorized person
- [ ] Available in required languages
- [ ] 10-year retention plan established
- [ ] Update procedure documented for substantial modifications

### CE Marking
- [ ] Digital CE marking implemented in user interface (if applicable)
- [ ] CE marking included in API documentation (if applicable)
- [ ] CE marking section in system documentation
- [ ] Machine-readable metadata added to system configuration
- [ ] CE marking references declaration of conformity

### EU Database Registration
- [ ] All Annex VIII data fields prepared
- [ ] Provider account created (when database available)
- [ ] Registration submitted before market entry
- [ ] Unique registration number received and documented
- [ ] Registration number included in system documentation
- [ ] Update procedure established for registration changes

### Post-Market
- [ ] Post-market monitoring system operational (Art. 72)
- [ ] Serious incident reporting procedure established (Art. 62)
- [ ] Cooperation procedure with authorities documented (Art. 21)
- [ ] EU authorized representative appointed (if provider outside EU)
- [ ] Calendar reminder set for periodic registration review

### If Provider Outside EU
- [ ] EU authorized representative appointed (Art. 22)
- [ ] Written mandate formalized
- [ ] Representative details included in all registrations and declarations
