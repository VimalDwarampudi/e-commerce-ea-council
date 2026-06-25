# R&D & EDA Architecture Guidelines

## How to Assess an R&D or EDA Architecture Proposal

### Step 1: Identify the R&D Stage and IP Context
- Where in the R&D lifecycle does this sit? (Discovery → Research → Development → Design → Verification → Transfer)
- What IP is involved — unpublished research, pre-patent designs, filed patents, trade secrets, licensed-in technology?
- What is the sensitivity level? Use RD-POL-007 classification table.

### Step 2: Export Control Check (mandatory)
Answer before proceeding:
- Is any data involved subject to ITAR, EAR, or EU Dual-Use controls?
- Does the proposal change who can access export-controlled data or systems?
- Does it involve a cloud platform, external partner, or new geographical location for the data?

If any answer is YES: flag to Export Control Officer and do not approve until ECO assessment is complete (RD-POL-001, RD-POL-002).

### Step 3: Performance Requirements Assessment
For EDA, CAE, or HPC proposals:
- What is the compute job profile? (memory-bound, CPU-bound, GPU, MPI parallel?)
- What are the storage throughput requirements? (EDA layouts: TB-scale, high random IOPS)
- What is the licence consumption pattern? (peak concurrent users, token burn rate)
- Has a capacity sizing exercise been done, or is this a rough estimate?

### Step 4: Tool Compatibility Check
- Which EDA/CAE tools are in scope?
- Are they certified on the proposed OS, kernel version, and storage platform?
- Have EDA/CAE tool vendors been consulted?
- Are license server changes required?

### Step 5: Data Architecture and Retention
- Where does the data live today, and where will it live after the change?
- Is version control and immutable audit trail in place?
- What is the retention requirement? (patent prosecution, regulatory, product lifecycle?)
- Is reproducibility guaranteed — can you re-run a simulation from 5 years ago?

### Step 6: PLM and Digital Thread
- Does the proposal affect the PLM system or design data management?
- Is the PLM system of record (RD-POL-003) maintained?
- Does the proposal preserve the digital thread (design → PLM → ERP → MES)?
- Are BOM structures affected? If yes, involve Integration Architecture for PLM↔ERP interface.

### Step 7: Regulatory Impact (for regulated R&D)
- Is this a GLP, GCP, or GxP environment?
- Is a computer system validation required or does an existing validation need updating?
- Are electronic records or signatures involved? (21 CFR Part 11 / EU Annex 11)

---

## EDA Infrastructure Reference

### On-Premises EDA Cluster (standard pattern)

```
┌──────────────────────────────────────────────────────────┐
│                    EDA COMPUTE CLUSTER                    │
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  Interactive  │  │  Batch Sim  │  │  Verification │   │
│  │  Design Wkst  │  │  Farm (CPU)  │  │  Farm (CPU/  │   │
│  │  (GPU-enabled │  │  100–500 cores│  │  GPU)        │   │
│  │  for layout)  │  └──────┬───────┘  └──────┬───────┘   │
│  └──────┬────────┘         │                 │           │
│         │      ┌────────────────────────────┘            │
│         └──────▼──────────────────────────────┐          │
│              JOB SCHEDULER (Slurm / LSF)       │          │
│         ┌─────────────────────────────────────┘          │
│         ▼                                                 │
│  ┌──────────────────────────────────────────────┐        │
│  │  HIGH-PERF STORAGE (Lustre / WEKA / GPFS)    │        │
│  │  /home (NFS) + /project (parallel FS)        │        │
│  │  /scratch (fast ephemeral, auto-purge 30d)   │        │
│  └──────────────────────────────────────────────┘        │
│                                                           │
│  ┌──────────────────────────────────────────────┐        │
│  │  LICENSE SERVERS (Primary + Standby HA pair) │        │
│  │  Cadence LM-X │ Synopsys SCL │ Ansys LM      │        │
│  └──────────────────────────────────────────────┘        │
└──────────────────────────────────────────────────────────┘
          │                           │
          ▼                           ▼
  ┌───────────────┐         ┌──────────────────┐
  │  Design DM    │         │  ELN / Research  │
  │  (DesignSync/ │         │  Data Mgmt       │
  │  Perforce)    │         │  (Benchling/     │
  └───────────────┘         │  eLabNext)       │
                            └──────────────────┘
```

### Storage Sizing Rules of Thumb for EDA
| Design Size | Active Project Storage | Simulation Scratch | Archive |
|---|---|---|---|
| Small SoC (< 50M gates) | 2–5 TB/project | 10–20 TB/project | 1–3 TB released |
| Mid-size SoC (50–500M gates) | 10–30 TB/project | 50–100 TB/project | 5–15 TB released |
| Large SoC / SiP (> 500M gates) | 50–200 TB/project | 200–500 TB/project | 20–100 TB released |
| Verification (formal + sim) | Adds 2–5× simulation storage | — | — |

