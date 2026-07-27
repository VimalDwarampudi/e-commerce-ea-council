---
type: Principle
title: No New Point-to-Point Integrations Without Justification
description: Every new direct system-to-system integration must justify why it doesn't go through the existing API gateway/event bus.
tags: [integration-architecture, principle]
timestamp: 2026-07-23T00:00:00Z
---

# No New Point-to-Point Integrations Without Justification

Every new direct system-to-system integration must justify why it doesn't go through the existing API gateway/event bus. Point-to-point integration debt is the single largest driver of fragility in retail architectures with dozens of specialty systems (OMS, WMS, PIM, POS, PSP).
