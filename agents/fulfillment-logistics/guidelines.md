# Manufacturing & OT Architecture Guidelines

## How to Assess an IT/OT Integration Proposal

### Step 1: Map to the Purdue Model
Before anything else, identify where the proposed components sit in the Purdue hierarchy:
- Which Purdue level does each component live at?
- Does the proposal cross a level boundary? If so, how?
- Is a DMZ (Level 3.5) part of the design, or is it being bypassed?

If the proposal collapses or bypasses levels, it is a **blocking finding** — stop and raise it immediately.

### Step 2: Identify OT Asset Context
Query ServiceNow CMDB for assets in scope:
```
GET /api/now/table/cmdb_ci_server
  ?sysparm_query=location={plant}^name LIKE {system}
  &sysparm_fields=name,os,os_version,location,
                  u_purdue_level,u_ot_zone,u_lifecycle_status,
                  u_last_patch_date,supported_by
```
Check LeanIX for the manufacturing capability context:
- Which manufacturing capabilities are affected?
- Is the application in the LeanIX landscape? What is its lifecycle status?

### Step 3: Assess OT Safety Impact
Answer these questions:
- Does any component in the proposal sit within or adjacent to a Safety Instrumented System (SIS)?
- Does the proposal change network topology in a way that could affect SIS isolation?
- Does the proposal affect alarm management, emergency shutdown logic, or fire & gas systems?

If **yes** to any: invoke OT-P-001 and require independent safety assessment before proceeding.

### Step 4: Availability & Latency Assessment
- What is the production process type? (Continuous / Batch / Discrete)
- What is the required availability for the affected systems?
- Does the proposal introduce any new dependency that could cause an unplanned stop?
- What is the latency requirement? Can cloud round-trips be tolerated?

### Step 5: Data Flow Design Review
For any data flowing from OT to IT:
- Source system and Purdue level?
- Protocol used at source (OPC UA, Modbus, proprietary)?
- Protocol translation point?
- Historian integration: is the historian in the path?
- DMZ crossing: where and how?
- Destination system and classification of the data?

### Step 6: Regulatory Impact Check
- Is this a regulated manufacturing environment? (GxP, FDA, ISO 13485, ISO 22000?)
- Does the change affect a validated system?
- Is a validation impact assessment required?
- Are electronic records or signatures involved? (21 CFR Part 11 / EU Annex 11?)

### Step 7: OT Lifecycle Check
- What is the age and expected remaining service life of affected OT assets?
- Are any assets running end-of-life OS/firmware? What compensating controls exist?
- Does the proposal require firmware/OS updates that need vendor qualification?
- Is there a vendor support contract in place?

---

## IEC 62443 Security Level Assessment

When evaluating OT security measures, use IEC 62443 Security Levels:

| SL | Description | Typical Zone | Key Controls |
|---|---|---|---|
| SL0 | No security requirements | N/A | None |
| SL1 | Protection against casual/unintentional violations | Non-critical monitoring | Basic authentication, audit logs |
| SL2 | Protection against intentional violation with low resources | Operations, Supervisory | Network segmentation, MFA for remote access, IDS |
| SL3 | Protection against sophisticated intentional attack | Critical control | Encryption, application whitelisting, no internet, OT-specific IDS |
| SL4 | Protection against state-sponsored/advanced persistent threat | Safety systems | Air-gap, physical controls, tamper detection |

**Assessment rule:** Every proposed zone must have a defined Security Level Target (SL-T). The implemented controls must achieve or exceed SL-T.

---

## IT/OT DMZ Design Patterns

### Pattern A: Unidirectional Security Gateway (Data Diode)
**When to use:** OT→IT data flows only; no commands flow back to OT (read-only telemetry)
```
OT Network → [Data Diode] → DMZ Replica Server → IT Network
```
- Hardware-enforced one-way data flow (physically impossible to send from IT to OT)
- Appropriate for: historian replication, production monitoring, OEE dashboards
- Products: Waterfall Security FLIP, Owl Cyber Defense

