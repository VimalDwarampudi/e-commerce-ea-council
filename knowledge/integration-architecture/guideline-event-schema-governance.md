---
type: Guideline
title: Event Schema Governance
description: All events published to the shared event bus must be registered in a schema registry with versioning and backward-compatibility rules.
tags: [integration-architecture, guideline]
timestamp: 2026-07-23T00:00:00Z
---

# Event Schema Governance

All events published to the shared event bus must be registered in a schema registry with versioning and backward-compatibility rules. Breaking schema changes require a deprecation window matching the Catalog domain's taxonomy-change policy.
