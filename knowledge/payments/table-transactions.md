---
type: Table
title: transactions
description: Payment transaction ledger. Contains no raw cardholder data — enforces the mandatory no-raw-cardholder-data-at-rest policy by design.
tags: [payments, table, placeholder]
timestamp: 2026-07-24T00:00:00Z
status: PLACEHOLDER
---

# transactions

**Owning system:** Payments service, backed by the PSP's tokenized vault

| Field | Type | Notes |
|---|---|---|
| transaction_id | string, PK | |
| order_id | string, FK -> order-management.orders | |
| payment_token | string | PSP-issued token; never a PAN |
| amount, currency | decimal, string | |
| status | enum(authorized, captured, declined, refunded, chargeback) | |
| fraud_signal_score | decimal | See risk-appetite in Risk & Compliance for threshold governance |
| processed_at | timestamp | |

> **PLACEHOLDER — sample only.** This concept illustrates the shape an asset concept should take once a live source system is connected (see `CLAUDE.md` "Data Sources"). Field names, endpoint paths, and metric values below are representative, not verified against a real system. Replace the body with the actual schema/contract/metric definition and remove `status: PLACEHOLDER` from the frontmatter when done.
