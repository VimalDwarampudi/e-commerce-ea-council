# ServiceNow API Reference — EA Council

## Overview

All ServiceNow interactions are wrapped in Power Automate flows (see `copilot-studio/06-servicenow-integration.md`). This document provides the raw API reference for development, debugging, and direct use.

**Base URL:** `https://{instance}.service-now.com`  
**Authentication:** OAuth 2.0 Bearer token  
**Content-Type:** `application/json`  
**Response format:** `application/json`  
**API version:** Table API (stable across ServiceNow versions)

---

## 1. CMDB — Application Configuration Items

### GET: Find application CIs by name
```http
GET /api/now/table/cmdb_ci_appl
  ?sysparm_query=nameLIKE{searchTerm}^ORshort_descriptionLIKE{searchTerm}
  &sysparm_fields=sys_id,name,short_description,install_status,operational_status,
                  business_criticality,owned_by,supported_by,
                  u_leanix_id,used_for,version
  &sysparm_limit=20
  &sysparm_display_value=true
```

**Response fields:**
| Field | Description |
|---|---|
| `sys_id` | Unique ServiceNow identifier |
| `name` | CI name |
| `install_status` | Installed / In Test / On Order / Absent |
| `operational_status` | Operational / Non-Operational / Repair In Progress |
| `business_criticality` | 1-Critical / 2-High / 3-Medium / 4-Low |
| `owned_by` | Application owner |
| `supported_by` | Support group |
| `u_leanix_id` | Custom field: linked LeanIX Application ID |

---

### GET: CI relationships (dependencies)
```http
GET /api/now/table/cmdb_rel_ci
  ?sysparm_query=parent.name={applicationName}^ORchild.name={applicationName}
  &sysparm_fields=parent.name,child.name,type.name,port
  &sysparm_display_value=true
  &sysparm_limit=50
```

---

## 2. CMDB — Infrastructure CIs

### GET: Servers, VMs, Cloud Instances
```http
GET /api/now/table/cmdb_ci_server
  ?sysparm_query=nameLIKE{searchTerm}^operational_status=1
  &sysparm_fields=sys_id,name,short_description,os,os_version,
                  virtual,cloud_provider,region,fqdn,
                  business_criticality,owned_by,supported_by
  &sysparm_limit=20
  &sysparm_display_value=true
```

### GET: Cloud service instances
```http
GET /api/now/table/cmdb_ci_cloud_service_account
  ?sysparm_query=nameLIKE{searchTerm}
  &sysparm_fields=sys_id,name,provider,account_id,region,status
  &sysparm_display_value=true
```

---

## 3. Change Management

### GET: Change requests for a system
```http
GET /api/now/table/change_request
  ?sysparm_query=cmdb_ciLIKE{systemName}^stateNOT IN6,4
  &sysparm_fields=number,short_description,state,priority,risk,
                  requested_by,assigned_to,start_date,end_date,
                  u_adr_reference
  &sysparm_orderby=start_date
  &sysparm_limit=10
  &sysparm_display_value=true
```

**State values:** 1=New, 2=Assess, 3=Authorize, 4=Scheduled, 5=Implement, 6=Review, 7=Closed

### POST: Create a change request
```http
POST /api/now/table/change_request
Content-Type: application/json

{
  "short_description": "{title}",
  "description": "{full description}\n\nADR Reference: {adr_id}",
  "type": "normal",
  "risk": "{low|medium|high|critical}",
  "impact": "2",
  "urgency": "3",
  "priority": "3",
  "category": "Software",
  "assignment_group": "Enterprise Architecture",
  "requested_by": "{user_sys_id_or_email}",
  "implementation_plan": "{implementation notes}",
  "backout_plan": "{rollback plan}",
  "test_plan": "{test approach}",
  "u_adr_reference": "{ADR-YYYY-NNN}"
}
```

**Response:** Returns the created record including `number` (CHG-XXXXX) and `sys_id`.

---

## 4. GRC — Risk Register

### GET: Risks by search term or application
```http
GET /api/now/table/sn_risk_risk
  ?sysparm_query=short_descriptionLIKE{searchTerm}^state!=closed
  &sysparm_fields=number,short_description,description,risk_rating,
                  state,assigned_to,mitigation,review_date,
                  category,source,affected_systems
  &sysparm_orderby=risk_rating
  &sysparm_limit=10
  &sysparm_display_value=true
```

