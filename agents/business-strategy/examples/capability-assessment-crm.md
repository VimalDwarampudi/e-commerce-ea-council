# Example: Business Architecture Assessment — CRM Platform Replacement

## Input (Request Summary)

> "We want to replace our legacy CRM (Siebel) with Dynamics 365 Sales to improve customer engagement capabilities and reduce maintenance costs."

## Output (Business Architecture Assessment)

## Business Architecture Assessment

### Strategic Alignment
This request directly enables Strategic Objective SO-2026-03: "Improve customer engagement through digital channels." Dynamics 365 is on the tech radar as ADOPT and aligns with the Microsoft-first platform strategy.

The replacement also supports SO-2026-07: "Reduce legacy footprint by 30% by 2027" — Siebel is in Phase Out lifecycle (since 2024) and currently the largest legacy maintenance cost in the Sales capability area.

**Alignment rating: ENABLES** (two strategic objectives supported)

### Capability Impact
**Affected capabilities (from LeanIX):**
- **Customer Relationship Management** — PRIMARY. Currently served by Siebel (Business Fit: 2/5, declining). Dynamics 365 expected Business Fit: 4/5.
- **Sales Pipeline Management** — directly linked. Siebel pipeline module underused; teams use spreadsheets as workaround.
- **Customer Analytics** — secondary benefit. Dynamics 365 integrates with Power BI natively; Siebel requires custom reporting.

**Redundancy check:** No other Active application serves CRM capability. However, the Marketing team uses HubSpot for campaign management — confirm scope boundary between CRM and marketing automation to avoid future overlap.

**Capability gap identified:** "Customer 360 View" — neither Siebel nor the current proposal explicitly addresses a unified customer view across Sales, Service, and Marketing. Flag as a design requirement for the implementation.

### Value Stream Impact
**Value stream: Lead-to-Cash**
- Steps affected: Lead Qualification → Opportunity Management → Quote → Order
- Current bottleneck: manual data entry between Siebel and SAP (order creation). Dynamics 365 offers a pre-built SAP integration connector — potential to eliminate this bottleneck.
- Expected improvement: 20–30% reduction in sales cycle admin time based on vendor benchmark data. Validate during PoC.

### Business Risk
1. **User adoption risk (MEDIUM):** Sales teams have used Siebel for 12+ years. Change management and training investment is critical — not optional.
2. **Data migration risk (MEDIUM):** 8 years of customer data in Siebel. Data quality issues are known but unquantified. Recommend data quality assessment before migration design.
3. **Scope creep risk (MEDIUM):** Dynamics 365 platform is broad. Without clear scope boundaries, the project could expand into Service, Marketing, and Field Service modules before CRM is stable.

### Recommendation
**Proceed with Dynamics 365 as the CRM platform replacement.** This is strategically aligned, addresses a known capability gap, and retires a legacy system. However, three conditions must be met:

1. Define clear scope: Sales CRM only in Phase 1. Do not bundle Marketing or Service modules.
2. Conduct a customer data quality assessment before migration planning.
3. Allocate a dedicated change management and training budget (not absorbed into IT budget).

### Dependencies on Peer Domains
- **Application Architecture:** Validate Siebel decommission timeline; confirm no other applications depend on Siebel data exports.
- **Integration Architecture:** Design SAP integration; assess HubSpot/Marketing data flow boundary.
- **Data & AI:** Customer data migration requires classification and DPIA review (personal data).

## Key Points Illustrated
- Strategic alignment scored explicitly against named objectives
- Capability redundancy check performed (HubSpot flagged)
- Capability gap identified proactively (Customer 360)
- Value stream impact quantified where possible
- Risks are business-level, not technical
- Conditions for approval clearly stated
- Dependencies on peer domains identified — not answered for them
