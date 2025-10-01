# Power BI Theme Builder
> Agent assisted system that extracts visual properties from PBIP JSON, maps them to canonical visual templates, and emits client specific theme JSON files.

## Table of Contents
- [Overview](#overview)
- [Folder Map](#folder-map)
- [Workflow and Milestones](#workflow-and-milestones)
- [File Naming and Versions](#file-naming-and-versions)
- [Validation Contract](#validation-contract)
- [Prompt Contract for Follow-up Agents](#prompt-contract-for-follow-up-agents)
- [Scorecards and Grading](#scorecards-and-grading)
- [Contribution Rules](#contribution-rules)
- [Changelog](#changelog)
- [Glossary](#glossary)

## Overview
This repository powers an auditable pipeline for producing Power BI themes. Source inputs are PBIP exported JSON fragments housed under `3.Sample Files`. Canonical per-visual templates live in `1.Visual Templates`, and client-ready themes are published under `2.Custom Themes` with semantic versioning.

Validation is enforced locally and via CI using the reference schema `reportThemeSchema-2.114.json` and supporting assets such as `tests/testSchema.json`. Each agent run must remain idempotent and conclude with an updated scorecard.

Legacy documentation is archived for traceability. The previous working README is now available at [`4.Documentation/legacy/README_1.1.md`](4.Documentation/legacy/README_1.1.md).

## Folder Map
| Path | Purpose | Key files | File counts |
| --- | --- | --- | --- |
| `/` | Root assets and schemas | `reportThemeSchema-2.114.json` | 1 JSON |
| `1.Visual Templates` | Canonical per-visual JSON templates | 38 template `.json` files | 38 JSON |
| `2.Custom Themes` | Client theme definitions (semantic versioned) | `Rainwater Theme v4.1.json`, `Virginia Forest.json` | 2 JSON |
| `3.Sample Files` | PBIP extraction inputs and test fragments | *(seed placeholder)* | 0 files |
| `4.Documentation` | Human + machine documentation, inventories | `# Power BI Theme Builder.md`, `FAQ.md`, `_reports/repo_inventory.json` | 8 files |
| `_reports/scorecards` | Run-level scorecards (`scorecard.v1`) | *(populated per run)* | 0 files |
| `.github/workflows` | CI validation pipelines | `tests-validate-json.yml` et al. | 5 YAML |
| `tests` | Schema fixtures for validation | `testSchema.json` | 1 JSON |

The latest repository inventory is captured at [`_reports/repo_inventory.json`](./_reports/repo_inventory.json) and is regenerated before any write action.

## Workflow and Milestones
### Final Workflow
1. **scan.inventory** — Recursively scan the repository, regenerate the inventory JSON grouped by folder and extension, and ensure `_reports/scorecards` exists.
2. **author.readme** — Synthesize the root `README.md` from the outline and current inventory, archiving any prior README copies under `4.Documentation/legacy/`.
3. **milestones.contract** — Declare and maintain the milestone artifact contract documented below.
4. **validation.contract** — Apply repository validation rules before committing artifacts.
5. **scoring.emit** — Emit a `scorecard.v1` JSON record under `_reports/scorecards/` describing the run.

### Milestone Artifacts
| Milestone | Artifact path pattern | Notes |
| --- | --- | --- |
| Extracted properties | `/3.Sample Files/{sampleSet}/{visualType}/properties.md` | Markdown summary of PBIP-derived properties limited to canonical template fields. |
| Templatized JSON | `/1.Visual Templates/{visualType}.templatized.json` (+ `.pretty.json` when >200 lines) | Template merged with extracted properties; keep paired pretty print when needed. |
| Theme update | `/2.Custom Themes/{client}/{themeName}.{semver}.json` | Insert templatized block, bump semantic version, append changelog entry inside the theme. |

All milestones are additive and must remain idempotent between runs.

## File Naming and Versions
- Theme files use semantic versioning, e.g. `ClientA.Corporate.1.2.0.json`, and include a matching internal `themeVersion` field.
- Visual templates stay one visual per file inside `1.Visual Templates`.
- When generated JSON exceeds 200 lines, emit both the minified artifact and a `.pretty.json` companion.
- Archive superseded documentation under `4.Documentation/legacy/` instead of deleting it.

## Validation Contract
- Parse every JSON artifact with a strict parser before writing.
- Validate theme JSONs against `reportThemeSchema-2.114.json`; use `tests/testSchema.json` for supporting checks.
- Ensure artifact paths exactly match the milestone patterns above.
- Perform an idempotency check (hash or diff) and skip writes when no changes are required.
- Confirm Markdown and JSON lint succeed locally or via CI before merge.

## Prompt Contract for Follow-up Agents
```xml
<contract version="1.0">
  <requirement>Read a fresh repository inventory before any modification.</requirement>
  <requirement>Apply the milestone path patterns without deviation.</requirement>
  <requirement>Emit a scorecard for every action using schema scorecard.v1.</requirement>
  <requirement>Run JSON and Markdown validation referencing reportThemeSchema-2.114.json and tests/testSchema.json as appropriate.</requirement>
  <requirement>Maintain idempotency across repeated executions.</requirement>
</contract>
```

## Scorecards and Grading
- Location: `/_reports/scorecards/` (create if missing).
- Schema: `scorecard.v1` with fields `task_id`, ISO8601 `timestamp`, an `inputs_digest`, `metrics`, `warnings`, `errors`, `notes`, `artifact_paths`, and `final_grade`.
- Metrics (targets): `repo_coverage` (1.0), `README_completeness` (0.95), `workflow_fidelity` (0.95), `idempotency_proof` (0.90), `lint_quality` (0.90).
- Grades: `Aplus` (all targets hit, no failures), `A` (>= 0.95 weighted with <= 1 minor warning), `B` (0.85-0.949), `Fail` (below 0.85 or any critical failure).
- Include created or updated artifact paths in each scorecard note for traceability.

## Contribution Rules
- Never delete generated artifacts; archive or bump versions instead.
- Keep `1.Visual Templates` aligned with official Power BI visual types and naming.
- Run JSON and Markdown lint locally; ensure GitHub workflows in `.github/workflows/` pass before merging.
- Document every agent run with a scorecard and, when applicable, update the changelog.

## Changelog
- 2025-10-01 — Initialized agent onboarding README, archived prior `README 1.1.md`, established workflow, milestone, validation, and scoring contracts.

## Glossary
- **PBIP JSON** — Exported JSON artifacts from a Power BI project bundle.
- **Templatized JSON** — A canonical visual template populated with extracted client-specific properties.
- **Theme JSON** — A client theme file aggregating visual defaults, stored under `2.Custom Themes` with semantic versioning.
- **Idempotent run** — Re-executing the workflow without introducing duplicate artifacts or redundant changes.
