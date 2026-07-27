---
type: Example
title: Marketplace Integration Threat Model
description: Request: threat model for the new marketplace channel integration (see Catalog & Product example).
tags: [security, example]
timestamp: 2026-07-23T00:00:00Z
---

# Marketplace Integration Threat Model

Request: threat model for the new marketplace channel integration (see Catalog & Product example).

Findings: marketplace webhook endpoint initially proposed with no signature verification — Spoofing/Tampering risk, HIGH severity.

Veto Decision: VETO ISSUED pending signature verification implementation — this violates the external API authentication policy above. Path to lift veto: implement HMAC signature verification on all inbound marketplace webhooks before go-live.
