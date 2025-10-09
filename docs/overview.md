# Power BI Theme Builder Overview

This repository delivers an auditable Power BI theme pipeline. Inputs originate from PBIP exports, pass through transformation scripts under `src/`, and land in versioned outputs under `themes/outputs/` with supporting analytics in `reports/`.

## Current Folder Map
1. `themes/inputs/visual_templates/` – canonical per-visual JSON templates.
2. `themes/inputs/schemas/` – schema references (`report_theme_schema-2_114.json`, `test_schema.json`).
3. `themes/outputs/` – client theme payloads (`rainwater/`, `spend_cube/`, `virginia_forest/`).
4. `themes/samples/` – PBIP sample bundles used for regression testing.
5. `src/scripts/` – Python automation entry points (table/matrix pipelines, comparison tooling).
6. `reports/` – generated catalogs, diffs, manifests, scorecards, and validation notes.
7. `docs/` – developer guidance, prompts, and project archives.

Legacy documentation is preserved in `docs/legacy/legacy_readmes/` for historical reference.

## Workflow Summary
1. **Extract** – capture properties from PBIP samples and record them in `reports/datasets/` or project notes under `docs/projects/`.
2. **Template** – update or add templates in `themes/inputs/visual_templates/`; maintain lower_snake_case naming.
3. **Generate** – assemble client themes in `themes/outputs/` using automation from `src/scripts/`.
4. **Validate** – enforce schema conformance and semantic checks using the scripts and schemas in `themes/inputs/schemas/`.
5. **Report** – refresh analytics and documentation in `reports/` and `docs/` to match the latest theme state.

## Naming & Versioning
- Theme filenames follow lower_snake_case and include a version suffix (e.g., `rainwater_theme_v4_1.json`).
- Template companions exceeding 200 lines may include `_pretty.json` variants.
- PBIP sample directories mirror the original export names but use lower_snake_case (e.g., `spend_cube_report`).

## Prompt & Scorecard Contracts
- Automation prompts are stored in `docs/prompts/` and are referenced by scripts via the `--prompt` argument.
- Each material change should emit a `scorecard.v1` record in `reports/scorecards/` summarizing metrics, warnings, and artifacts touched.

## Glossary
- **PBIP JSON** – JSON artifacts exported from a Power BI desktop project.
- **Theme manifest** – `themes/MANIFEST.json` describing active inputs, outputs, and schema requirements.
- **Catalog** – Aggregated attribute inventory derived from PBIP scans, stored in `reports/datasets/catalog.*`.
