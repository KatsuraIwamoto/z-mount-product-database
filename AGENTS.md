# AGENTS.md

## Purpose and authority

This repository maintains two public Nikon Z-compatible datasets: lenses and directly
mountable related optical products (`lenses`), and mount-conversion adapters (`adapters`).

Schemas and executable validation define data contracts and cross-file rules.
The task-specific documents linked below define the applicable editorial and engineering
rules; read their relevant sections when doing that work, whether or not a skill is used.
Narrative documentation never overrides validation. `docs/ja/` is primary and the paired
`docs/en/` is its AI-translated mirror; use either edition without loading both by default.
The research skill is an operational aid, not an alternative source of policy.

## Sources of truth

- Canonical products: `data/records/{lenses,adapters}/<brand-id>/<id>.json`
- Decisions and evidence: `research/results/{lenses,adapters}/<brand-id>/<id>.json`
- Identity registry: `data/product-manufacturer-brand-registry.json`
- Mount registry: `data/mount-system-registry.json`
- Versions: `config/versions.json`
- Public contracts: `schemas/{shared,lenses,adapters}/*.schema.json`
- Repository-only registry validation: `schemas/internal/*.schema.json`

`dist/z-mount-lenses.full.json`, `dist/z-mount-lenses.light.json`,
`dist/z-mount-adapters.full.json`, and `PRODUCTS.md` are generated and committed.
Edit their inputs and regenerate; never edit these artifacts manually.

## Repository-wide boundaries

- Preserve published facts and names. Do not guess unpublished facts or silently choose
  between conflicting sources. Keep unresolved questions explicit.
- A public product key is `(namespace, id)`, not a bare `id`. Do not derive product facts
  or display text from slug text.
- Product keys and manufacturer, brand, and mount IDs become fixed on first appearance
  in an official GitHub Release asset. Never rename, reassign, or reuse published IDs.
  Reintroduce the same product with its reserved ID. Before publication, working IDs
  may be corrected. Stable IDs do not guarantee permanent inclusion.
- For merges, splits, removals, or namespace changes, document the old key and replacement
  key (or no replacement) in release notes. Do not add a general ID-history schema or
  central ID registry until an exceptional change or concrete automation need requires it.
- Published versioned schema URLs and contents are immutable. Contract changes require
  a new `schemaVersion`; keep prior version directories available.
- Keep schema and data narratives English-first. Follow the documentation language and
  pairing rules in [Documentation maintenance](docs/en/development.md#documentation-maintenance).

## Read according to the change

| Work | Required rules and relevant references |
| --- | --- |
| Product additions, corrections, or research decisions | [Inclusion scope](docs/en/overview.md), [Evidence and research records](docs/en/research.md), and [Value rules](docs/en/value-rules.md), including `officialName` when used |
| Mapping evidence to canonical fields | The matching current schema; [Lens fields](docs/en/lens-field-reference.md) or [Adapter fields](docs/en/adapter-field-reference.md) for field meaning |
| Identity or registry changes | [Product keys and shared registries](docs/en/data-model.md), including pre-release usage and retention of published IDs |
| Generator, validator, schema, or release changes | [Generation and release constraints](docs/en/development.md#generation-and-release), [Schema changes](docs/en/development.md), and the affected contracts and tests |
| Documentation or instruction changes | [Documentation maintenance](docs/en/development.md#documentation-maintenance); keep policy in its owning document and link to it from operational guidance |

For product research, use
[the research skill](.agents/skills/z-mount-product-research/SKILL.md) for efficient
source discovery and task completion. Source eligibility, inclusion criteria, and value
rules still apply when the skill is not loaded. Do not read unrelated reference pages
merely because they are linked here.

## Validation and completion

Use Python 3.14 or later and Hatch; the project uses Ruff, strict mypy, and pytest.
Before declaring work complete, run the following commands in order and review the
generated diff. See [Development and validation](docs/en/development.md#workflow)
for the full workflow.

```bash
hatch run generate
hatch run check
hatch run docs:build
```

Complete the requested work through these checks, resolve failures caused by the
change, and report remaining blockers. Completion requires current generated artifacts,
no guessed official facts, and explicit unresolved research questions.
