---
type: API
title: api-gateway-contract
description: The retailer's single external-facing API gateway; every partner, marketplace, and carrier integration must route through this per the mandatory gateway policy.
tags: [integration-architecture, api, placeholder]
timestamp: 2026-07-24T00:00:00Z
status: PLACEHOLDER
---

# api-gateway-contract

**Capabilities:** auth (OAuth2/API key), rate limiting, request/response logging, webhook signature verification.

**Registered integrations (placeholder — populate with actuals):** marketplace channel feeds, carrier tracking webhooks, PSP webhooks.

No integration should exist that bypasses this gateway for direct system access — that's the specific failure mode caught in the Security domain's marketplace-webhook worked example.

> **PLACEHOLDER — sample only.** This concept illustrates the shape an asset concept should take once a live source system is connected (see `CLAUDE.md` "Data Sources"). Field names, endpoint paths, and metric values below are representative, not verified against a real system. Replace the body with the actual schema/contract/metric definition and remove `status: PLACEHOLDER` from the frontmatter when done.
