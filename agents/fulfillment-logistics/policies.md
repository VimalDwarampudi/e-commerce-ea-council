# Supply Chain & Fulfillment Architecture Policies

## OT-POL-001: Mandatory DMZ for All IT/OT Integration
**Requirement:** Any data flow between OT networks (Levels 0–3) and IT networks (Levels 4–5) MUST traverse a Level 3.5 DMZ. Direct connectivity is prohibited.

**Compliant patterns:**
- Unidirectional security gateway (data diode) for read-only OT→IT flows
- Bidirectional DMZ with dual-homed servers, IDS/IPS monitoring, protocol inspection
- Jump server / bastion host for authorised remote maintenance (OT-POL-004)

**Non-compliant patterns (prohibited):**
- VPN directly into the OT control network from corporate IT
- Cloud connectors (Azure IoT Hub SDK, MQTT broker) installed directly on SCADA/DCS servers
- OPC UA server on a PLC exposed directly to the corporate LAN

---

## OT-POL-002: No Remote Access to Safety Systems
**Requirement:** Safety Instrumented Systems (SIS), Emergency Shutdown (ESD), and Fire & Gas (F&G) systems have zero remote access capability. All maintenance is local, with physical presence.

**No exceptions.** Proposals to enable remote monitoring or maintenance of SIS require escalation to the CISO and Plant Safety Manager and are subject to independent safety assessment.

---

## OT-POL-003: OT Asset Register in CMDB
**Requirement:** All OT assets at Levels 1–3 (PLCs, HMIs, SCADA servers, historians, MES servers, industrial PCs) must have a Configuration Item record in ServiceNow CMDB with the following fields populated:
- Asset name and physical location (plant, line, cell)
- Manufacturer and model
- OS/firmware version
- Network zone (IEC 62443 zone)
- Lifecycle status
- Responsible engineer (not just a team)
- Last patch/firmware date

**Compliance check:** EA Council will query CMDB for OT assets as part of any assessment. Unregistered OT assets in scope of a proposal are a blocking finding.

---

## OT-POL-004: OT Remote Access via Dedicated Jump Server
**Requirement:** Remote access to OT networks (for authorised maintenance, vendor access, or monitoring) is only permitted via a dedicated OT jump server / bastion host in the DMZ. Requirements:
- Multi-factor authentication mandatory
- Session recording for all sessions (audit trail)
- Separate credentials from IT systems (no SSO with corporate AD into OT network)
- Vendor access: time-limited, single-session tokens; never permanent credentials
- No persistent network access — connections are proxied, not tunnelled

---

## OT-POL-005: Industrial Protocol Adoption
**Requirement:** New integrations and new assets at Levels 1–3 must use open, standard protocols where technically feasible:
- **Preferred:** OPC UA (secure channel, certificates, publish-subscribe via OPC UA PubSub)
- **Acceptable:** MQTT (with TLS and authentication, for edge/IIoT)
- **Tolerated (legacy):** Modbus TCP, EtherNet/IP, PROFINET — only for existing assets or where OPC UA is not supported by the vendor
- **Prohibited for new deployments:** Proprietary vendor protocols with no documented standard interface

---

## OT-POL-006: OT Security Tools Must Be OT-Validated
**Requirement:** IT security tools (vulnerability scanners, EDR agents, patch management, network monitoring) must be validated as safe for OT environments before deployment in Levels 1–3. "OT-validated" means:
- Vendor has explicitly certified the tool for use in ICS/SCADA environments
- Passive monitoring only in Control Zone (no active scanning of PLCs)
- Tool does not interfere with real-time control cycles
- Acceptable OT security tools: Claroty, Dragos, Nozomi Networks, Microsoft Defender for IoT (passive mode)
- **Prohibited in Control Zone:** Nessus / Tenable active scanning, CrowdStrike EDR (unless OT-mode validated), any tool that generates network traffic toward Level 1 devices

---

## OT-POL-007: Manufacturing Data Classification
**Requirement:** Manufacturing data is classified as follows. Classification drives access control, encryption, and sovereignty requirements.

| Data Type | Classification | Sovereignty Requirement |
|---|---|---|
| Real-time process values (non-recipe) | Internal | None |
| Production volumes, OEE, throughput | Confidential | Do not leave country without approval |
| Product recipes, formulations, process parameters | **Restricted** | Do not leave country; encrypted at rest and in transit |
| Safety system parameters and configurations | **Restricted** | Air-gapped storage only |
| Quality batch records (regulated industries) | **Restricted** | Must be accessible for regulatory inspection; retention ≥ product shelf life + 1 year |
| Predictive maintenance model training data | Confidential | May go to cloud with DPA |

---

## OT-POL-008: Regulated Industry Validation Requirements
**Requirement:** In regulated manufacturing environments (pharmaceuticals under GxP, medical devices under ISO 13485/FDA, food under FDA 21 CFR Part 11 or EU Annex 11), all computer system changes require a defined validation approach:

- **Impact assessment:** Does the change affect a validated system or a parameter governed by a regulatory submission?
- **Validation scope:** IQ (Installation Qualification), OQ (Operational Qualification), PQ (Performance Qualification) — scope defined by risk assessment
- **Electronic records/signatures:** If the system generates electronic records or signatures that replace paper records, 21 CFR Part 11 / EU Annex 11 compliance is required
- **Change control linkage:** OT CHG record linked to Quality change control record (Deviations/CAPAs if applicable)

---

## OT-POL-009: Historian as Only Authorised OT Data Source for Enterprise
**Requirement:** Enterprise systems (ERP, analytics, AI platforms) must retrieve OT operational data exclusively via the plant historian interface. Direct queries against SCADA databases, DCS data servers, or PLC memory are prohibited.

**Rationale:** Direct queries can consume PLC/SCADA resources, cause control cycle overruns, and introduce uncontrolled network traffic into the control network.

---

## OT-POL-010: Edge Computing Deployment Baseline
**Requirement:** Edge compute nodes deployed in plant environments (Azure IoT Edge, NVIDIA Jetson, industrial PCs running containerised workloads) must meet:
- Hardened OS (CIS benchmark Level 2 for industrial Linux or Windows IoT)
- No unnecessary services or ports open
- Secure boot enabled
- Remote management via OT jump server only (OT-POL-004)
- Container images from approved registry only
- Edge must operate autonomously when disconnected from cloud — no dependency on cloud availability for local production operations
