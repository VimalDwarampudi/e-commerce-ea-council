# Example: Red Team Assessment — CRM Migration to Dynamics 365

## Input (Council Output Summary)

> The council has proposed migrating from Siebel CRM to Dynamics 365 Sales. Domain agents reached consensus: strategically aligned, portfolio redundancy addressed, integration pattern selected (Service Bus + Logic Apps), infrastructure on Azure App Service, DPIA identified by Risk & Compliance. Security raised OAuth requirement (addressed in revised proposal). Overall council confidence appeared HIGH.

## Output (Red Team Assessment)

## Red Team Assessment

### Confidence Rating
**MEDIUM** — The council has done solid work and addressed the obvious risks. However, consensus among all agents is itself a risk signal. The proposal is well-framed but several assumptions are unvalidated and the operational reality has not been stress-tested.

---

### Top Findings

#### Finding 1: 8 Years of CRM Data — No Quality Assessment Has Been Done
**Type:** Assumption / Data Risk  
**Severity:** HIGH  
**Finding:** Business Architecture mentioned "data quality issues are known but unquantified." The integration design assumes a clean bidirectional sync between Dynamics 365 and SAP using customer ID as the cross-reference key. No one has confirmed whether 8 years of Siebel data has consistent, unique, valid customer IDs that map cleanly to SAP business partner numbers.  
**Evidence:** In every legacy CRM migration the EA Council has reviewed, data quality is underestimated. Duplicate customers, inconsistent IDs, and unmapped SAP relationships typically add 3–6 months to migrations when discovered late.  
**Implication:** If customer IDs don't map cleanly to SAP BPs, the bidirectional sync breaks at launch. The integration architecture assumes a mapping table — but who populates it and how has not been designed.  
**Suggested Response:** Make the data quality assessment a **gate** before integration architecture is finalised. Do not design the sync until you know the mapping completeness.

---

#### Finding 2: Greenhouse Retention Creates a Three-System Recruiting Landscape
**Type:** Simplicity Challenge / Future Complexity  
**Severity:** MEDIUM  
**Finding:** Business Architecture recommended retaining Greenhouse for Phase 1 and revisiting in 12 months. Application Architecture agreed. This is pragmatic — but in practice, "revisit in 12 months" almost never happens. The council has just locked in a three-system recruiting landscape: Greenhouse (recruiting), SuccessFactors (HR core), Dynamics 365 (CRM/Sales contacts) — each with a candidate/contact data model. Who owns the candidate record? When does a candidate become a customer contact?  
**Evidence:** The "Phase 2 review" in the ADR has no owner, no success criteria, and no trigger. Without these, it will not happen.  
**Implication:** In 3 years, we will have three systems with overlapping contact/candidate data and no clear system of record.  
**Suggested Response:** Add to the ADR: a named owner for the Phase 2 Greenhouse review, a trigger condition (not just "12 months"), and a definition of what "system of record for recruiting contacts" means.

---

#### Finding 3: The SAP Integration Is on the Critical Path With No Fallback
**Type:** Failure Mode / Operational  
**Severity:** HIGH  
**Finding:** The Quote-to-Order flow (Dynamics → Logic Apps → SAP S/4HANA) is synchronous and on the critical path for the sales process. Integration Architecture proposed a circuit breaker — but the proposal does not define what happens when the circuit is open. Do salespeople know SAP is unreachable? Can they still close a deal? Does the order queue automatically retry, or does it silently fail?  
**Evidence:** Circuit breakers prevent cascading failure but they don't solve the business process. "Graceful degradation" must be designed, not assumed.  
**Implication:** First time SAP goes down for maintenance (every weekend, typically), salespeople will get a mysterious error and call the helpdesk. This is predictable and should be designed for.  
**Suggested Response:** Define the circuit-open UX: user sees "Order submitted — will be processed when SAP is available" + automatic retry queue with status notification. This is a design requirement, not an operational concern.

---

