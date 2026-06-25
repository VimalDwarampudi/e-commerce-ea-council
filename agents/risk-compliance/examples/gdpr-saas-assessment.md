# Example: Risk & Compliance Assessment — New SaaS HR Platform (SuccessFactors)

## Input (Request Summary)

> Council has proposed adopting SAP SuccessFactors Employee Central as the core HR platform, migrating employee data from legacy on-premises PeopleOne.

## Output (Risk Management & Compliance Assessment)

## Risk Management & Compliance Assessment

### Regulatory Applicability
| Regulation | Applicable? | Reason |
|---|---|---|
| **GDPR** | ✅ YES | Processing EU employee personal data including special categories (sick leave, disability accommodations) |
| **NIS2** | REVIEW | If the organisation is classified as Important or Essential Entity under NIS2, HR platform change requires supply chain risk assessment of SAP |
| **ISO 27001** | ✅ YES | SAP as a critical supplier must meet information security requirements |
| **Local employment law** | ✅ YES | Netherlands: Works Council (Ondernemingsraad) must be consulted before implementing employee monitoring capabilities |
| **DORA** | ❌ N/A | Not applicable — not a financial sector ICT system |

### Compliance Findings

| Regulation | Requirement | Status | Risk Level | Action Required |
|---|---|---|---|---|
| GDPR Art. 28 | Data Processing Agreement with SAP | CONDITIONAL | HIGH | DPA must be in place before data transfer. SAP standard DPA available — review and execute. |
| GDPR Art. 46 | Data transfer mechanism (if SAP processes outside EEA) | CONDITIONAL | HIGH | Confirm SAP SuccessFactors data centre location. EU data centre (Frankfurt/Amsterdam) required or SCCs needed. |
| GDPR Art. 25 | Privacy by Design — migrate minimum necessary data | FAIL | MEDIUM | Data migration must include minimization review. Do not migrate all Siebel/PeopleOne fields — map required fields only. |
| GDPR Art. 9 | Special category data (health-related absence records) | CONDITIONAL | HIGH | Identify special category fields. Explicit processing basis required for health data. |
| GDPR Art. 17 | Right to erasure — data deletion capability | CONDITIONAL | MEDIUM | Confirm SuccessFactors supports employee record deletion. Test deletion request process before go-live. |
| Netherlands WOR Art. 27 | Works Council approval for employee monitoring | **ACTION REQUIRED** | HIGH | Works Council must be informed and consulted before deploying performance management or monitoring capabilities in SuccessFactors. |
| ISO 27001 | Supplier security assessment | FAIL | MEDIUM | SAP vendor risk assessment not yet completed (RC-POL-003). SAP holds ISO 27001 and SOC 2 — obtain current certificates. |

### Risk Assessment

| Risk | Probability | Impact | Rating | Mitigation |
|---|---|---|---|---|
| Personal data transferred to SAP without DPA | LOW (SAP standard DPA exists; just needs signing) | HIGH | **HIGH** | Execute DPA before data transfer |
| Employee special category data (health) processed without explicit basis | MEDIUM | HIGH | **HIGH** | Map all special category fields; confirm legal basis; document in DPIA |
| Data migration includes excessive historical fields (minimization breach) | HIGH | MEDIUM | **HIGH** | Conduct data mapping session; define migration scope explicitly |
| Works Council not consulted before deploying performance features | MEDIUM | HIGH | **HIGH** | Initiate WOR Art. 27 consultation process immediately |
| SAP stores data outside EU without adequate transfer mechanism | LOW (SAP has EU data centres) | HIGH | MEDIUM | Confirm EU data centre in DPA/order confirmation |
| Deleted employee data not actually purged from SAP | MEDIUM | MEDIUM | MEDIUM | Test deletion end-to-end in UAT; verify in post-migration audit |

### Risk Register Impact
**New risks to create in ServiceNow GRC:**
1. "GDPR DPA not executed before SuccessFactors data migration" — HIGH — Owner: DPO — Review: 30 days
2. "Special category data processing basis not established" — HIGH — Owner: DPO + HR Director — Review: 60 days
3. "Works Council consultation not initiated for HR system change" — HIGH — Owner: HR Director — Review: 30 days
4. "SuccessFactors data deletion capability unconfirmed" — MEDIUM — Owner: IT Security — Review: UAT milestone

### Escalation Requirement
**ESCALATION REQUIRED** — Works Council (Ondernemingsraad) requirement.

The Netherlands Works Council Act (WOR) Article 27 requires Works Council approval before implementing systems that monitor employee performance or work patterns. SAP SuccessFactors includes Performance & Goals and time tracking capabilities. This is a legal obligation — not an option. The DPO and HR Director must initiate WOR consultation before implementation begins.

The EA Council cannot approve deployment of performance management features without Works Council approval. Core HR (Employee Central only, no performance/monitoring features) may proceed in parallel.

### Conditions for Compliance Endorsement
1. ✅ SAP DPA executed before any data is migrated to SuccessFactors
2. ✅ DPIA completed for the migration (RC-POL-002 mandatory trigger)
3. ✅ Data migration scope limited to required fields only (data minimization documented)
4. ✅ Special category fields (health/absence data) mapped; processing basis documented
5. ✅ Works Council consultation initiated (performance features blocked until approval)
6. ✅ SAP security certificates (ISO 27001, SOC 2) obtained and filed (RC-POL-003)
7. ✅ Deletion process tested in UAT

## Key Points Illustrated
- Every applicable regulation identified with reason
- Works Council requirement surfaced — legal obligation that would have been missed without this lens
- Risk table with explicit probability × impact = rating
- ServiceNow GRC risk records to create are listed with owners
- Escalation is targeted: not "escalate everything" — escalate the specific legal obligation
- Conditions for endorsement are concrete and measurable
