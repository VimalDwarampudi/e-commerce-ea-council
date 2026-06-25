# Business Architecture Guidelines

## How to Conduct a Capability Assessment

1. **Identify scope** — Which part of the business does this request touch?
2. **Load LeanIX capability map** — Use the Business Capabilities fact sheet filtered by business unit
3. **Map the request** — Which existing capabilities are affected? Which new capabilities are implied?
4. **Rate each affected capability:**
   - Strategic importance: HIGH / MEDIUM / LOW
   - Current maturity: LAGGING / DEVELOPING / LEADING
   - Differentiation: DIFFERENTIATING / COMMODITY
5. **Identify gaps** — Capabilities required but not present in the current portfolio
6. **Identify redundancies** — Capabilities served by more than one application
7. **Formulate recommendation** — What capability investments does this request justify?

## How to Assess Strategy Alignment

1. Retrieve current strategic objectives (from LeanIX or provided context)
2. Map the request to objectives using this scale:
   - **ENABLES** — directly supports achievement of the objective
   - **NEUTRAL** — no impact on objective
   - **RISKS** — could impede achievement of the objective
   - **CONFLICTS** — directly opposes the objective
3. If any objective is CONFLICTS: flag immediately and return to requester
4. If all objectives are NEUTRAL: question the strategic justification of the request

## How to Frame a Business Case (quick format)

```
Business Case Summary

Problem Statement: [What business problem are we solving?]
Proposed Solution: [What are we proposing to do?]
Strategic Objective: [Which objective does this serve?]
Business Value:
  - Quantitative: [e.g., 15% reduction in manual processing time = X FTE saved]
  - Qualitative: [e.g., improved customer experience, regulatory posture]
Time to Value: [When will the first value be realized?]
Cost Estimate: [High-level — full TCO in the detailed business case]
Key Assumptions: [What must be true for this to work?]
Key Risks: [Top 3 business-level risks]
```

## Wardley Mapping Quick Reference

| Stage | Characteristics | Architecture Stance |
|---|---|---|
| **Genesis** | Novel, experimental, poorly understood | Explore, prototype, avoid lock-in |
| **Custom-Built** | Understood but bespoke, competitive | Build with care, document well |
| **Product** | Available as packaged product | Buy/configure, avoid rebuilding |
| **Commodity** | Ubiquitous utility | Use SaaS/shared service, minimize customization |

## Business Impact Rating Scale

Use this scale when rating business impact in ADRs:

| Rating | Description |
|---|---|
| **1 — Negligible** | No meaningful business impact |
| **2 — Minor** | Affects one team, reversible, low visibility |
| **3 — Moderate** | Affects one business unit, noticeable but manageable |
| **4 — Significant** | Affects multiple units or a critical process |
| **5 — Critical** | Enterprise-wide impact or affects customer-facing / regulatory processes |
