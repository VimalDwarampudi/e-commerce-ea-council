# 06 — ServiceNow Integration

## Overview

ServiceNow is integrated via its REST Table API, exposed to Copilot Studio agents through **Power Automate flows** acting as action wrappers. This approach provides:
- Clean error handling and response transformation
- OAuth token management abstracted from the agent
- Reusable flows across agents
- Audit logging of all API calls

---

## Authentication Setup

### Step 1: Create OAuth 2.0 Client in ServiceNow

In ServiceNow (Admin → System OAuth → Application Registry):
```
Name: EA Council Copilot Integration
Client ID: [auto-generated]
Client Secret: [store in Azure Key Vault]
Grant Type: Client Credentials
Accessible from: All application scopes
Default Redirect URL: https://global.consent.azure-apim.net/redirect
```

Grant this OAuth client the following roles (minimum):
- `cmdb_read` — read Configuration Items
- `itil` — read incidents and change requests
- `sn_risk.user` — read/write risk records
- `sn_compliance.user` — read/write compliance records
- `change_manager` — create change requests (for write-back)

### Step 2: Store Credentials in Azure Key Vault
```
Secret Name: servicenow-client-id → {client ID value}
Secret Name: servicenow-client-secret → {client secret value}
Secret Name: servicenow-instance-url → https://{instance}.service-now.com
```

### Step 3: Create Power Platform Custom Connector

In Power Platform (Data → Custom Connectors):
```
Name: ServiceNow EA Council
Base URL: https://{instance}.service-now.com
Authentication: OAuth 2.0
  - Authorization URL: https://{instance}.service-now.com/oauth_auth.do
  - Token URL: https://{instance}.service-now.com/oauth_token.do
  - Client ID: [from Key Vault reference]
  - Client Secret: [from Key Vault reference]
  - Scope: useraccount
```

---

## Power Automate Flows (Actions)

Build one Power Automate flow per logical operation. Each flow is exposed as a Copilot Studio Action.

---

### Flow 1: Query CMDB — Get Application CIs

**Action name:** `QueryServiceNowCMDB`  
**Action description:** "Query the ServiceNow CMDB to retrieve Configuration Items (CIs) for applications, infrastructure, and their relationships. Use to understand the current technical landscape for a system."

**Flow logic:**
```
Trigger: Power Apps / Copilot Studio (inputs: applicationName, ciClass)
  ↓
HTTP GET: /api/now/table/cmdb_ci_appl
  params: 
    sysparm_query: name={applicationName}^ORshort_description={applicationName}
    sysparm_fields: name,short_description,install_status,operational_status,
                    business_criticality,owned_by,supported_by,
                    u_leanix_id (custom field linking to LeanIX)
    sysparm_limit: 20
  ↓
Parse JSON response
  ↓
Compose formatted output:
  "CMDB Results for '{applicationName}':
   {for each CI: Name | Status | Criticality | Owner | LeanIX ID}"
  ↓
Return formatted string to Copilot Studio
```

---

### Flow 2: Query GRC — Risk Register

**Action name:** `QueryServiceNowGRC`  
**Action description:** "Query the ServiceNow GRC module to retrieve existing risks, compliance findings, and policy exceptions related to a system or topic."

**Flow logic:**
```
Trigger: Power Apps / Copilot Studio (inputs: searchTerm, riskState)
  ↓
HTTP GET: /api/now/table/sn_risk_risk
  params:
    sysparm_query: short_descriptionLIKE{searchTerm}^state={riskState OR 'open'}
    sysparm_fields: number,short_description,description,risk_rating,
                    state,assigned_to,mitigation,review_date
    sysparm_limit: 10
  ↓
HTTP GET (parallel): /api/now/table/sn_compliance_policy_exception
  params:
    sysparm_query: short_descriptionLIKE{searchTerm}^state=approved
    sysparm_fields: number,short_description,policy,justification,
                    approved_by,expiry_date
    sysparm_limit: 5
  ↓
Compose formatted output combining risks + exceptions
  ↓
Return to Copilot Studio
```

---

### Flow 3: Create Change Request

**Action name:** `CreateServiceNowChangeRequest`  
**Action description:** "Create a ServiceNow Change Request to implement an approved architecture decision. Call this after an ADR is accepted and the Chief Architect has confirmed write-back actions."

