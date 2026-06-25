# Example: Manufacturing & OT Assessment — IIoT Cloud-Connected Predictive Maintenance

## Input (Request Summary)

> "We want to implement predictive maintenance for our production lines. The plan is to connect our PLCs directly to Azure IoT Hub using the Azure IoT SDK, then send real-time sensor data to Azure ML for anomaly detection. Azure ML will trigger maintenance alerts."

## Output (Manufacturing & OT Architecture Assessment)

## Manufacturing & OT Architecture Assessment

### Purdue Model Impact
The proposal as described directly violates the Purdue Reference Model by connecting Level 1 systems (PLCs) directly to cloud (Level 5+):

**Proposed (non-compliant):**
```
PLC (Level 1) → [Azure IoT Hub SDK directly on PLC] → Azure ML (cloud)
```

This collapses Levels 1 through 3.5, eliminating the DMZ entirely. The PLC would have a direct internet-routed connection.

**Required (compliant):**
```
PLC (L1) → SCADA (L2) → Historian (L3) → IoT Edge (L3) → DMZ Gateway → Azure IoT Hub → Azure ML
```

**Blocking finding:** The proposed architecture bypasses the OT DMZ. This is a violation of OT-P-002 and OT-POL-001. The proposal cannot be approved as described.

### OT Safety & Availability Assessment
**Safety impact:** The production lines include several PLCs connected to pneumatic systems and conveyor drives. No dedicated SIS identified — but the proposal would create a cloud dependency in the PLC's network stack. If Azure IoT Hub SDK on the PLC consumes CPU or memory during cloud communication, this can cause PLC scan cycle overruns — a safety-relevant failure mode on motion control equipment. **This risk is unacceptable at Level 1.**

**Availability requirement:** Continuous production process. Target availability: **99.99%** (OT-P-003). The proposal introduces a cloud availability dependency into the real-time control path. Azure IoT Hub SLA is 99.9% — this would degrade the production system below its target.

**Latency sensitivity:** Predictive maintenance alerts are non-real-time — batch-tolerant (minutes to hours is acceptable). This is important: it means there is **no business reason** to connect PLCs directly to cloud. The data does not need real-time cloud delivery.

### IT/OT Convergence Analysis
The proposal as designed creates a direct internet-facing connection at Level 1. This is one of the most severe OT security anti-patterns:

- A compromised Azure IoT Hub credential would give an attacker a direct conduit to PLC network
- The PLC's embedded networking stack is not designed for internet-facing traffic or TLS certificate management
- No existing DMZ controls would be bypassed — they would simply not exist in this path

**Compliant redesign:** The internet-facing IoT connection must terminate at Level 3 (IoT Edge node) or Level 3.5 (DMZ). Data is pulled from the Historian (not directly from PLC) and forwarded via the IoT Edge connector.

### Manufacturing Data Architecture
**Current state:** Production PLCs publish data to Siemens WinCC SCADA (Level 2). WinCC feeds the plant Historian (OSIsoft PI). PI is the authorised data source for enterprise analytics (OT-P-006, OT-POL-009).

**Compliant data flow:**
1. PLCs publish vibration, temperature, and motor current data to WinCC SCADA (existing, unchanged)
2. WinCC PI Interface feeds data to OSIsoft PI Historian (Level 3) — existing
3. Azure IoT Edge node at Level 3 runs PI Connector for IoT — pulls from PI and forwards to Azure IoT Hub via HTTPS through DMZ (new)
4. Azure IoT Hub ingests to Azure Event Hubs → Azure Fabric → Azure ML training
5. Azure ML trained model deployed to IoT Edge as module — runs inference locally at Level 3
6. Inference output: maintenance alert → sent to CMMS (ServiceNow) via Azure Logic Apps — not a PLC control signal

**Data classification:** Vibration and motor current telemetry = Internal. Production throughput implied by motor data = Confidential. Ensure Historian replication to Azure is covered by DPA and does not cross data sovereignty boundary.

### Regulatory & Compliance Impact
No pharmaceutical/food GxP context identified for this plant. However:
- **NIS2:** If this organisation is a medium/large manufacturer classified as Important Entity, OT cybersecurity risk management is required — this proposal improves visibility (positive) but must be implemented with NIS2-compliant controls
- **CMDB:** Azure IoT Edge nodes deployed in the plant must be registered as OT assets in ServiceNow CMDB (OT-POL-003) before deployment

### OT Lifecycle Considerations
**Siemens S7-1200 PLCs identified:** Firmware 4.4, circa 2019. These PLCs do not support TLS natively and cannot run the Azure IoT Hub SDK. This confirms the PLC-direct approach is not only architecturally non-compliant but also technically infeasible on the existing hardware.

**IoT Edge nodes:** Recommend **Advantech UNO-2484G** industrial PCs (DIN-rail, fanless, -25°C to 70°C rated) running Azure IoT Edge on Ubuntu Server 22.04 LTS. These are purpose-built for plant-floor deployment and are not standard IT servers.

### Recommendation
**APPROVE WITH CONDITIONS — after redesign**

The business objective (predictive maintenance via Azure ML) is valid and achievable. The proposed implementation is not. The following redesign is required before any approval:

**Conditions:**
1. Remove Azure IoT SDK from all PLC connections — PLCs do not connect to cloud, directly or indirectly
2. Implement compliant data flow: PI Historian → Azure IoT Edge → IoT Hub → Azure ML (as described above)
3. IoT Edge nodes deployed in plant floor (Level 3); registered in CMDB before deployment
4. All IoT Hub traffic routes through DMZ — existing DMZ firewall updated with outbound HTTPS rule (IoT Hub FQDN allowlisted, not open internet)
5. Azure ML inference deployed to IoT Edge — cloud outage must not stop maintenance alert capability locally
6. Maintenance alerts sent to ServiceNow CMMS — not control signals back to PLCs

### Dependencies on Peer Domains
- **Security Architecture:** DMZ firewall rule change; IoT Hub credential management; threat model for Edge node
- **Technology & Infrastructure:** IoT Edge node procurement and deployment; Azure IoT Hub namespace provisioning
- **Data & AI:** Azure ML model training pipeline on historian data; confirm data sovereignty for PI data replication to Azure

## Key Points Illustrated
- Purdue model violation identified immediately — blocking finding raised before anything else
- Safety risk of SDK on PLC scanner explained concretely (scan cycle overrun)
- Latency analysis removes the only possible business justification for direct PLC connection
- Compliant redesign provided step by step — not just a rejection
- PLC hardware capability checked — SDK approach is also technically infeasible
- Edge autonomy requirement stated explicitly (cloud outage must not affect maintenance alerts)
- Industrial PC specification given (not standard IT servers for plant floor)
