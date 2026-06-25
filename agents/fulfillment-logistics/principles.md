# Supply Chain & Fulfillment Architecture Principles

## OT-P-001: Safety First, Always
**Statement:** Safety Instrumented Systems (SIS) and safety-critical control loops are architecturally isolated and never share networks, compute, or dependencies with non-safety systems.

**Rationale:** SIS must achieve their Safety Integrity Level (SIL) under all circumstances including cyber attack, IT maintenance, and network failure. Any dependency on non-safety systems can degrade the SIL.

**Implications:**
- SIS networks are physically separated (air-gapped) from all other OT and IT networks
- No remote access to SIS — local access only, with authorised personnel
- Any proposal to connect SIS to SCADA, MES, or IT must be rejected
- SIS vendor approval is required for any architectural change in the SIS vicinity

---

## OT-P-002: Purdue Model / ISA-95 Hierarchy
**Statement:** The manufacturing architecture follows the Purdue Reference Model. Data flows upward (field → control → supervisory → operations → enterprise). Control commands flow downward only within authorised pathways with explicit change control.

**Rationale:** Maintaining clear level separation is the foundation of OT security and operational reliability. Collapsing levels increases the attack surface and operational coupling.

**Level reference:**
- **Level 0:** Physical process (sensors, actuators, valves)
- **Level 1:** Basic control (PLCs, RTUs, drives)
- **Level 2:** Supervisory control (SCADA, DCS, HMI)
- **Level 3:** Site operations (MES, historian, OEE)
- **Level 3.5:** DMZ (data diodes, protocol brokers, jump servers)
- **Level 4:** Business logistics (ERP, planning)
- **Level 5:** Enterprise (corporate IT, cloud)

**Implications:**
- All IT↔OT data flows pass through the Level 3.5 DMZ
- No direct connectivity between Level 2 and Level 4+ is permitted without explicit DMZ implementation
- Cloud-connected MES must operate at Level 3 with a DMZ below it — never direct OPC UA to cloud

---

## OT-P-003: Availability Over All Else
**Statement:** Unplanned downtime is unacceptable. Architecture decisions that improve features but risk production availability will not be approved without explicit quantification of the availability trade-off and acceptance by the Plant Manager.

**Rationale:** In manufacturing, 1 hour of unplanned downtime typically costs €10,000–€500,000 depending on the process. IT availability norms (99.9% = 8.7h downtime/year) are not acceptable for OT.

**OT availability targets (default):**
- Continuous process (chemical, pharma, food): **99.99%** (< 1h/year)
- Batch process: **99.95%** (< 4.4h/year) per campaign
- Discrete manufacturing (automotive, electronics): **99.9%** per planned shift schedule

**Implications:**
- Redundancy is standard for Levels 1–3 in critical processes
- Patching and updates require a planned maintenance window — never during production
- Architecture changes must define rollback procedures with <15 minute recovery time
- Cloud dependency in real-time control paths is prohibited (network latency and availability cannot be guaranteed)

---

## OT-P-004: OT Network Segmentation (IEC 62443 Zones & Conduits)
**Statement:** OT networks are segmented into IEC 62443 security zones with defined conduits between them. Zone assignment determines the security level target (SL-T) and the controls required.

**Default zone structure:**
| Zone | Contents | SL-T | Key Controls |
|---|---|---|---|
| Safety Zone | SIS, ESD | SL4 | Air-gap; physical access only |
| Control Zone | PLC, RTU, DCS | SL2–3 | Isolated VLAN; no internet; limited conduits |
| Supervisory Zone | SCADA, HMI | SL2 | Unidirectional gateway preferred; no direct IT |
| Operations Zone | MES, Historian, OEE | SL2 | DMZ boundary; monitored conduit to IT |
| IT/OT DMZ | Protocol brokers, jump servers | SL2 | All IT↔OT traffic here; IDS/IPS monitoring |

**Implications:**
- Any proposal must identify which zones are affected
- Adding a new conduit (connection between zones) requires a security risk assessment
- IT security tools (EDR, vulnerability scanners) must be OT-safe before deployment in Control or Supervisory zones

---

## OT-P-005: Long Lifecycle & Legacy Compatibility
**Statement:** OT systems have lifecycles of 10–25 years. Architecture decisions must be compatible with existing OT assets and must not require replacement of in-service control equipment to achieve IT goals.

**Rationale:** A PLC installed in 2008 controlling a critical reactor may run until 2030. Its operating system, firmware, and protocols are fixed by the vendor and the qualification state. IT architectural principles (e.g., "no Windows 7") cannot override operational and regulatory constraints.

**Implications:**
- Protocol adapters and gateways (OPC UA servers, protocol converters) bridge legacy protocols — the PLC itself is not changed
- IT security tools must be validated as OT-safe before deployment near legacy systems
- End-of-life IT components embedded in OT systems are managed via compensating controls (network isolation, application whitelisting), not forced upgrades
- Any forced upgrade of an in-service control system requires production planning, regulatory revalidation (if applicable), and vendor support

---

## OT-P-006: Data Historian as OT Data Platform
**Statement:** Time-series process data from Levels 0–3 is collected via a plant historian (PI System / InfluxDB / Ignition). The historian is the system of record for OT data and the single authorised source for feeding enterprise analytics.

**Rationale:** Direct database queries or API calls against SCADA/DCS/PLC systems are not safe for OT environments — they consume controller resources and can disrupt real-time control.

**Implications:**
- All enterprise data consumers (analytics, AI, ERP) read from the historian, not from SCADA/DCS directly
- Historian replication to the enterprise data platform crosses the DMZ via a secure connector
- Real-time dashboards in enterprise tools read from historian replicas, not live OT systems
- Historian data classification: Confidential (process recipes, throughput data) or Restricted (if safety-related)

---

## OT-P-007: Change Control for OT Systems
**Statement:** All changes to OT systems at Levels 1–3 follow OT change control — separate from IT change management, with additional steps for production impact assessment, qualification (if regulated), and Plant Manager approval.

**Rationale:** An OT change that causes a production stop or quality deviation can have regulatory consequences (batch recall, regulatory reporting) that IT change management does not account for.

**OT change gate requirements (in addition to IT CHG):**
1. Production impact assessment (can change be applied during scheduled maintenance?)
2. Rollback procedure tested in staging environment
3. For regulated environments: IQ/OQ/PQ revalidation scope defined
4. Plant Manager sign-off
5. Quality/Regulatory sign-off (if applicable)

---

## OT-P-008: Industry 4.0 / Smart Factory — Cloud with Constraints
**Statement:** Cloud-enabled Industry 4.0 capabilities (digital twin, AI-driven OEE, predictive maintenance) are supported — but cloud connectivity is restricted to non-real-time data flows and must never introduce cloud availability into real-time control paths.

**Allowed pattern (cloud with constraints):**
```
PLC → SCADA → Historian → OT DMZ → Azure IoT Hub / Event Hubs → Azure ML / Fabric
```
**Prohibited pattern:**
```
PLC → Cloud (directly) — violates OT-P-002 and OT-P-003
```

**Implications:**
- Cloud ML models for predictive maintenance run on edge (Azure IoT Edge / NVIDIA Jetson) at Level 3 — not in real-time control loops
- Inference results are advisory, not control signals
- Cloud outages must not affect production — edge must operate autonomously
