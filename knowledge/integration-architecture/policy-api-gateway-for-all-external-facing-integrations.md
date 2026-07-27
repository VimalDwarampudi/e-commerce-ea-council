---
type: Policy
title: API Gateway for All External-Facing Integrations
description: All partner, marketplace, and third-party carrier integrations must route through the API gateway (rate limiting, auth, monitoring), never direct system access.
tags: [integration-architecture, policy]
timestamp: 2026-07-23T00:00:00Z
mandatory: true
---

# API Gateway for All External-Facing Integrations

**[MANDATORY]**

All partner, marketplace, and third-party carrier integrations must route through the API gateway (rate limiting, auth, monitoring), never direct system access. This is mandatory because direct external access to internal systems is both a Security exposure and an operational blind spot.
