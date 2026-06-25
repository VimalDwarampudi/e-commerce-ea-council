# OT Security Baseline — Manufacturing Architecture Agent

## Purpose
This document defines the minimum security baseline for OT environments, following IEC 62443 and NIST SP 800-82. Use this as the reference when assessing OT security posture.

## Network Security Baseline

### Mandatory Controls (all OT environments)
- [ ] OT networks physically or logically separated from corporate IT (VLAN minimum; separate switches preferred)
- [ ] All IT↔OT traffic passes through Level 3.5 DMZ
- [ ] Firewall default-deny between all OT zones; explicit allow rules only
- [ ] OT network topology documented and current (verified quarterly)
- [ ] No direct internet access from Control Zone (Level 1–2)
- [ ] DNS for OT networks: local DNS only; no resolution to public internet from Control Zone
- [ ] NTP: OT systems synchronise to local NTP server (not internet NTP)
- [ ] Wireless networks: prohibited in Control Zone; Supervisory Zone requires WPA3-Enterprise with separate SSID and VLAN

### Enhanced Controls (critical processes; SL2+ target)
- [ ] IDS/IPS monitoring all DMZ traffic — OT-specific signatures (Claroty / Dragos / Nozomi)
- [ ] Network traffic baseline established; anomaly detection active
- [ ] Unidirectional gateway (data diode) for Levels 0–2 → IT where bidirectional flow is not needed
- [ ] OT network asset discovery: automated passive discovery running continuously
- [ ] Historian replicated to DMZ via read-only interface (no write path from IT to historian)

---

## Identity & Access Baseline

### Mandatory Controls
- [ ] Separate OT accounts for all OT systems — no SSO with corporate AD into Control or Supervisory zones
- [ ] Privileged Access Management (PAM) for OT administrator accounts
- [ ] No shared accounts on OT systems (one account per person)
- [ ] Default vendor accounts disabled or passwords changed before deployment
- [ ] Role-based access: operators (read/acknowledge alarms), engineers (read/write process parameters), administrators (configuration changes)
- [ ] Remote access: OT jump server only (OT-POL-004); MFA mandatory; session recording

### Enhanced Controls
- [ ] Privileged session management with dual-control for safety-critical parameter changes (requires two authorised engineers)
- [ ] Quarterly review of OT account list — remove leavers and contractors
- [ ] Vendor access: just-in-time provisioning; zero standing access

---

## Endpoint Security Baseline

### Mandatory Controls (Levels 2–3, industrial PCs and servers)
- [ ] Application whitelisting (Tripwire, McAfee Application Control) — not traditional AV
- [ ] USB ports disabled or controlled (no unknown media)
- [ ] Only OT-necessary software installed — no email, web browsing, Office on control systems
- [ ] Local firewall enabled with OT-appropriate rules
- [ ] Operating system hardened to CIS benchmark (adapted for OT — some IT controls do not apply)
- [ ] Patch management: planned maintenance window schedule; never during production

### Mandatory Controls (Level 1 — PLCs, RTUs)
- [ ] Firmware version documented in CMDB
- [ ] Physical key switch: PLCs in RUN mode during production (prevents unauthorised programming)
- [ ] No programming ports (RS-232, USB) accessible without physical presence
- [ ] Vendor default passwords changed during commissioning

---

## Patch & Vulnerability Management

### Approach for OT (different from IT)
OT patching is constrained by:
1. **Maintenance windows:** Patches can only be applied during scheduled downtime (typically annual, quarterly for critical)
2. **Vendor qualification:** Patches for validated systems must be evaluated for regulatory re-validation impact
3. **Vendor support:** Patch must be approved/tested by the OT system vendor before application
4. **Rollback:** Rollback procedure must be tested before patching production

### Compensating Controls for Unpatched Systems
When patching is not possible (legacy systems, between maintenance windows):
- Network isolation: ensure the system is not reachable from IT or internet
- Passive monitoring: IDS watching for exploitation attempts
- Application whitelisting: prevent unauthorised code execution even if vulnerability is exploited
- Physical access controls: prevent local tampering
- Document formally in risk register with compensating controls and review date

---

## Incident Response for OT

### OT-Specific Considerations
OT incident response differs from IT because:
- **You cannot take a production system offline** without production and safety impact assessment
- **Malware on a PLC** — do not attempt to remove it while the PLC is in production; isolate network and involve OT vendor
- **Network isolation** may itself cause a production stop — weigh this explicitly

### OT Incident Severity Levels
| Level | Trigger | Response |
|---|---|---|
| OT-SEV-1 | Malware active in Control Zone OR loss of control of safety-critical process | Immediate plant safety response + CISO + Plant Manager + OT vendor; consider controlled shutdown |
| OT-SEV-2 | Anomalous network traffic from OT to IT or internet; unauthorised access detected | Isolate affected segment; notify CISO and OT lead; do not disrupt production unless SEV-1 develops |
| OT-SEV-3 | Policy violation (e.g., USB used, unauthorised software); no evidence of compromise | Investigate; contain; report to OT security team |
| OT-SEV-4 | Vulnerability discovered; no evidence of exploitation | Risk register entry; schedule patch in next maintenance window |

### Notification Requirements
- OT-SEV-1/2: CISO notified within 1 hour; NIS2 incident report within 24 hours if applicable
- Regulatory notification: FDA/EMA/local authority within required timeframe if product quality or patient safety affected

---

## Regulatory Compliance Quick Reference

| Regulation | Applies To | Key OT Requirements |
|---|---|---|
| **IEC 62443** | All industrial automation | Zone/conduit model; Security Level targets; risk assessment |
| **NIST SP 800-82** | US critical infrastructure OT | OT-adapted controls framework; ICS security guidance |
| **EU NIS2 Directive** | Operators of essential services (manufacturing included) | Cybersecurity risk management; incident reporting within 24h; supply chain security |
| **FDA 21 CFR Part 11** | US pharmaceutical, medical, food (electronic records) | Audit trail; electronic signatures; access control; system validation |
| **EU Annex 11** | EU pharmaceutical (computer systems) | Validation; data integrity; backup; disaster recovery |
| **ISO 13485** | Medical device manufacturers | Management system; traceability; complaint handling; software validation |
| **ISO 22000** | Food safety | Hazard analysis; HACCP; traceability system requirements |
| **ATEX/IECEx** | Explosive atmosphere environments | Equipment certification; zoning; electrical safety |
