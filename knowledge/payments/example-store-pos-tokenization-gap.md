---
type: Example
title: Store POS Tokenization Gap
description: Request: assess PCI exposure of the in-store POS payment flow.
tags: [payments, example]
timestamp: 2026-07-23T00:00:00Z
---

# Store POS Tokenization Gap

Request: assess PCI exposure of the in-store POS payment flow.

Finding: POS terminals are P2PE-certified (good), but the store network segment carrying terminal traffic is flat with the general store LAN, not segmented.

Security Architecture involvement: mandatory — this is a network segmentation finding with veto-level severity if unmitigated, since it expands PCI scope to the entire store network. Recommendation: segment POS traffic on its own VLAN with strict firewall rules before this is considered resolved.
