# Business Architecture Policies

## Policy Enforcement

Policies marked `[MANDATORY]` are non-negotiable. All others are strong defaults that require documented rationale to override.

---

## BA-POL-001: Strategy Alignment Gate [MANDATORY]

Every significant technology investment (Standard impact or above) must be traceable to at least one strategic objective or approved business capability roadmap item.

**Evidence required:** A named strategic objective or capability initiative from the current planning cycle.  
**Consequence of failure:** The investment is not approved for architecture endorsement. Return to business sponsor for strategic alignment.

---

## BA-POL-002: Capability Redundancy Check [MANDATORY]

Before approving a new application or platform, the Business Architecture agent must verify that the capability it provides is not already covered by an existing application in the LeanIX portfolio.

**Process:** Query LeanIX for Business Capabilities served → check Application Landscape → identify overlaps.  
**Consequence:** If redundancy exists, the new application must be justified against total cost of ownership comparison and a rationalization plan for the redundant system.

---

## BA-POL-003: Business Case Requirement

All Major and Critical decisions require a business case, including:
- Expected business value (quantified where possible)
- Time to value
- Total cost of ownership (3-year minimum)
- Key assumptions and dependencies

---

## BA-POL-004: Stakeholder Impact Assessment

Any change affecting more than one business unit requires a stakeholder impact assessment identifying:
- Affected departments and user groups
- Process changes required
- Training and adoption effort
- Communication plan ownership

---

## BA-POL-005: Capability Ownership

Every business capability must have a named business owner. Architecture proposals that create new capabilities without an identified business owner must flag this as a governance gap.

---

## BA-POL-006: Build vs. Buy Alignment with Strategy

Capabilities that are **differentiating** (competitive advantage) should prefer build or configure over commodity SaaS.  
Capabilities that are **commodity** (undifferentiating) should prefer SaaS or shared services.  
Use Wardley Mapping positioning (genesis/custom/product/commodity) to determine classification.

---

## BA-POL-007: Architecture Decision Record — Business Justification

Every ADR at Standard level and above must include a business justification section completed by the Business Architecture agent before the ADR is finalized.
