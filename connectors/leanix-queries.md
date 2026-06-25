# LeanIX MCP Queries — Reference Guide

## Purpose

Pre-built queries that agents can invoke via the LeanIX MCP connection. Each query includes the purpose, which agents use it, the MCP tool call, and an example of expected output structure.

When using the MCP server, agents call these as tools. When using the GraphQL API directly (fallback), the raw queries are provided.

---

## Query 1: Application Portfolio Overview

**Purpose:** Get the full application portfolio filtered by lifecycle state, business unit, or criticality.  
**Used by:** Application Architecture, Business Architecture, Chief Architect

**MCP tool call:**
```
Tool: list_applications
Parameters:
  filter:
    lifecycleState: ["active", "phaseOut", "endOfLife", "plan"]
    businessUnit: "{optional — filter by BU}"
  fields: [name, lifecycle, businessCriticality, technicalFit, functionalFit, 
           businessOwner, technicalOwner, description]
  sort: businessCriticality DESC
  limit: 100
```

**GraphQL equivalent:**
```graphql
{
  allFactSheets(
    filter: {
      facetFilters: [
        { facetKey: "FactSheetTypes", keys: ["Application"] }
        { facetKey: "lifecycle", keys: ["active", "phaseOut", "endOfLife", "plan"] }
      ]
    }
    sort: { mode: BY_FIELD, key: "businessCriticality", order: desc }
    first: 100
  ) {
    edges {
      node {
        id
        name
        displayName
        type
        ... on Application {
          lifecycle { asString phases { phase startDate } }
          businessCriticality
          technicalFit
          functionalFit
          description
          relApplicationToBusinessCapability { edges { node { factSheet { name } } } }
          relApplicationToITComponent { edges { node { factSheet { name } } } }
        }
      }
    }
  }
}
```

**Expected output structure:**
```
Application: HR Recruitment Portal
  Lifecycle: Active (since 2021-06-01)
  Business Criticality: HIGH
  Technical Fit: 3/5
  Functional Fit: 4/5
  Business Owner: Jane Smith
  Technical Owner: Bob Lee
  Business Capabilities: Talent Acquisition, Employee Onboarding
  IT Components: Azure App Service, Azure SQL, Entra ID
```

---

## Query 2: Applications by Business Capability

**Purpose:** Find all applications serving a specific business capability — used for redundancy detection and rationalization.  
**Used by:** Business Architecture, Application Architecture

**MCP tool call:**
```
Tool: search_fact_sheets
Parameters:
  type: "BusinessCapability"
  query: "{capability name}"
  includeRelations: ["relBusinessCapabilityToApplication"]
  fields: [name, description, strategicImportance]
```

**GraphQL equivalent:**
```graphql
{
  allFactSheets(
    filter: {
      facetFilters: [
        { facetKey: "FactSheetTypes", keys: ["BusinessCapability"] }
      ]
      fullTextSearch: "{capability name}"
    }
  ) {
    edges {
      node {
        name
        ... on BusinessCapability {
          description
          relBusinessCapabilityToApplication {
            edges {
              node {
                factSheet {
                  name
                  ... on Application {
                    lifecycle { asString }
                    businessCriticality
                    technicalFit
                    functionalFit
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

---

## Query 3: Interfaces Between Two Applications

**Purpose:** Find existing integrations (data flows) between two applications — used before proposing new integrations.  
**Used by:** Integration Architecture, Application Architecture

**MCP tool call:**
```
Tool: get_application_relations
Parameters:
  applicationName: "{source application}"
  relationType: "relApplicationToInterface"
  fields: [name, description, protocol, frequency, dataObjects, targetApplication]
```

**GraphQL equivalent:**
```graphql
{
  allFactSheets(
    filter: {
      facetFilters: [
        { facetKey: "FactSheetTypes", keys: ["Interface"] }
      ]
      fullTextSearch: "{application name}"
    }
  ) {
    edges {
      node {
        name
        ... on Interface {
          description
          relInterfaceToProviderApplication { edges { node { factSheet { name } } } }
          relInterfaceToConsumerApplication { edges { node { factSheet { name } } } }
          relInterfaceToDataObject { edges { node { factSheet { name } } } }
        }
      }
    }
  }
}
```

**Expected output structure:**
```
Interface: CRM→SAP:CustomerMaster:REST
  Provider: CRM Dynamics 365
  Consumer: SAP S/4HANA
  Protocol: REST API (synchronous)
  Frequency: Real-time
  Data Objects: Customer.Profile, Customer.Address
  Business Criticality: HIGH
