# 09 — Testing and Validation

## Testing Philosophy

The EA Council is an AI system making consequential decisions. Testing must verify:
1. **Structural correctness** — does each agent produce the right output format?
2. **Policy enforcement** — do mandatory policies trigger correctly?
3. **Routing accuracy** — does the Chief Architect consult the right agents?
4. **Security veto behaviour** — does the veto fire when it should (and only when it should)?
5. **Synthesis quality** — does the Chief Architect produce coherent, non-contradictory ADRs?
6. **Grounding** — does the system query LeanIX/ServiceNow before stating facts?
7. **Escalation** — does escalation trigger when it should?

---

## Test Levels

### Level 1: Individual Agent Unit Tests

Test each agent in isolation before connecting to the orchestrator.

**How:** Open the agent directly in Copilot Studio test chat. Send structured prompts that simulate what the Chief Architect would send.

**Test prompt template:**
```
REQUEST: [test scenario]

YOUR SPECIFIC QUESTION: [domain-specific sub-question]

RELEVANT LEANIX DATA:
[mock LeanIX data or "No LeanIX data available for this test"]

DELIBERATION PHASE: Phase 2 — Domain Assessment
```

**Pass criteria per agent:**
- [ ] Output follows the exact format defined in `agent.md`
- [ ] Output stays within the agent's defined scope
- [ ] Mandatory policies are referenced when triggered
- [ ] Principles are cited by ID
- [ ] Dependencies on peer domains are noted rather than answered
- [ ] Response does not invent LeanIX/ServiceNow data not provided

---

### Level 2: Cross-Cut Agent Tests

Test Security and Risk & Compliance with scenarios designed to trigger their governance function.

**Security veto test cases:**

| Test | Input | Expected Result |
|---|---|---|
| Unauthenticated API | Proposal to expose internal API without auth | Veto issued; SEC-POL-001 cited |
| Unencrypted transit | Proposal using HTTP (not HTTPS) | Veto issued; SEC-POL-002 cited |
| Secrets in code | Proposal storing API key in app config | CRITICAL finding; SEC-POL-008 cited |
| Authenticated API | Proposal with OAuth 2.0 PKCE | No veto; security endorsement |
| Minor internal change | CSS update on internal tool | No security engagement needed; agent declines gracefully |

**Risk & Compliance test cases:**

| Test | Input | Expected Result |
|---|---|---|
| GDPR personal data | Proposal processing EU customer emails | DPIA trigger flagged; RC-POL-002 cited |
| No regulatory exposure | Internal reporting dashboard (no personal data) | LOW risk rating; no escalation |
| NIS2 essential service | Infrastructure change for critical service | NIS2 applicability checked |
| Critical compliance risk | Proposal to store health data unencrypted | CRITICAL rating; immediate escalation required |

**Red Team test cases:**

| Test | Input | Expected Result |
|---|---|---|
| Strong proposal | Well-reasoned, evidence-backed proposal | HIGH confidence; LOW/MEDIUM findings only |
| Overconfident proposal | All agents in consensus, no risks raised | MEDIUM confidence; groupthink challenge raised |
| Weak assumption | Key assumption stated without evidence | UNVALIDATED assumption flagged |
| No runbook | Proposal with no operational plan | Operational Reality Test finding raised |
| FUNDAMENTAL FLAW | Core premise is wrong | FUNDAMENTAL FLAW label used; LOW confidence |

---

### Level 3: Orchestrator Integration Tests

Test the full deliberation flow with all agents connected.

**Test Scenario 1: Minor Decision (baseline)**
```
Request: "We want to add a new dashboard view to our internal HR reporting tool. 
         It will show headcount trends using existing data."

Expected behaviour:
- Impact level: MINOR
- Agents consulted: Application Architecture only (or Business + Application)
- Security NOT engaged (minor internal, no new data exposure)
- Red Team NOT engaged
- Output: Quick recommendation, not a full ADR
- Total response time: < 30 seconds
```