**Flow logic:**
```
Trigger: Power Apps / Copilot Studio 
  inputs: adTitle, adDescription, adRationale, affectedSystems, 
          requestedBy, implementationNotes, riskLevel, adrReference
  ↓
HTTP POST: /api/now/table/change_request
  body:
  {
    "short_description": "{adTitle}",
    "description": "{adDescription}\n\nRationale: {adRationale}\n\nADR Reference: {adrReference}",
    "type": "normal",
    "risk": "{riskLevel}",  // low/medium/high/critical
    "impact": "2",
    "urgency": "3",
    "assignment_group": "Enterprise Architecture",
    "requested_by": "{requestedBy}",
    "implementation_plan": "{implementationNotes}",
    "u_adr_reference": "{adrReference}"
  }
  ↓
Parse response → extract CHG number
  ↓
Return: "Change request {CHG-XXXXX} created in ServiceNow. 
         Review at: https://{instance}.service-now.com/nav_to.do?uri=change_request.do?sys_id={sys_id}"
```

---

### Flow 4: Create GRC Risk Record

**Action name:** `CreateServiceNowRisk`  
**Action description:** "Create a new risk record in ServiceNow GRC when an architecture decision identifies a risk that must be formally tracked."

**Flow logic:**
```
Trigger: Power Apps / Copilot Studio
  inputs: riskTitle, riskDescription, probability, impact, 
          riskRating, owner, mitigationPlan, adrReference, reviewDate
  ↓
HTTP POST: /api/now/table/sn_risk_risk
  body:
  {
    "short_description": "{riskTitle}",
    "description": "{riskDescription}\n\nSource ADR: {adrReference}",
    "probability": "{probability}",    // high/medium/low
    "impact": "{impact}",              // high/medium/low
    "risk_rating": "{riskRating}",     // critical/high/medium/low
    "assigned_to": "{owner}",
    "mitigation": "{mitigationPlan}",
    "review_date": "{reviewDate}",
    "state": "open",
    "category": "Technology"
  }
  ↓
Return: "Risk record {RISK-XXXXX} created."
```

---

### Flow 5: Get Incident History for a System

**Action name:** `QueryServiceNowIncidents`  
**Action description:** "Query ServiceNow incident history for a system to inform infrastructure and reliability assessments. Used by Technology & Infrastructure agent."

**Flow logic:**
```
Trigger: Power Apps / Copilot Studio (inputs: systemName, lookbackDays)
  ↓
HTTP GET: /api/now/table/incident
  params:
    sysparm_query: cmdb_ciLIKE{systemName}^resolved_atON{today-lookbackDays}
                   ^ORopened_atON{today-lookbackDays}
    sysparm_fields: number,short_description,priority,state,
                    resolved_at,opened_at,cmdb_ci
    sysparm_orderby: priority
    sysparm_limit: 20
  ↓
Compose summary:
  "Incident history for '{systemName}' (last {lookbackDays} days):
   P1: {count} | P2: {count} | P3: {count}
   Recent: {list of most recent 5}"
  ↓
Return to Copilot Studio
```

---

## Response Formatting Convention

All ServiceNow flows return **plain text strings** formatted for LLM consumption, not raw JSON. This prevents the agent from hallucinating JSON interpretation and keeps context tokens efficient.

Format template:
```
ServiceNow {RecordType} Results:
───────────────────────────────
{Number}: {Short Description}
  Status: {status} | Risk/Priority: {rating} | Owner: {owner}
  Summary: {description truncated to 200 chars}
───────────────────────────────
[{count} records returned. Query: {sysparm_query used}]
```

---

## Error Handling in All Flows

Every flow includes:
```
Scope: Try
  [HTTP call]
  [Parse + format]
Scope: Catch
  Compose error message:
  "ServiceNow query failed. 
   Error: {error code} — {error message}
   The assessment will proceed without this data. 
   Note this as a data gap in the output."
Return error message to Copilot Studio (do not throw — agent handles gracefully)
```

Agents are instructed to treat ServiceNow query failures as data gaps, not errors, and proceed with available information while flagging the gap explicitly.