**Risk rating values:** `critical` / `high` / `medium` / `low`

### POST: Create a risk record
```http
POST /api/now/table/sn_risk_risk
Content-Type: application/json

{
  "short_description": "{risk title}",
  "description": "{full description}\n\nSource ADR: {adr_id}",
  "probability": "{high|medium|low}",
  "impact": "{high|medium|low}",
  "risk_rating": "{critical|high|medium|low}",
  "assigned_to": "{owner email or sys_id}",
  "mitigation": "{mitigation plan}",
  "review_date": "{YYYY-MM-DD}",
  "state": "open",
  "category": "Technology",
  "source": "Enterprise Architecture Council"
}
```

---

## 5. GRC — Policy Exceptions

### GET: Active policy exceptions
```http
GET /api/now/table/sn_compliance_policy_exception
  ?sysparm_query=short_descriptionLIKE{searchTerm}^state=approved
  &sysparm_fields=number,short_description,policy,justification,
                  approved_by,expiry_date,state,compensating_controls
  &sysparm_display_value=true
  &sysparm_limit=10
```

### POST: Log a new policy exception
```http
POST /api/now/table/sn_compliance_policy_exception
Content-Type: application/json

{
  "short_description": "{exception title}",
  "description": "{business justification}",
  "policy": "{policy ID — e.g., SEC-POL-001}",
  "justification": "{detailed justification}",
  "compensating_controls": "{alternative controls in place}",
  "expiry_date": "{YYYY-MM-DD}",
  "state": "requested",
  "requested_by": "{requestor}"
}
```

---

## 6. Incident History

### GET: Incidents for a system (operational risk data)
```http
GET /api/now/table/incident
  ?sysparm_query=cmdb_ciLIKE{systemName}^opened_atON{lookbackPeriod}
  &sysparm_fields=number,short_description,priority,state,
                  opened_at,resolved_at,cmdb_ci,category,
                  close_code,resolution_notes
  &sysparm_orderby=priority
  &sysparm_limit=20
  &sysparm_display_value=true
```

**Priority values:** 1=Critical / 2=High / 3=Moderate / 4=Low

**Lookback period format:** `javascript:gs.beginningOfLast30Days()` or date range:
```
opened_at>=2026-01-01^opened_at<=2026-03-23
```

---

## 7. CMDB — Relationships for Dependency Mapping

### GET: All downstream dependencies of an application
```http
GET /api/now/table/cmdb_rel_ci
  ?sysparm_query=parent.sys_class_name=cmdb_ci_appl^parent.name={applicationName}
  &sysparm_fields=parent.name,child.name,child.sys_class_name,
                  type.name,port,connection_type
  &sysparm_display_value=true
  &sysparm_limit=50
```

---

## Error Handling Reference

| HTTP Status | Meaning | Agent Response |
|---|---|---|
| `200 OK` | Success | Process response |
| `400 Bad Request` | Invalid query syntax | Log query; report as data gap |
| `401 Unauthorized` | Token expired | Retry with refreshed token (handled by Power Automate) |
| `403 Forbidden` | Insufficient role | Report as access gap; flag to IT admin |
| `404 Not Found` | Record or table not found | Report as data gap |
| `429 Too Many Requests` | Rate limit hit | Retry after `Retry-After` header delay |
| `500 Server Error` | ServiceNow issue | Report outage; proceed without this data |

---

## Query Conventions for Agents

1. **Always use `sysparm_display_value=true`** — returns human-readable labels instead of numeric codes.
2. **Limit results** — use `sysparm_limit` to avoid context overload. 10–20 records is sufficient for most queries.
3. **Cite record numbers** — always include the ServiceNow number (CHG-, RISK-, INC-) when referencing records.
4. **Handle zero results explicitly** — if no records found, state: "No ServiceNow records found for this query. This may indicate undocumented risk or an incomplete CMDB."
5. **Never write without confirmation** — POST/PATCH operations (creating change requests, risks) are only triggered after ADR is ACCEPTED and the human confirms write-back via the Adaptive Card button.
