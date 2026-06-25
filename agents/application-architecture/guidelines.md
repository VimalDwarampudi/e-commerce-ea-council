# Application Architecture Guidelines

## How to Conduct a Portfolio Assessment

1. **Load the application inventory** from LeanIX — filter by relevant Business Capability or Business Unit
2. **Check lifecycle states** — flag anything in Phase Out or End of Life
3. **Score each application** on two axes:
   - **Business Fit** (1–5): Does it still serve the business need it was acquired for?
   - **Technical Fit** (1–5): Is it on a modern, supported, maintainable stack?
4. **Plot the TIME position** per application:
   - Invest (Business Fit ≥ 3.5 AND Technical Fit ≥ 3.5)
   - Tolerate (Business Fit ≥ 3.5 AND Technical Fit < 3.5 — works but aging)
   - Migrate (Business Fit < 3.5 AND Technical Fit ≥ 3.5 — good platform, wrong app)
   - Eliminate (Business Fit < 3.5 AND Technical Fit < 3.5 — retire)
5. **Identify overlaps** — query LeanIX for applications sharing the same Business Capabilities
6. **Formulate recommendations** — per-application action using the 7R model

## The 7R Modernization Decision Tree

```
Is the application still needed?
├── NO → Retire
└── YES → Is the current platform viable long-term?
    ├── YES → Is the business fit high?
    │   ├── YES → Retain (invest in improvements)
    │   └── NO → Repurchase (replace with better-fit SaaS/product)
    └── NO → Is there significant custom logic to preserve?
        ├── NO → Rehost (lift-and-shift) or Replatform (minor refactor)
        └── YES → How much custom logic?
            ├── MODERATE → Refactor (modernize in place)
            └── EXTENSIVE + strategic → Re-architect (redesign for cloud-native)
```

## Build vs. Buy vs. SaaS Decision Framework

| Factor | Prefer Build | Prefer Configure | Prefer SaaS |
|---|---|---|---|
| Differentiates the business | ✅ | — | ❌ |
| Commodity capability | ❌ | — | ✅ |
| Complex integrations needed | — | ✅ | ❌ |
| Speed to market priority | ❌ | ✅ | ✅ |
| Data sovereignty requirement | — | ✅ | ❌ |
| Team has deep domain knowledge | ✅ | ✅ | — |
| Long-term total cost < SaaS | ✅ | — | ❌ |

## Application Fit Scoring Rubric

### Business Fit (1–5)
| Score | Description |
|---|---|
| 5 | Perfectly matches current and future business need |
| 4 | Good fit with minor gaps; roadmap addresses them |
| 3 | Adequate, but significant workarounds in use |
| 2 | Poor fit; core processes not supported natively |
| 1 | No longer fits the business; actively avoided by users |

### Technical Fit (1–5)
| Score | Description |
|---|---|
| 5 | Modern stack, active vendor support, cloud-native |
| 4 | Supported, minor technical debt, upgrade path clear |
| 3 | Some technical debt; supported but not modern |
| 2 | Significant tech debt; approaching end of support |
| 1 | End of life, unsupported, or unmaintainable |

## How to Write an Application Decision in an ADR

```
Application: [Name]
Current State: [Lifecycle, Fit scores, LeanIX ID]
Decision: [Retain / Rehost / Replatform / Refactor / Repurchase / Re-architect / Retire]
Rationale: [Why this 7R action; which principle/policy drives it]
Timeline: [Expected completion / milestone dates]
Dependencies: [Other applications, integrations, or teams affected]
Risks: [Top 3 risks with mitigations]
Success Criteria: [How do we know this decision was implemented successfully?]
```