```

---

## Query 4: IT Components / Technology Stack for an Application

**Purpose:** Get the technology stack underlying an application — used for lifecycle and tech radar checks.  
**Used by:** Technology & Infrastructure, Application Architecture

**MCP tool call:**
```
Tool: get_application_relations
Parameters:
  applicationName: "{application name}"
  relationType: "relApplicationToITComponent"
  fields: [name, category, lifecycle, vendor, endOfSupport]
```

**GraphQL equivalent:**
```graphql
{
  allFactSheets(
    filter: {
      facetFilters: [
        { facetKey: "FactSheetTypes", keys: ["Application"] }
      ]
      fullTextSearch: "{application name}"
    }
  ) {
    edges {
      node {
        name
        ... on Application {
          relApplicationToITComponent {
            edges {
              node {
                factSheet {
                  name
                  ... on ITComponent {
                    category
                    lifecycle { asString phases { phase startDate } }
                    vendor
                    description
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

---

## Query 5: Data Objects and Ownership

**Purpose:** Identify data objects, their classification, ownership, and which applications produce/consume them.  
**Used by:** Data & AI, Integration Architecture

**MCP tool call:**
```
Tool: list_data_objects
Parameters:
  query: "{data domain — e.g., Customer, Employee, Order}"
  fields: [name, description, classification, owner, producingApplications, consumingApplications]
```

**GraphQL equivalent:**
```graphql
{
  allFactSheets(
    filter: {
      facetFilters: [
        { facetKey: "FactSheetTypes", keys: ["DataObject"] }
      ]
      fullTextSearch: "{data domain}"
    }
  ) {
    edges {
      node {
        name
        ... on DataObject {
          description
          relDataObjectToApplication {
            edges {
              node {
                factSheet { name }
                relationshipType
              }
            }
          }
        }
      }
    }
  }
}
```

---

## Query 6: Technology Radar Positions

**Purpose:** Check the current radar position of a technology or product.  
**Used by:** Application Architecture, Technology & Infrastructure

**MCP tool call:**
```
Tool: get_tech_radar
Parameters:
  query: "{technology name}"
  fields: [name, radarRing, radarCategory, assessmentDate, rationale]
```

> **Note:** Tech radar in LeanIX may be modeled as tags or custom fields on IT Components. If your workspace uses a custom radar model, adjust the query to match your implementation.

---

## Query 7: Full Fact Sheet by ID

**Purpose:** Retrieve a specific fact sheet with all fields when you have the LeanIX ID.  
**Used by:** All agents (for drill-down after search results)

**MCP tool call:**
```
Tool: get_fact_sheet
Parameters:
  id: "{leanix-fact-sheet-uuid}"
  includeRelations: true
```

---

## Query 8: Upcoming Lifecycle Transitions

**Purpose:** Find applications or IT components approaching Phase Out or End of Life within N months.  
**Used by:** Application Architecture, Technology & Infrastructure, Chief Architect

**MCP tool call:**
```
Tool: list_applications
Parameters:
  filter:
    lifecyclePhaseTransitionBefore: "{date — e.g., 2027-01-01}"
    currentPhase: "active"
  fields: [name, lifecycle, nextPhase, nextPhaseDate, businessCriticality]
```

**GraphQL equivalent:**
```graphql
{
  allFactSheets(
    filter: {
      facetFilters: [
        { facetKey: "FactSheetTypes", keys: ["Application"] }
        { facetKey: "lifecycle", keys: ["active"] }
      ]
      lifecycle: {
        asOf: "2027-01-01"
        phases: ["phaseOut", "endOfLife"]
      }
    }
  ) {
    edges {
      node {
        name
        ... on Application {
          lifecycle { asString phases { phase startDate } }
          businessCriticality
        }
      }
    }
  }
}
```

---

## Query Conventions for Agents

1. **Always search before stating facts.** Never make claims about the portfolio without a query in this session.
2. **Start broad, then drill.** Use `search_fact_sheets` first, then `get_fact_sheet` by ID for detail.
3. **Check for absence.** If a query returns zero results, that's a finding (possible shadow IT or documentation gap).
4. **Cite LeanIX IDs.** When referencing a fact sheet in your output, include the name and LeanIX ID so humans can verify.
5. **Rate-limit awareness.** Batch related queries where possible. Avoid per-application loops for large portfolio scans.