#### Finding 4: Change Management Budget Is Invisible in the ADR
**Type:** Assumption / Operational  
**Severity:** MEDIUM  
**Finding:** Business Architecture listed user adoption as a MEDIUM risk and stated "change management and training investment is critical — not optional." The ADR records this as a condition. But the change management budget is not in the cost estimate, there is no named change manager, and there is no training plan.  
**Evidence:** CRM migrations have the highest user adoption failure rate of any enterprise application category. Sales teams that don't use the CRM make the data worthless — which makes the integration worthless — which makes the whole investment worthless.  
**Implication:** The technical architecture succeeds and the project still fails because sales reps keep using spreadsheets.  
**Suggested Response:** Add to next steps: "Appoint change manager and define training budget before project kick-off." Make this a Project Approval gate, not an afterthought.

---

#### Finding 5: HubSpot Was Flagged But Not Resolved
**Type:** Assumption / Scope  
**Severity:** MEDIUM  
**Finding:** Business Architecture flagged HubSpot (marketing automation) as a potential overlap/boundary concern and said "confirm scope boundary between CRM and marketing automation." This was noted but not actioned. The integration architecture has no mention of HubSpot.  
**Evidence:** Marketing teams run campaigns in HubSpot against contact records. Those contact records will now live in Dynamics 365. If there's no Dynamics 365 ↔ HubSpot sync, marketing is running campaigns against stale data within 30 days of Dynamics 365 going live.  
**Implication:** A fourth integration requirement has been missed from scope.  
**Suggested Response:** Add HubSpot boundary definition to the ADR scope section before acceptance. Either: (a) define the HubSpot ↔ Dynamics 365 integration as in scope, or (b) explicitly exclude it and describe how marketing will access contact data.

---

### Assumption Audit

| Assumption | Status | Risk if Wrong |
|---|---|---|
| Customer IDs in Siebel map cleanly to SAP BP numbers | **UNVALIDATED** | Integration sync fails at launch; 3–6 month remediation |
| Sales team will adopt Dynamics 365 with training | UNVALIDATED | Data quality degrades; integration value lost |
| Greenhouse Phase 2 review will happen in 12 months | **QUESTIONABLE** — no owner or trigger | Three-system data fragmentation solidifies permanently |
| SAP is available during business hours for synchronous orders | VALIDATED (SAP SLA exists) | Circuit-open UX still needed for maintenance windows |
| HubSpot scope is out of this project | **UNVALIDATED** — never confirmed | Missing integration discovered post-launch |

### Simplicity Challenge
**Is there a simpler path?** Partially. The bidirectional customer master sync via Service Bus is the right pattern — no simpler alternative. However, the Quote-to-Order flow could use **async with a short SLA** rather than synchronous — this removes the circuit breaker complexity and the "SAP down" UX problem. Salespeople submit the order; it processes within 2 minutes and they get a Teams notification with the SAP order number. Recommend Integration Architecture re-evaluate this.

### Pre-Mortem
*It is 18 months after Dynamics 365 go-live. The project has "failed" in the sense that sales leadership is asking to roll back or replace it. What happened?*

The data migration underestimated duplicate customer records — 15% of Siebel customers had no clean SAP mapping. The sync created duplicate accounts in Dynamics 365 within the first week. Sales reps lost trust in the data immediately. The helpdesk was overwhelmed. IT spent 3 months on data remediation while the sales team continued using Siebel in parallel. By month 6, the organisation was running two CRM systems simultaneously with no clear owner. Change management had no budget and no dedicated resource. The project manager was the de facto change manager, which meant it wasn't managed at all.

**Key implication:** The data quality assessment is not a nice-to-have pre-work item. It is the make-or-break dependency of this entire programme. Do it before anything else.

## Key Points Illustrated
- Consensus (all agents agreed) prompted increased scrutiny, not less
- Every finding is evidence-based with a historical pattern or logical consequence
- Red Team does not redesign — it surfaces the problem, suggests where to look
- Assumption audit explicitly marks UNVALIDATED vs VALIDATED
- Pre-mortem names the most likely failure narrative concisely
- Confidence is MEDIUM, not LOW — the council did good work; specific gaps found
