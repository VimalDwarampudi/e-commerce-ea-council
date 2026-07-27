---
type: Principle
title: Minimize PCI Scope Aggressively
description: Every system touching cardholder data expands PCI-DSS audit scope and cost.
tags: [payments, principle]
timestamp: 2026-07-23T00:00:00Z
---

# Minimize PCI Scope Aggressively

Every system touching cardholder data expands PCI-DSS audit scope and cost. Default to tokenization and PSP-hosted fields for any new payment surface (checkout, store POS, call-center order entry) so that raw cardholder data never enters retailer-owned infrastructure.
