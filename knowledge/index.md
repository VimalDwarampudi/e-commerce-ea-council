# Retail EA Council — Knowledge Bundle Index (OKF)

This is the OKF bundle root. Read this file first (per `SKILL.md`), then drill into the domain
sub-bundle relevant to the question at hand.

**Two layers of content live in each domain folder:**
- **Governance layer** — `Principle`, `Policy`, `Guideline`, `Example` concepts. Always present.
- **Asset layer** — `Table`, `API`, `Metric` concepts describing the domain's actual system assets
  (schemas, contracts, operational metrics). Currently **sample placeholders** (`status: PLACEHOLDER` in
  frontmatter) — not verified against real systems yet. Present in 12 of the 15 domains; Business Strategy,
  Application Architecture, and Red Team don't own concrete system assets in the same way, so they don't
  have one. Replace placeholders with real schemas/contracts/metrics as source systems get connected — see
  `CLAUDE.md` "Data Sources."

## Domain sub-bundles

| Domain | Path | Concepts |
|---|---|---|
| Business Strategy & Capability Alignment | `business-strategy/index.md` | 6 |
| Catalog & Product Information Architecture | `catalog-product/index.md` | 6 |
| Search & Discovery Architecture | `search-discovery/index.md` | 6 |
| Commerce & Checkout Architecture | `commerce-checkout/index.md` | 6 |
| Order Management Architecture | `order-management/index.md` | 6 |
| Payments Architecture | `payments/index.md` | 6 |
| Omnichannel & Store Systems Architecture | `omnichannel-store/index.md` | 6 |
| Fulfillment & Logistics Architecture | `fulfillment-logistics/index.md` | 6 |
| Application Architecture | `application-architecture/index.md` | 6 |
| Integration Architecture | `integration-architecture/index.md` | 6 |
| Technology & Infrastructure | `technology-infrastructure/index.md` | 6 |
| Data & AI Architecture | `data-ai/index.md` | 6 |
| Security Architecture | `security/index.md` | 7 |
| Risk Management & Compliance | `risk-compliance/index.md` | 6 |
| Red Team | `red-team/index.md` | 4 |

## Enterprise-wide (shared)

| Content | Path |
|---|---|
| 12 enterprise architecture principles | `shared/index.md` |
| Technology radar (ADOPT/TRIAL/ASSESS/HOLD) | `shared/tech-radar/index.md` |
| Glossary | `shared/glossary.md` |
| Standards (ADR template, naming, documentation) | `shared/standards/` |
| Reference architectures | `shared/reference-architectures/` |

See `log.md` for the chronological change history of this bundle.
