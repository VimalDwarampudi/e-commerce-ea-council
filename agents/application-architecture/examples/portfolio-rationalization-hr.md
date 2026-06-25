# Example: Application Architecture Assessment — HR Platform Rationalization

## Input (Request Summary)

> "We want to adopt SAP SuccessFactors for HR. Currently we run a mix of legacy HR systems. What is the portfolio impact?"

## Output (Application Architecture Assessment)

## Application Architecture Assessment

### Portfolio Context
LeanIX query returned 4 applications in the HR domain:

| Application | Lifecycle | Business Fit | Technical Fit | TIME Position |
|---|---|---|---|---|
| HR-Legacy-PeopleOne | End of Life | 1/5 | 1/5 | **Eliminate** |
| HR-PayrollSystem-ADP | Active | 4/5 | 3/5 | **Tolerate** |
| HR-Recruitment-Greenhouse | Active | 4/5 | 4/5 | **Invest** |
| HR-Learning-SuccessFactors-LMS | Active | 3/5 | 4/5 | **Invest** |

Two additional applications were found in LeanIX linked to HR Business Capabilities with no assigned owner — flagged as governance gap: `HR-Timesheet-LegacyTool` and `HR-ExpensePortal-v1`. These require investigation before any HR platform decision is finalized.

### Proposal Evaluation
SAP SuccessFactors (Employee Central) covers: Core HR, Payroll, Performance & Goals, Succession, Learning, Recruiting.

**Overlap analysis:**
- **HR-Legacy-PeopleOne** → Full overlap. Immediate candidate for **Retire**.
- **HR-PayrollSystem-ADP** → Partial overlap. SuccessFactors Payroll available but ADP integration is also viable. Decision required: replace or integrate? (see dependency note below).
- **HR-Recruitment-Greenhouse** → Full overlap with SuccessFactors Recruiting. However, Greenhouse has higher Business Fit (4/5) and strong user adoption. Recommend **Retain Greenhouse** in Phase 1; revisit in 12 months.
- **HR-Learning-SuccessFactors-LMS** → Already SuccessFactors. Migrate to same tenant as Employee Central — not a new application.

### Tech Radar Position
| Technology | Radar Position | Notes |
|---|---|---|
| SAP SuccessFactors | **ADOPT** | Enterprise HCM standard |
| ADP Payroll (SaaS) | **TRIAL** | Acceptable for payroll if SuccessFactors Payroll not chosen |
| Greenhouse Recruiting | **TRIAL** | Acceptable to retain; review against SuccessFactors Recruiting |
| HR-Legacy-PeopleOne stack | **HOLD** | End of life — no new investment |

### Build / Buy / SaaS Recommendation
**SaaS (SuccessFactors)** — clear choice. HR is a commodity capability (Wardley: Product/Commodity). No competitive differentiation from custom HR software. Minimize customization; configure to standard SuccessFactors best practices.

### Rationalization Impact
This proposal creates an opportunity to retire HR-Legacy-PeopleOne and potentially consolidate ADP Payroll. Net portfolio reduction of 1–2 applications after full rollout. This is positive — supports AA-POL-003 (Redundancy Check) and EP-007 (Reuse Before Build).

**Remaining risk:** 2 unowned applications (`HR-Timesheet-LegacyTool`, `HR-ExpensePortal-v1`) must be investigated. If they depend on PeopleOne data exports, decommission of PeopleOne must be sequenced after they are addressed.

### Recommendation
1. **Retire** HR-Legacy-PeopleOne — no new investment; plan decommission within 18 months of SuccessFactors go-live.
2. **Adopt** SuccessFactors Employee Central as core HR platform.
3. **Retain** Greenhouse Recruiting for Phase 1; evaluate SuccessFactors Recruiting in Phase 2 review.
4. **Decide** on ADP Payroll vs SuccessFactors Payroll — business case comparison needed (out of scope for this assessment; raise as separate ADR).
5. **Investigate** 2 unowned applications before finalizing decommission sequence.

### Dependencies on Peer Domains
- **Integration Architecture:** Design SuccessFactors ↔ SAP S/4HANA (employee master data) integration; ADP Payroll interface if retained.
- **Data & AI:** Employee personal data migration — DPIA required (GDPR special category: employment data).
- **Business Architecture:** Confirm Greenhouse retention aligns with Talent Acquisition capability strategy.

## Key Points Illustrated
- LeanIX portfolio query performed; all HR applications surfaced and scored
- TIME model applied explicitly per application
- Tech radar checked for every technology
- Unowned applications flagged as governance gap (AA-POL-007)
- Redundancy check performed (AA-POL-003)
- Build/Buy/SaaS justified via Wardley positioning
- Phase 1 vs Phase 2 scope boundary recommended to avoid big-bang risk
