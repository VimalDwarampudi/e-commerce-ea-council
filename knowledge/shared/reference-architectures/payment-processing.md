---
type: ReferenceArchitecture
title: PCI-Minimized Payment Processing Reference Architecture
description: All payment surfaces (digital checkout, store POS, call-center order entry) use PSP-hosted tokenization fields; no retailer-owned system receives raw cardholder data.
tags: [shared, reference-architecture]
timestamp: 2026-07-23T00:00:00Z
---

# PCI-Minimized Payment Processing Reference Architecture

All payment surfaces (digital checkout, store POS, call-center order entry) use PSP-hosted tokenization fields; no retailer-owned system receives raw cardholder data. Multi-PSP orchestration layer provides failover for peak events. Store POS traffic is network-segmented per Security's mandatory policy. This is the concrete implementation shared by the Payments, Security, and Omnichannel domains' cardholder-data and network-segmentation policies.
