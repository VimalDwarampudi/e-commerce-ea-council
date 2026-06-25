# Customer Experience Architecture Policies

## RD-POL-001: Export Control Classification at System Onboarding
**Requirement:** Before any user is granted access to systems handling R&D or engineering data, an export control classification check must be completed:
1. Is the data in the system subject to ITAR, EAR, or EU Dual-Use controls?
2. Is the user a "US Person" or authorised under an applicable license? (for ITAR)
3. Is the user's nationality consistent with applicable EAR license exceptions?

This check is performed by the Export Control Officer (ECO) or their designate. IT cannot grant access to export-controlled systems independently.

---

## RD-POL-002: Export-Controlled Data Must Not Be Stored in Public Cloud Without Authorised Controls
**Requirement:** ITAR-controlled technical data and EAR-controlled data without an applicable license exception must not be stored in or transmitted through public cloud infrastructure (Azure, AWS, GCP standard regions) without:
- **For ITAR:** US Government cloud (Azure Government, AWS GovCloud) with ITAR-compliant configuration, or on-premises
- **For EAR:** Evaluate applicable license exceptions (e.g., EAR §740.13 License Exception TSU); where no exception applies, use the same approach as ITAR

**Assessment requirement:** Any proposal to move R&D data to cloud must include an export control classification of the data as part of the architecture review. If classification is unknown, treat as Restricted pending ECO assessment.

---

## RD-POL-003: PLM is the System of Record for Product Structure
**Requirement:** The PLM system (Teamcenter, Windchill, Enovia, or equivalent) is the single system of record for:
- Engineering Bill of Materials (eBOM)
- Manufacturing Bill of Materials (mBOM) — derived from eBOM in PLM
- Engineering Change Orders (ECO) and Change Notices (ECN)
- Document control (controlled documents, work instructions, specifications)
- Configuration management and variant management

No other system creates or maintains the authoritative product structure. ERP receives mBOM via integration from PLM — it does not independently manage BOMs.

---

## RD-POL-004: EDA Design Data Must Be Stored in a Managed Design Data Management System
**Requirement:** IC/chip design data (RTL, schematics, layout databases, simulation models, verification suites) must be stored in an authorised Design Data Management (DDM) system with:
- Version control (not a shared file system with no versioning)
- Access control at project and design-block level
- Check-in/check-out workflow (prevent simultaneous conflicting edits)
- Audit trail of all check-in/check-out events
- Automated backup with tested restore capability

**Acceptable DDM systems:** Cadence Design Management (CDM), Synopsys DesignSync, Perforce Helix Core (with appropriate config), or equivalent enterprise DM with the above capabilities.

**Not acceptable:** Shared NAS folders, SharePoint document libraries (no EDA-aware versioning), personal drives, or Git without EDA-specific configuration (binary EDA databases are not suited to standard Git).

---

## RD-POL-005: Research Data Must Be Recorded in ELN/LIMS
**Requirement:** All experimental data and laboratory results that could form the basis of a patent application, regulatory submission, publication, or IP disclosure must be recorded in the authorised Electronic Lab Notebook (ELN) or LIMS at the time of the experiment — not retrospectively transcribed from paper.

**Rationale:** ELN timestamps are legally defensible evidence of invention date. Paper notebooks transcribed later are not.

**Backup requirement:** ELN/LIMS data must be backed up with a separate backup credential from production systems. Recovery tested quarterly.

---

## RD-POL-006: License Server High Availability is Mandatory
**Requirement:** All EDA and commercial CAE license servers must be deployed in a high-availability configuration:
- Primary + standby license server (automatic failover)
- License server hosts on redundant power and network
- License server software and configuration backed up daily
- Failover tested during quarterly maintenance windows
- License server maintenance changes require advance notification to all users (minimum 24 hours)

**Monitoring:** License server availability is monitored with alerting to the R&D IT team. License checkout failure rate >1% triggers investigation.

---

## RD-POL-007: IP Data Classification Baseline for R&D
**Requirement:** All R&D and engineering data is classified at minimum as follows:

| Data Type | Classification | Special Handling |
|---|---|---|
| Core IP: chip design databases, formulations, process parameters | **Restricted** | Need-to-know access; no cloud without ECO approval; access logged |
| Product specifications, requirements documents | **Restricted** | Controlled in PLM/DMS; access by project team |
| Simulation models and results (novel/unpublished) | **Confidential** | Project access control; export control check |
| Published research data | Internal (post-publication) | Normal handling after publication |
| Lab notebooks / ELN entries (pre-patent filing) | **Restricted** | Legal hold capability required; no deletion |
| Patent applications (pre-filing) | **Restricted** | Attorney-client privilege; access: IP team + named inventors only |
| Third-party data under NDA | **Restricted** | Handle per NDA terms; do not commingle with own IP |

---

## RD-POL-008: External Collaboration Requires Technology Control Plan
**Requirement:** Before sharing R&D or engineering data with an external party (joint venture partner, contract research organisation, supplier, university), a Technology Control Plan (TCP) must be in place covering:
1. Export control classification of shared data
2. Authorised recipients and their nationality check (for ITAR)
3. Technical controls for the collaboration environment (shared vault, secure workspace)
4. Data handling and destruction requirements at collaboration end
5. IP ownership and licensing terms (referenced from the legal agreement)

**Technical controls for external collaboration:** Use a dedicated secure collaboration workspace (e.g., Egnyte, SharePoint dedicated site with DLP, or a physical clean room for highest sensitivity) — never email or personal Dropbox.

---

## RD-POL-009: HPC Cluster Access Controls
**Requirement:** HPC clusters used for R&D compute (chip simulation, CFD, ML training) must implement:
- Project-based access control: researchers access only their project's data and compute quota
- Job accounting: all compute jobs logged with user, project, resource consumption, and wall time
- Data residency: HPC scratch and project storage must not replicate to regions outside the approved data residency boundary
- Export control: if the cluster runs ITAR-controlled workloads, non-US-Person users must not have access to those job directories or results — enforced technically (not just policy)

---

## RD-POL-010: Regulated Research (GLP/GCP) Computer System Validation
**Requirement:** In pharmaceutical and medical device R&D, any computer system used to acquire, process, report, or store data that supports a regulatory submission must be validated per applicable GxP standards:
- **GLP (Good Laboratory Practice):** Systems supporting non-clinical safety studies
- **GCP (Good Clinical Practice):** Systems supporting clinical trials (eTMF, EDC, randomisation)
- **21 CFR Part 11 / EU Annex 11:** Electronic records and signatures

**Validation requirements:**
- User Requirements Specification (URS)
- Risk-based validation plan: IQ, OQ, PQ
- Validation report reviewed and approved by Quality
- Change control: all system changes assessed for validation impact
- Periodic review: system re-validation or confirmation that validation remains current (typically every 3 years or on major upgrade)
