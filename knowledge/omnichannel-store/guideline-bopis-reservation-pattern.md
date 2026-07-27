---
type: Guideline
title: BOPIS Reservation Pattern
description: Reserve inventory at the moment of online order placement, not at pickup, using a short-TTL soft-hold that auto-releases if pickup doesn't occur within the promised window.
tags: [omnichannel-store, guideline]
timestamp: 2026-07-23T00:00:00Z
---

# BOPIS Reservation Pattern

Reserve inventory at the moment of online order placement, not at pickup, using a short-TTL soft-hold that auto-releases if pickup doesn't occur within the promised window. This balances promise reliability against inventory lockup — a hard, indefinite hold starves in-store sale of the same unit.
