# Customer Experience Architecture Principles

## RD-P-001: Intellectual Property is the Primary Asset
**Statement:** R&D and design data represents the organisation's primary competitive asset. Architecture decisions for R&D systems prioritise IP protection — confidentiality, integrity, and traceability — above all other considerations except safety.

**Rationale:** Loss of R&D data through breach, inadvertent disclosure, or insider threat can eliminate competitive advantage, invalidate patent applications, and create export control liability.

**Implications:**
- All R&D data is classified Confidential or Restricted by default — no R&D data is Internal or Public unless explicitly reviewed
- Systems handling R&D data require IP-specific access controls (need-to-know, not just job-level)
- Cloud and external collaboration requires explicit IP risk assessment before any R&D data leaves the controlled environment
- All access to core IP (EDA databases, formulations, core design files) is logged and auditable

---

## RD-P-002: Export Control Compliance is Non-Negotiable
**Statement:** Architecture for R&D systems must be designed to prevent unauthorised access to export-controlled technical data (ITAR, EAR, EU Dual-Use) by non-authorised persons, regardless of their employment status or physical location.

**Rationale:** ITAR violations carry criminal penalties of up to 20 years imprisonment and $1M per violation. EAR violations are also criminal. These are not IT compliance issues — they are legal requirements.

**Export control technical data definition (simplified):**
- ITAR (US): Technical data related to defence articles on the US Munitions List (USML) — aerospace, military electronics, encryption
- EAR (US): Dual-use items on the Commerce Control List (CCL) — high-performance chips, certain chemicals, encryption
- EU Dual-Use: European equivalent of EAR

**Implications:**
- Any system storing export-controlled technical data must restrict access by nationality of users (not just location)
- Cloud systems must guarantee that cloud provider employees with access rights do not include non-authorised nationals — this typically requires dedicated/sovereign cloud options
- External collaboration (supply chain, joint ventures) requires technology control plan (TCP) before sharing controlled data
- New employees and contractors accessing R&D systems require export control classification check at onboarding

---

## RD-P-003: Performance First for Compute-Intensive Workloads
**Statement:** Architecture for EDA, CAE, and HPC workloads is optimised for computational throughput and tool compatibility. Security and IT standardisation controls that measurably degrade performance or tool compatibility are not imposed without a validated risk-justified alternative.

**Rationale:** A chip design schedule runs on EDA tool runtimes. An FEA simulation that runs 3× longer because of storage performance degradation has the same business impact as a system outage. R&D productivity is quantifiable and financially material.

**Implications:**
- HPC storage uses parallel file systems (Lustre, GPFS, WEKA) or NVMe — not NAS/NFS shared storage that cannot support EDA throughput
- Network for HPC: InfiniBand (HDR/NDR) or high-bandwidth Ethernet (100GbE+) with RDMA for MPI workloads
- Security tools (AV, EDR) are evaluated for performance impact on EDA workloads before deployment — tools that cause >5% throughput degradation on benchmark workloads require exemption process
- IT standardisation (mandated OS images, approved software lists) accommodates R&D tool requirements — EDA tools often require specific OS versions, kernel parameters, and library versions

---

## RD-P-004: Design Data Has Version History and Is Never Truly Deleted
**Statement:** Engineering design data is versioned, and released/tagged versions are retained permanently (or for the lifetime of the product + regulatory retention period). "Deletion" of active design data requires formal engineering change control.

**Rationale:**
- Patent prosecution requires proof of invention date — design data version history is legal evidence
- Regulatory submissions (FDA, EMA) reference specific design versions — the data must be retrievable during the product's regulatory life
- Trade secret status requires demonstrable access control history — version control provides this
- Reproducibility of research results requires original data and tool versions

**Implications:**
- PLM / design data management systems implement formal check-in/check-out with immutable version history
- "Delete" in PLM means "obsolete" or "archive" — the record remains; only access is restricted
- Archival storage for released designs: minimum product lifecycle + 10 years (longer for medical/pharmaceutical)
- EDA design databases: archived with the exact tool version used to create them (tool version is part of the archive)

---

## RD-P-005: License Server Availability is a Production Constraint
**Statement:** EDA and CAE license server availability is equivalent to production system availability. License server downtime = engineering downtime = project schedule impact. License servers are treated as critical infrastructure.

**Rationale:** All EDA and commercial CAE tools require a license checkout from a license server (FlexLM, Synopsys SCL, Cadence LM-X, Ansys License Manager). If the license server is unavailable, no tool can be launched.

**Implications:**
- License servers are deployed in high-availability pairs (primary + failover)
- License server maintenance requires prior scheduling and engineer notification
- License server infrastructure is on UPS and redundant power
- License server DR: failover to secondary site within 30 minutes
- License utilisation is monitored — insufficient license availability has the same operational impact as a system outage and must be tracked and actioned

---

## RD-P-006: Research Data is Findable, Accessible, Interoperable, Reusable (FAIR)
**Statement:** Research data management follows FAIR principles — not just for open science compliance, but because undiscoverable internal research data leads to duplicated experiments, wasted investment, and patent prosecution risk.

**Rationale:** In large R&D organisations, researchers frequently duplicate experiments because prior results are undiscoverable. FAIR data management pays for itself in avoided duplication.

**Implications:**
- Research data is catalogued in an Electronic Lab Notebook (ELN) or Research Data Management (RDM) platform — not stored only on personal drives
- Metadata standards are defined per research domain (e.g., MIAME for genomics, JCAMP for spectroscopy, OSDP for materials)
- Data is linked to the experiment, researcher, project, and outputs (publications, patents, regulatory submissions)
- At project close: data archived to a managed repository with a persistent identifier; not left on the researcher's laptop

---

## RD-P-007: Digital Thread — From Design to Manufacturing
**Statement:** A digital thread connects R&D design data through validation, through PLM, to manufacturing execution. The thread is maintained without data re-entry and without loss of traceability.

**Rationale:** Manual re-entry of design data between PLM and MES/ERP is a source of quality errors, compliance risk, and inefficiency. The digital thread eliminates these gaps.

**Digital thread elements:**
- CAD model → PLM (BOM, configuration)
- PLM (released BOM) → ERP (procurement, cost)
- PLM (manufacturing BOM) → MES (work instructions, quality plan)
- MES (actuals) → PLM (as-built record)

**Implications:**
- PLM is the system of record for product structure — not ERP, not CAD
- PLM↔ERP and PLM↔MES integrations are designed as system-to-system interfaces, never manual export/import
- Design change control in PLM triggers downstream notifications to ERP and MES automatically
