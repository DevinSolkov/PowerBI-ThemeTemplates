# Power BI Theme Builder

> Agent assisted system that extracts visual properties from PBIP JSON, maps them to canonical visual templates, and emits client specific theme JSON files.

## Table of contents
1. Overview
2. Folder map
3. Workflow and milestones
4. File naming and versions
5. XML prompt contract for follow up agents
6. Scorecards and grading
7. Contribution rules
8. Changelog
9. Glossary

## Overview
This workspace enables consistent and automatable theme creation for Power BI. Inputs are PBIP exported JSON fragments. Outputs are client theme JSONs under `2.Custom Themes`. JSON validity is checked against `reportThemeSchema-2.114.json` and repository CI workflows.

## Folder map
1. `1.Visual Templates` contains canonical per visual JSON templates. One file per visual, for example `Gauge.json`, `Pie.json`, `Matrix.json`.
2. `2.Custom Themes` contains client theme JSONs with semantic versions, for example `Rainwater Theme v4.1.json`.
3. `3.Sample Files` contains PBIP JSON fragments used for extraction and testing.
4. `_reports/scorecards` contains scorecards per agent action. Create this directory if missing.
5. `.github/workflows` contains validation workflows for JSON and docs.
6. `tests` contains `testSchema.json` and other validation assets.
7. `docs/legacy` holds archived readme files if present.

Archived readme links when present  
`/docs/legacy/README_1.1.md` for the previous working readme  
`/docs/legacy/README_original.md` for any older top level readme

## Workflow and milestones
1. Extracted properties  
   For a chosen visual and PBIP sample, extract only the properties that match the canonical template. Save as Markdown at  
   `3.Sample Files/<sampleSet>/<visualType>/properties.md`
2. Templatized JSON  
   Merge the extracted properties into the visual template. Save at  
   `1.Visual Templates/<visualType>.templatized.json`  
   When the file exceeds 200 lines, also write a companion `.pretty.json`.
3. Theme update  
   Insert the templatized block into a client theme and bump the version. Save at  
   `2.Custom Themes/<client>/<themeName>.<semver>.json`  
   Add a `changelog` entry inside the theme file.

Every step validates with a strict JSON parser. Every step emits a scorecard.

## File naming and versions
1. Theme files use semantic versioning, for example `ClientA.Corporate.1.2.0.json`. Include an internal `themeVersion` field that matches the file name.
2. Keep templates scoped to a single visual type.
3. When a generated JSON file exceeds 200 lines, write a `.pretty.json` beside the minified version.

## XML prompt contract for follow up agents
Agents must
1. Read a fresh repository inventory before any write.
2. Respect idempotency and update in place when content is functionally identical.
3. Emit a scorecard for every action using the schema `scorecard.v1`.
4. Validate JSON and reference `reportThemeSchema-2.114.json` or `tests/testSchema.json` when relevant.

## Scorecards and grading
Location for scorecards  
`/_reports/scorecards/`

Metrics and targets  
`repo_coverage` target 1.0  
`README_completeness` target 0.95  
`workflow_fidelity` target 0.95  
`idempotency_proof` target 0.90  
`lint_quality` target 0.90

Grade bands  
A plus, A, B, Fail  
Aim for A plus

## Contribution rules
1. Do not delete generated artifacts. Prefer version bumps and archival.
2. Keep `1.Visual Templates` consistent with official Power BI visual types.
3. Run JSON and Markdown lint locally before commit. Ensure GitHub checks pass.

## Changelog
1. 2025 10 01 created `README.md`, archived `README 1.1.md` when present, and enabled scorecarding.

## Glossary
1. PBIP JSON means exported JSON from a Power BI project.
2. Templatized JSON means a visual template with extracted properties applied.
3. Theme JSON means a client specific theme file that aggregates visual level defaults.
