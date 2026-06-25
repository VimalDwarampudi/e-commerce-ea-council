# Architecture Decision Record — Template

---

## ADR-[YYYY-NNN]: [Short Title]

**Status:** `PROPOSED` | `ACCEPTED` | `REJECTED` | `SUPERSEDED BY ADR-YYYY-NNN` | `DEPRECATED`  
**Date:** [YYYY-MM-DD]  
**Impact Level:** `Minor` | `Standard` | `Major` | `Critical`  
**Decision Type:** `Strategy` | `Design` | `Review` | `Assessment` | `Decision`  
**Requested By:** [Name / Role / Team]  
**Chief Architect:** [AI Council / Human name if overridden]

---

## 1. Context

> *What is the situation or problem that requires a decision? What forces are at play? Why is this decision needed now?*

[Describe the business or technical context. Reference relevant LeanIX applications, capabilities, or data objects. Reference relevant ServiceNow records if applicable.]

**Key drivers:**
- [Driver 1]
- [Driver 2]

**Constraints:**
- [Constraint 1 — e.g., must integrate with existing SAP S/4HANA]
- [Constraint 2 — e.g., GDPR compliance required; EU data residency]

---

## 2. Decision

> *What is the decision? State it clearly in one or two sentences.*

**We will [do / adopt / retire / migrate / reject] [subject] because [primary rationale].**

---

## 3. Options Considered

### Option A: [Name]
**Description:** [Brief description]  
**Pros:** [List]  
**Cons:** [List]  
**Why not chosen:** [Reason]

### Option B: [Name]
**Description:** [Brief description]  
**Pros:** [List]  
**Cons:** [List]  
**Why not chosen:** [Reason — or "This is the chosen option"]

### Option C: [Name] *(if applicable)*
[same structure]

---

## 4. Rationale

> *Why was the chosen option selected? Which principles and policies drove the decision?*

**Principles applied:**
- [EP-00X: Principle name] — [how it applies]

**Policies cited:**
- [AA-POL-00X / SEC-POL-00X / etc.] — [how it applies]

**Evidence from LeanIX / ServiceNow:**
- [Data point — e.g., "3 applications in Phase Out lifecycle share this capability — consolidation opportunity"]

---

## 5. Council Input

### Agents Consulted
| Agent | Input Summary | Concerns Raised |
|---|---|---|
| Business Architecture | [summary] | [concerns or "None"] |
| Application Architecture | [summary] | [concerns or "None"] |
| Integration Architecture | [summary] | [concerns or "None"] |
| Technology & Infrastructure | [summary] | [concerns or "None"] |
| Data & AI | [summary] | [concerns or "None"] |
| Security Architecture | [summary] | [concerns or "None"] |
| Risk Management & Compliance | [summary] | [concerns or "None"] |
| Red Team | [summary] | [findings or "Not engaged"] |

### Dissenting Views
> *Document any agent that maintained a dissenting position after synthesis.*

[Agent name]: [Their position and why it was not adopted]

### Veto or Escalation
- Security veto issued: `YES` / `NO`
- Human escalation required: `YES` / `NO`
- Escalation outcome: [description if applicable]

---

## 6. Trade-offs and Accepted Risks

> *What are we accepting or giving up with this decision?*

| Trade-off | Accepted? | Mitigation |
|---|---|---|
| [e.g., Vendor lock-in on Azure Event Hubs] | YES | Exit strategy documented in connectors/servicenow-apis.md |
| [e.g., Higher initial implementation cost vs Option B] | YES | Lower TCO over 3 years offsets initial investment |

**Accepted Risks:**
| Risk | Rating | Owner | Mitigation | ServiceNow Risk ID |
|---|---|---|---|---|
| [Risk description] | HIGH / MED / LOW | [Role] | [Mitigation] | [RISK-XXXX or TBD] |

---

## 7. Implications

### LeanIX Updates Required
- [ ] Application lifecycle state change: [App name] → [New state]
- [ ] New Interface record: [Source] → [Target] via [protocol]
- [ ] Technology radar position update: [Technology] → [Ring]
- [ ] New Data Object record: [name]

### ServiceNow Updates Required
- [ ] Change request created: [CHG-XXXXX or TBD]
- [ ] CMDB CI updates: [description]
- [ ] Risk register entry: [RISK-XXXXX or TBD]
- [ ] Policy exception logged: [POL-EXC-XXXXX or TBD]

### Downstream Architecture Impacts
- [System or team that will be affected and how]

---

## 8. Next Steps

| Action | Owner | Due Date | Success Criterion |
|---|---|---|---|
| [Action 1] | [Role / Team] | [Date] | [How do we know it's done?] |
| [Action 2] | [Role / Team] | [Date] | [How do we know it's done?] |

---

## 9. Review

**Next review date:** [Date — typically 6–12 months; sooner if conditions change]  
**Review trigger:** [Event that would require earlier review — e.g., vendor end-of-support, regulatory change]
