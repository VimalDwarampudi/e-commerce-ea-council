# SKILL: Navigating the Retail EA Council Knowledge Bundle

This is a small, stable procedure for reading `knowledge/` — an **OKF (Open Knowledge Format) bundle**
containing the retail EA council's policies, principles, guidelines, examples, tech radar, and reference
architectures. The bundle is large and will keep growing as the council operates; this file should stay
short and not need to change when it does.

## What OKF is, briefly

An OKF bundle is a directory of markdown "concept" files, each with a small YAML frontmatter block. The
only field every concept is guaranteed to have is `type`. Concepts link to each other with normal markdown
links. Two filenames are reserved: `index.md` (a catalog of concepts at that level, for progressive
disclosure) and `log.md` (chronological change history). Full spec:
https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md

This bundle uses two layers of `type`:
- **Governance types** — `Principle`, `Policy`, `Guideline`, `Example`, `TechRadarEntry`,
  `ReferenceArchitecture`, `Glossary`. Authored knowledge about how to decide.
- **Asset types** — `Table`, `API`, `Metric`. Describe actual system assets (schemas, contracts,
  operational metrics) per the domain. Currently sample placeholders (`status: PLACEHOLDER` in
  frontmatter) — treat their specific field names/values as illustrative, not verified, until that flag is
  removed. This is the standard OKF use case per Google's own reference bundle (a real dataset's tables and
  metrics), not a deviation from the format.

## Procedure

**1. Always start at the top.** Read `knowledge/index.md`. It lists all 15 domain sub-bundles and the
`shared/` enterprise-wide content, with a concept count for each. Do not read anything else first.

**2. Identify the relevant domain(s).** Match the question against the domain list in `knowledge/index.md`
and `council-config.md`'s routing table. Most questions touch 1–3 domains plus `shared/`.

**3. Drill into each relevant domain's `index.md`.** e.g. `knowledge/payments/index.md`. This lists every
concept file in that domain with its `type` and title — this is your filter. Do **not** read every file in
a domain by default; read the index, then select.

**4. Read by type, in this priority order:**
   - **`Policy` files with `mandatory: true`** first, always — these can eliminate an option outright and
     override everything else in the conflict-resolution hierarchy.
   - **`Principle` files** next — these ground your recommendation.
   - **`Guideline` files** relevant to the specific question — these give you a method to apply.
   - **`Example` files** last among governance types, and only if a similar scenario exists — these show
     the expected output shape and often cross-reference other domains' examples via markdown links. Follow
     those links when they're relevant; the bundle is a graph, not a set of isolated folders.
   - **`Table` / `API` / `Metric` files** — check these when the question is about an actual system's
     schema, contract, or operational number, not just policy. Check `status` in the frontmatter first: if
     `PLACEHOLDER`, say so explicitly in your answer rather than presenting the sample field names/values
     as real.

**5. Always check `knowledge/shared/index.md`.** The 12 enterprise-wide principles there take precedence
over domain-specific preferences when they conflict (see the conflict-resolution hierarchy in
`orchestration/deliberation-protocol.md`). If the question involves a specific technology, also check
`knowledge/shared/tech-radar/index.md` for its ADOPT/TRIAL/ASSESS/HOLD status before recommending it. If a
`ReferenceArchitecture` concept already exists for the scenario, prefer citing and applying it over
designing from scratch.

**6. Check `knowledge/log.md`** only when you need to know what changed recently or when — not as part of
routine navigation.

## What NOT to do

- Don't read every file in the bundle "to be safe." The index files exist so you don't have to — that's
  the entire point of progressive disclosure.
- Don't treat a domain's `index.md` as optional. Skipping straight to a concept file by guessing its name
  means you'll miss related concepts the index would have surfaced.
- Don't invent a `type` or a concept that isn't in an index. If the knowledge doesn't exist yet, say so
  explicitly rather than reasoning as if it does — and flag it as a gap worth adding to the bundle.

## Who uses this file

- The **Chief Architect** (`CLAUDE.md`, the orchestrator) uses this procedure during triage to pull the
  right shared context before dispatching to subagents.
- Each of the **15 subagents** (`.claude/agents/*.md`) references this file directly and applies the same
  procedure scoped to their own domain folder.

This file is the "schema" layer in the three-layer knowledge pattern (raw sources are immutable in
practice here since the bundle *is* the source; the bundle itself is maintained deliberately by architects,
not auto-compiled from a wider corpus; this file is the stable procedure that doesn't change when the
bundle's content does).