**Storage performance requirements:**
- Layout tool scratch: > 5 GB/s sequential; > 500K IOPS random
- Simulation farm: > 2 GB/s per 100 cores aggregate
- Archive: cost-optimised (NFS-backed or object storage); latency-tolerant

### License Sizing Guidelines
| Tool Category | Concurrent Licenses | Burst Headroom |
|---|---|---|
| Logic simulation (Xcelium, VCS) | 1 license per 2 engineers (sharing model) | +30% for tape-out rush |
| Synthesis (Genus, Design Compiler) | 1 license per 3 engineers | +50% for closure runs |
| Place & Route (Innovus, ICC2) | 1 license per 2 engineers | +30% for signoff |
| Formal verification (JasperGold, VC Formal) | 1 license per 3 engineers | +20% |
| Signoff (Voltus, StarRC, PrimeTime) | 1 license per 2 engineers | +50% for tapeout |

---

## Cloud Bursting for EDA (hybrid model)

When on-premises capacity is insufficient during peak demand (tape-out rushes):

**Allowed:** Cloud burst for **non-export-controlled** EDA workloads (standard commercial IP):
```
On-premises Slurm head node → Cloud (Azure CycleCloud / AWS ParallelCluster)
  - Job dispatched to cloud compute nodes
  - Design data staged to cloud storage bucket (encrypted, dedicated tenant)
  - Results pulled back to on-premises after job completion
  - Cloud storage purged after results confirmed
```

**Prohibited without ECO approval:** Cloud burst of ITAR/EAR-controlled design data.

**Technical controls for cloud burst:**
- Dedicated cloud subscription / account (not shared with other workloads)
- Storage encryption with customer-managed keys
- No cloud admin access to design data directories (access control enforced via ACLs and CMK)
- Cloud compute nodes are ephemeral — no persistent storage of EDA data
- Audit log of all data staged to and from cloud

---

## PLM Architecture Reference

### PLM in the Digital Thread

```
                      ┌──────────────────────┐
                      │    PLM SYSTEM         │
                      │  (Teamcenter /        │
                      │   Windchill /         │
                      │   Enovia)             │
                      │                       │
                      │ • eBOM                │
                      │ • mBOM                │
                      │ • CAD models          │
                      │ • Specs & drawings    │
                      │ • ECO/ECN process     │
                      │ • Config management   │
                      └──┬──────────────┬─────┘
                         │              │
              ┌──────────▼──┐      ┌────▼──────────┐
              │    ERP       │      │    MES / MOM   │
              │  (SAP S/4)   │      │  (production)  │
              │              │      │                │
              │  Receives    │      │  Receives mBOM │
              │  mBOM for    │      │  work instruc- │
              │  procurement │      │  tions, quality│
              │  & costing   │      │  plans         │
              └──────────────┘      └────────────────┘
```

**Integration patterns:**
- PLM → ERP: mBOM release triggers ERP material master creation (via Integration Platform — not direct DB link)
- ERP → PLM: Cost data fed back to PLM for design-to-cost analysis
- PLM → MES: Work instruction and quality plan released with mBOM; MES acknowledges

**PLM data governance:**
- PLM administrator manages structure — not individuals
- Released items are locked — only accessible via formal ECO process
- Lifecycle states: In Work → In Review → Released → Obsolete

---

## Research Data Management Reference

### FAIR Data Implementation for R&D

| FAIR Principle | Technical Implementation |
|---|---|
| **Findable** | All datasets in ELN/LIMS with metadata; searchable via data catalog (Purview / Collibra) |
| **Accessible** | Authenticated API access to archived datasets; no "lost on laptop" data |
| **Interoperable** | Domain metadata standards (MIAME, JCAMP, SDF, CIF, OSDP) used for structured data types |
| **Reusable** | Data accompanied by provenance (instrument, method, analyst, date); license stated (internal/restricted) |

### ELN Selection Criteria
| Criterion | Requirement |
|---|---|
| Regulatory | 21 CFR Part 11 / EU Annex 11 compliance if GLP/GCP environment |
| IP | Timestamping with cryptographic integrity; no editing without audit trail |
| Integration | API integration with LIMS, PLM, and research data repository |
| Export control | Access control by user nationality enforceable |
| Formats | Supports structured data (JCAMP, SDF, images, NMR, sequences) |
| Search | Full-text search across entries; structured metadata search |
