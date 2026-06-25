# Example: R&D & EDA Assessment — EDA Cluster Cloud Bursting for Tape-Out

## Input (Request Summary)

> "Our EDA simulation farm is at capacity during tape-out. We want to burst our Synopsys VCS simulation workloads to Azure. The team is proposing to use Azure HPC (HBv3 VMs) with a shared NFS mount from on-premises over ExpressRoute for design data access."

## Output (R&D & EDA Architecture Assessment)

## R&D & EDA Architecture Assessment

### R&D Stage and IP Context
This proposal affects the **Design Verification** stage — one of the most IP-sensitive phases of chip development. The design data involved includes RTL source code, testbenches, simulation models, and gate-level netlists — all of which represent core unreleased IP.

**Data classification:** Restricted (RD-POL-007). RTL and netlists are the highest-sensitivity pre-silicon IP. If this IP were disclosed, it would eliminate competitive advantage, potentially invalidate patent applications, and expose the company to export control liability.

**Key question before proceeding:** Is any of this chip design subject to EAR controls? High-performance semiconductor designs may involve EAR-controlled encryption or export-controlled process nodes. Answer required from Export Control Officer before cloud bursting is approved for this workload.

### Export Control Check
**⚠️ EXPORT CONTROL REVIEW REQUIRED**

The proposal does not include an export control classification of the design data. Before Azure cloud bursting is approved:

1. **ECO assessment required:** Is the chip design EAR-controlled (e.g., controlled encryption implementation, controlled RF functionality, controlled performance threshold under ECCN 3E001)?
2. **Azure region nationality:** Standard Azure commercial regions (including Netherlands-based Azure) are operated by Microsoft staff who may include non-US-persons. If the design is ITAR-controlled, Azure commercial is not permitted.
3. **If EAR-controlled:** Assess whether License Exception TSU (Technology and Software Unrestricted) or License Exception STA applies. If no exception: do not proceed with standard Azure; evaluate Azure Government or other sovereign cloud.
4. **Pending ECO assessment:** This assessment is CONDITIONAL on ECO clearance for cloud use.

**Assumption for the rest of this assessment:** ECO has confirmed the design is not ITAR-controlled and applicable EAR license exceptions permit cloud use (standard commercial assumption — must be validated).

### Performance Requirements Assessment
**Current on-premises profile:**
- 200 VCS simulation licenses (Synopsys SCL)
- 400-core Slurm farm for regression runs
- Storage: WEKA parallel filesystem, 800 TB usable, ~3 GB/s aggregate throughput
- Tape-out peak demand: 600+ concurrent simulation jobs — 200-core overflow unmet

**Azure HBv3 VM assessment:**
- HBv3-120 (120 AMD EPYC cores, 448 GB RAM, 480 GB NVMe local SSD): well-suited for simulation
- Recommended burst configuration: 10–20 HBv3-120 nodes (1,200–2,400 additional cores)
- Network to on-premises: **this is where the proposal has a critical flaw** (see below)

**Critical flaw — NFS over ExpressRoute:**
The proposal mounts on-premises NFS over ExpressRoute. EDA simulation workloads have extremely high storage I/O requirements — a 200-core simulation job on VCS may generate 50–200 GB/s of intermediate data in scratch directories. NFS over ExpressRoute (typically 1–10 Gbps) cannot support this throughput. The result: simulations run 10–50× slower than on-premises, making cloud burst effectively useless for the intended purpose.

**Required storage pattern for cloud burst:**
- Design data staging: copy project data subset to Azure Blob Storage (via AzCopy, encrypted, CMK) before burst jobs start
- Scratch storage: local NVMe on HBv3 nodes (480 GB per node) or Azure Managed Lustre (for multi-node shared scratch)
- Results pull-back: after job completion, copy results from Azure Blob back to on-premises; purge Azure copy
- NFS over ExpressRoute: used only for job submission and monitoring (head-node traffic) — not for data I/O