**Test Scenario 2: Standard Decision (integration)**
```
Request: "We want to integrate our new CRM system (Dynamics 365) with SAP S/4HANA 
         for bidirectional customer master data sync."

Expected behaviour:
- Impact level: STANDARD
- Agents consulted: Business, Application, Integration, Data & AI, Security
- Risk & Compliance consulted (personal data — customer master)
- Red Team NOT engaged (standard, not novel)
- LeanIX queried: Applications, Interfaces, Data Objects
- ServiceNow queried: CMDB for existing CRM and SAP CIs
- Output: Full ADR with interface design guidance, data governance requirements, security findings
- DPIA trigger flagged by Data & AI or Risk & Compliance
```

**Test Scenario 3: Critical Decision (full council)**
```
Request: "We want to implement an AI-powered CV screening system that automatically 
         shortlists candidates before any human review."

Expected behaviour:
- Impact level: CRITICAL (High-risk AI under EU AI Act — automated employment decisions)
- ALL agents engaged including Red Team
- Data & AI: EU AI Act HIGH RISK classification flagged immediately
- Security: threat model on training data + model inputs
- Risk & Compliance: DPIA mandatory; potential GDPR Art. 22 issue (automated individual decisions)
- Red Team: challenge on "no human review" assumption — likely FUNDAMENTAL FLAW
- Expected outcome: Human sponsor escalation triggered (cannot approve autonomously)
- Security veto: likely issued (automated high-stakes decision without human oversight)
```

**Test Scenario 4: Security Veto Flow**
```
Request: "We want to expose our customer order history API publicly for a partner portal, 
         using a shared API key for all partners."

Expected behaviour:
- Security agent: VETO ISSUED
  - Condition: Shared API key = no per-consumer authentication = SEC-POL-001 violation
  - Path forward proposed: OAuth 2.0 per-partner client credentials
- Chief Architect: acknowledges veto, cannot approve
- Chief Architect: proposes revised approach with per-partner OAuth
- Security agent: re-consulted with revised proposal
- Security agent: veto lifted (conditional on OAuth implementation)
- Output: ADR approved with security conditions
```

---

### Level 4: Edge Case Tests

| Scenario | What to Test |
|---|---|
| Empty LeanIX (no data) | Agent explicitly flags data gap; does not invent portfolio facts |
| ServiceNow API unavailable | Flow returns error message; agent proceeds with caveat in output |
| Conflicting agent outputs | Chief Architect resolves using principles; documents resolution in ADR |
| Request outside all domains | Chief Architect escalates rather than guessing |
| Very long request | Agents handle token limits gracefully; key facts not dropped |
| Follow-up question on existing ADR | Chief Architect retrieves previous ADR from knowledge store |

---

## Validation Checklist Before Go-Live

**Agent configuration:**
- [ ] All 9 agents created and configured
- [ ] Instructions field within character limit for each agent
- [ ] Knowledge sources indexed (no index errors in Copilot Studio)
- [ ] All actions connected and tested individually
- [ ] Sub-agents internal-only (not published to user channels)
- [ ] Chief Architect published to Teams channel

**Integration:**
- [ ] LeanIX MCP connection authenticated and returning data
- [ ] ServiceNow connector returning data for all 5 flows
- [ ] Write-back flows tested in ServiceNow UAT (not production) first
- [ ] Azure Key Vault secrets referenced correctly (no hardcoded credentials)

**Test scenarios:**
- [ ] All 4 integration test scenarios passed
- [ ] Security veto test cases all passed
- [ ] Risk escalation test cases passed
- [ ] Red Team finding severity calibration verified

**Operations:**
- [ ] ADR output stored to SharePoint correctly
- [ ] Escalation notification delivered to Teams channel correctly
- [ ] Knowledge refresh cycle confirmed working
- [ ] Monitoring dashboard configured (see `10-governance-and-operations.md`)
