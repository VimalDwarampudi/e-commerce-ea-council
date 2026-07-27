---
type: Policy
title: PII Classification Required Before Model Training
description: Any dataset used to train a personalization or recommendation model must have its fields classified for PII/sensitivity before training begins.
tags: [data-ai, policy]
timestamp: 2026-07-23T00:00:00Z
mandatory: true
---

# PII Classification Required Before Model Training

**[MANDATORY]**

Any dataset used to train a personalization or recommendation model must have its fields classified for PII/sensitivity before training begins. Training on unclassified data is a mandatory-blocking finding — this is what prevents inadvertent use of, e.g., payment-adjacent data in a marketing model.
