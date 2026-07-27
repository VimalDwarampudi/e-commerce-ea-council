---
type: ReferenceArchitecture
title: Unified Omnichannel Inventory Reference Architecture
description: WMS and store inventory systems publish inventory-changed events to a shared event bus; a unified inventory availability service consumes both streams and serves reads to Order Management, Search & Discovery, and Omnichannel & Store Systems.
tags: [shared, reference-architecture]
timestamp: 2026-07-23T00:00:00Z
---

# Unified Omnichannel Inventory Reference Architecture

WMS and store inventory systems publish inventory-changed events to a shared event bus; a unified inventory availability service consumes both streams and serves reads to Order Management, Search & Discovery, and Omnichannel & Store Systems. Store-local systems maintain a short-TTL cache for offline resilience, reconciled on reconnect. This is the concrete implementation of the One Truth Per Domain of Data principle for inventory specifically, and directly unblocks the BOPIS capability referenced across the Business Strategy, Omnichannel, and Application Architecture worked examples.
