---
type: Policy
title: No Custom Cardholder Data Handling in Checkout UI
description: The checkout flow's own application code must never receive, log, or store raw cardholder data.
tags: [commerce-checkout, policy]
timestamp: 2026-07-23T00:00:00Z
mandatory: true
---

# No Custom Cardholder Data Handling in Checkout UI

**[MANDATORY]**

The checkout flow's own application code must never receive, log, or store raw cardholder data. All payment collection must go through the PCI-scoped mechanism defined by Payments Architecture (iframe/tokenization). This eliminates checkout services from PCI-DSS scope — violating it brings the entire checkout platform into scope.
