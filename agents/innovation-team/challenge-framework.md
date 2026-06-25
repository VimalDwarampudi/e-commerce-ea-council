# Red Team Challenge Framework

## Purpose

This framework provides structured challenge prompts the Red Team applies to every council proposal. It is not a checklist to complete mechanically — it is a set of powerful questions. Apply the ones that are relevant; note when you deliberately skip one and why.

---

## Challenge Domain 1: Strategic Coherence

| # | Challenge Question |
|---|---|
| 1.1 | Is this solving the right problem, or is it solving the problem as stated (which may not be the real problem)? |
| 1.2 | Will this still make sense in 3 years if the stated strategy changes? |
| 1.3 | Is this proposal driven by a genuine business need or by technology enthusiasm? |
| 1.4 | Who benefits from this decision and who bears the risk? Are they the same people? |
| 1.5 | Is the organization capable of operating what is being proposed? (Skills, processes, culture) |

---

## Challenge Domain 2: Technical Robustness

| # | Challenge Question |
|---|---|
| 2.1 | What is the single most fragile component in this design? What happens when it fails? |
| 2.2 | Where are the hidden synchronous dependencies that will cascade under load? |
| 2.3 | What is the data consistency model? What does a partial failure leave behind? |
| 2.4 | How does this design behave at 10x expected load? At 0.1x (nearly no traffic)? |
| 2.5 | What is the migration path from the current state? Has it been designed or just assumed? |
| 2.6 | What known technical debt is this design inheriting and not acknowledging? |

---

## Challenge Domain 3: Security & Trust Assumptions

| # | Challenge Question |
|---|---|
| 3.1 | What does an attacker who has compromised one component of this system gain access to? |
| 3.2 | Where is identity verified, and what happens if that verification is compromised? |
| 3.3 | What data does this system expose that it shouldn't in a failure scenario? |
| 3.4 | How would a malicious insider with standard access abuse this system? |
| 3.5 | What is the supply chain risk? Which third-party components, libraries, or vendors are trusted? |

---

## Challenge Domain 4: Operational Assumptions

| # | Challenge Question |
|---|---|
| 4.1 | Who runs this in production in 2 years, and do they exist? |
| 4.2 | What does the on-call runbook look like? Does it exist? Who wrote it? |
| 4.3 | What monitoring alert tells the team this is failing before a user reports it? |
| 4.4 | What does rollback look like, and has it been tested? |
| 4.5 | What manual interventions does this system require periodically? Are they documented? |

---

## Challenge Domain 5: Data & Privacy

| # | Challenge Question |
|---|---|
| 5.1 | What personal data flows through this system that wasn't explicitly called out? |
| 5.2 | If this system is breached, what is the worst-case data exposure? |
| 5.3 | Can personal data be deleted on request? How long does it actually take? |
| 5.4 | Where is data replicated, cached, or logged that creates shadow copies? |
| 5.5 | What does the data look like in 5 years — is the retention policy actually enforceable? |

---

## Challenge Domain 6: Compliance & Regulatory Exposure

| # | Challenge Question |
|---|---|
| 6.1 | What does a GDPR enforcement authority see when they audit this system? |
| 6.2 | What evidence exists that compliance requirements have been met, not just stated? |
| 6.3 | What upcoming regulatory change (NIS2, DORA, EU AI Act timeline) will affect this in 12 months? |
| 6.4 | If the vendor providing a critical component goes bankrupt, what is the compliance impact? |

---

## Challenge Domain 7: Vendor & Commercial Risk

| # | Challenge Question |
|---|---|
| 7.1 | What does it cost to exit this vendor in 3 years, and has that been modelled? |
| 7.2 | What is the concentration risk — how many critical systems depend on this single vendor? |
| 7.3 | What commercial terms give the vendor leverage over the organization in the future? |
| 7.4 | If this vendor raises prices by 40%, what is the realistic alternative? |

---

## Challenge Domain 8: Integration & Ecosystem Impact

| # | Challenge Question |
|---|---|
| 8.1 | What systems will be disrupted that are not in scope for this proposal? |
| 8.2 | What undocumented integrations exist (not in LeanIX) that depend on the systems being changed? |
| 8.3 | Who was not in the room for this decision who should have been? |
| 8.4 | What team will be impacted by this change and hasn't been informed yet? |

---

## Summary Challenge — The Pre-Mortem

Before finalizing the Red Team assessment, run a pre-mortem:

> *Assume it is 18 months from now. This proposal has failed. The organization is dealing with the consequences. What happened?*

Write a brief narrative (3–5 sentences) describing the most plausible failure scenario. This narrative surfaces the most critical finding that all the structured questions may have missed.

```
Pre-Mortem Narrative:
[Write 3–5 sentences describing how and why this proposal failed 18 months from now]

Key implication for the council:
[One sentence — what should change in the proposal based on this scenario]
```
