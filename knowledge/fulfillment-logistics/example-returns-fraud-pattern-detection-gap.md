---
type: Example
title: Returns Fraud Pattern Detection Gap
description: Request: reduce return-related shrink.
tags: [fulfillment-logistics, example]
timestamp: 2026-07-23T00:00:00Z
---

# Returns Fraud Pattern Detection Gap

Request: reduce return-related shrink.

Finding: the returns system currently has no visibility into a customer's return history across channels (store returns and online returns are tracked separately) — directly violates the return fraud signal-sharing policy above.

Recommendation: Standard impact. Unify return history under customer identity (same identity model Commerce & Checkout uses for cart) and feed it to Payments' fraud engine. Flag to Risk & Compliance for fraud-threshold policy input.