### Pattern B: Bidirectional DMZ with Dual-Homed Broker
**When to use:** Bidirectional data flows required (e.g., ERP sending production orders to MES; MES responding with completions)
```
OT Network → [OT Firewall] → DMZ Broker → [IT Firewall] → IT Network
```
- DMZ broker has two NICs — one OT-facing, one IT-facing — and never routes packets directly
- Application-layer protocol inspection (not just TCP/IP forwarding)
- IDS/IPS monitoring all DMZ traffic
- Message validation and schema enforcement in the broker

### Pattern C: Jump Server for Remote Maintenance
**When to use:** Authorised vendor or engineer needs temporary interactive access to OT systems
```
IT Network → [MFA + Session Recording] → Jump Server (DMZ) → OT Network (time-limited)
```
- No persistent tunnel — each session is individually authorised
- Session recording mandatory
- Jump server is single-purpose — no other workloads

---

## Industry 4.0 Architecture Guide

### Recommended Smart Factory Stack

```
Level 5 (Cloud):    Azure Fabric / Azure ML / Power BI
                           ↑ (non-real-time replication)
Level 4 (Enterprise): ERP, EAM, Quality Management System
                           ↑
Level 3.5 (DMZ):    Azure IoT Hub connector / OPC UA Gateway
                           ↑
Level 3 (Operations): MES, Plant Historian (PI/InfluxDB), OEE platform
                    + Azure IoT Edge node (inference only, advisory)
                           ↑
Level 2 (Supervisory): SCADA / DCS / HMI
                           ↑
Level 1 (Control):  PLCs / RTUs / Drives
                           ↑
Level 0 (Physical): Sensors, actuators, valves, motors
```

### IIoT Data Flow (standard pattern)
1. PLC/sensor publishes data via OPC UA (Level 1→2)
2. SCADA/DCS aggregates to Historian (Level 2→3)
3. Historian replicates to IoT Edge via OPC UA Publisher (Level 3)
4. IoT Edge forwards to Azure IoT Hub via DMZ connector (Level 3→3.5→cloud)
5. Azure Event Hubs / Fabric ingests for analytics
6. Azure ML trains models on historical data; deploys inference to IoT Edge
7. Edge inference runs locally — cloud outage does not affect production

### Predictive Maintenance Architecture
- **Training:** Cloud (Azure ML) — uses historical historian data; no real-time OT dependency
- **Inference:** Edge (Azure IoT Edge at Level 3) — low latency, autonomous
- **Action:** Advisory only — alert to maintenance team, never a direct control command
- **Model update:** New model versions deployed to edge during planned maintenance windows, not live

---

## Common Anti-Patterns (Do Not Approve)

| Anti-Pattern | Risk | Alternative |
|---|---|---|
| OPC UA server on PLC exposed to corporate LAN | Bypasses DMZ; PLC directly accessible from IT | OPC UA server in Operations zone (Level 3) aggregates from PLCs |
| Azure IoT Hub SDK installed on SCADA server | SCADA directly cloud-connected; availability risk; bypasses DMZ | IoT Edge at Level 3 or dedicated IoT gateway in DMZ |
| IT vulnerability scanner deployed in Control Zone | Active scanning can crash PLCs or cause control cycle overruns | OT-specific passive monitoring (Claroty, Dragos) in passive mode only |
| Corporate AD used for SCADA authentication | Corporate AD compromise = SCADA access | Separate OT Active Directory / local accounts with OT-specific PAM |
| Cloud MES without local fallback | Cloud outage stops production | Hybrid MES: cloud for analytics; local MES for real-time scheduling with 72h offline capability |
| Patching PLCs via IT patch management | IT patch tools not OT-safe; breaks validation in regulated environments | Vendor-managed firmware updates in scheduled maintenance windows |
| Shared network segment for IT workstations and HMIs | IT workstation compromise can reach HMI | Separate VLANs; firewall rules; HMIs use dedicated OT accounts |
