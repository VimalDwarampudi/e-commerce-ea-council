---
type: API
title: tokenization-endpoint
description: PSP-hosted field/tokenization endpoint — the only path by which any checkout surface (digital, POS, call center) may collect payment detail, per the PCI-scope-minimization principle.
tags: [payments, api, placeholder]
timestamp: 2026-07-24T00:00:00Z
status: PLACEHOLDER
---

# tokenization-endpoint

`POST /v1/tokenize` (PSP-hosted, not retailer infrastructure) — returns a token, never touches retailer servers with raw PAN
`POST /v1/charge` — retailer-initiated charge using a token, via the PSP orchestration layer (see the multi-PSP failover policy)

**Note:** the actual endpoint is whichever PSP is integrated (placeholder — e.g. Stripe, Adyen, Braintree); this concept documents the retailer-side integration contract, not the PSP's own API docs.

> **PLACEHOLDER — sample only.** This concept illustrates the shape an asset concept should take once a live source system is connected (see `CLAUDE.md` "Data Sources"). Field names, endpoint paths, and metric values below are representative, not verified against a real system. Replace the body with the actual schema/contract/metric definition and remove `status: PLACEHOLDER` from the frontmatter when done.