### Tool & License Architecture
**VCS (Synopsys VCS) on Azure:**
- Synopsys supports cloud deployment via Synopsys Cloud or self-managed cloud burst
- Synopsys SCL license server must serve licenses to Azure cloud nodes — two options:
  - **Option A:** Existing on-premises SCL server extends licenses to cloud nodes via secure tunnel — latency-sensitive; test round-trip time from Azure to on-premises SCL
  - **Option B:** Synopsys cloud-hosted license server (Synopsys Cloud subscription) — recommended for burst as it removes on-premises license server as a bottleneck
- **License availability:** 200 VCS licenses are insufficient for burst. Either lease additional cloud-burst licenses from Synopsys (pay-per-use / flex licensing) or confirm existing license count before burst architecture is finalised. Starting a burst run and finding licenses are exhausted is worse than not bursting.

**Tool installation on cloud nodes:**
- VCS binary installation: deploy via custom VM image (baked in, not installed at job start)
- PDK and standard cell library: staged to Azure Blob with CMK; mounted read-only on burst nodes
- No Synopsys binaries stored in Azure beyond the burst window — licence requires it

### Data Architecture and Retention
**Design data staged to cloud:**
- Only the specific project subset needed for burst runs (not the full EDA database)
- Encrypted with customer-managed key (Azure Key Vault, HSM-backed)
- Azure Blob Storage — dedicated storage account in isolated subscription
- Microsoft Cloud Storage access: restricted via Azure Private Endpoints; no public internet access to storage account
- Azure storage logs: all access events logged to Log Analytics (audit trail for IP access)

**Purge policy:**
- All staged design data purged from Azure within 24 hours of burst job completion
- Azure Blob lifecycle policy enforces deletion; confirmed by daily compliance check
- Intermediate scratch data (on NVMe) purged when VM is deallocated

**Retention on-premises:** Design data retained in DesignSync/Perforce under full version control per RD-POL-004. Cloud burst does not change on-premises retention obligations.

### PLM and Digital Thread
This proposal does not affect PLM or the digital thread — it is compute infrastructure for pre-silicon verification. No assessment required.

### Regulatory Impact
No GxP context for semiconductor design. NDA with foundry/PDK vendor may restrict cloud use of PDK data — confirm with IP/Legal team before PDK is staged to cloud.

### Recommendation
**APPROVE WITH CONDITIONS**

Cloud bursting for VCS simulation is technically and commercially sound for this use case — but the proposed NFS-over-ExpressRoute storage pattern must be replaced before any approval.

**Conditions:**
1. **Export control clearance** from ECO before any design data is staged to Azure (RD-POL-001/002)
2. **Replace NFS-over-ExpressRoute** with Azure Blob staging + local NVMe scratch pattern (as described above)
3. **Resolve license gap:** Confirm VCS license count for burst (existing 200 may be insufficient) or procure Synopsys flex cloud licenses
4. **Dedicated Azure subscription** for EDA burst — not shared with other workloads (IP isolation)
5. **Customer-managed keys** for all design data in Azure Blob (Key Vault HSM)
6. **Private endpoints** for all Azure storage access — no public internet endpoints
7. **Purge policy** enforced via Azure Blob lifecycle management; compliance verified
8. **PDK cloud use:** Confirm with foundry/PDK vendor that cloud staging is permitted under PDK licence agreement
9. **Synopsys cloud burst approval:** Confirm Synopsys licence agreement permits cloud burst deployment (most Synopsys agreements do, but requires verification)

### Dependencies on Peer Domains
- **Risk & Compliance:** Export control assessment (ECO); PDK and Synopsys licence agreement review (Legal/Procurement)
- **Security Architecture:** CMK configuration; private endpoint design; access control for Azure burst subscription; threat model for staged IP data
- **Technology & Infrastructure:** Azure HBv3 VM deployment, Azure Managed Lustre sizing, ExpressRoute capacity for head-node traffic

## Key Points Illustrated
- Export control surfaced immediately as a gate — not an afterthought
- Storage performance flaw in proposal identified with quantitative reasoning (throughput mismatch)
- Correct storage pattern for EDA cloud burst described in detail (staging, NVMe scratch, pull-back, purge)
- License architecture addressed concretely (not just "check with vendor")
- CMK and IP access logging specified — this is IP, not generic enterprise data
- PDK cloud use flag raised — often missed, legally significant
- Approval is conditional, not blocked — path forward is clear
