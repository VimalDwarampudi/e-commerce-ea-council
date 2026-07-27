---
type: Example
title: BOPIS Proposal Challenge
description: Reviewing the BOPIS launch proposal (see Omnichannel example).
tags: [red-team, example]
timestamp: 2026-07-23T00:00:00Z
---

# BOPIS Proposal Challenge

Reviewing the BOPIS launch proposal (see Omnichannel example).

Weaknesses identified: (1) the soft-hold TTL design assumes customers pick up within the promised window — no analysis of what fraction historically don't, and whether repeated no-shows create a gaming vector for inventory manipulation. (2) No answer for what happens if a store's local system is offline (per Omnichannel's offline principle) at the exact moment of a BOPIS pickup attempt. (3) Confidence rated MEDIUM, not LOW — the core design is sound, but ship without answering (1) and (2) and the failure mode will surface in the first peak season, not before.
