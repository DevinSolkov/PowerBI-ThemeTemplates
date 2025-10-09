# Power BI Theme Builder
> Automated toolkit for extracting, templating, and packaging Power BI theme assets from PBIP exports.

## Repository Layout
| Path | Purpose | Highlights |
| --- | --- | --- |
| `.github/` | GitHub Actions, issue templates, and repository policies. | JSON/Markdown validation workflows. |
| `docs/` | Developer documentation, policies, prompts, and project notes. | See `docs/index.md` for the living index. |
| `reports/` | Generated analytics, scorecards, and supporting datasets. | Diff outputs now live under `reports/diffs/`. |
| `src/` | Python automation scripts that transform and validate theme content. | Scripts load prompts from `docs/prompts/`. |
| `themes/` | Authoritative inputs, generated outputs, and PBIP samples. | `themes/MANIFEST.json` tracks active assets. |
| `README.machine.md` | Machine-friendly quick spec for automations. | Pairs with this human overview. |
| `CHANGELOG.md` | Keep a Changelog log of repository activity. | Updated with every structural change. |

## Themes
- `docs/theme_readme.md` – License Cost Analysis general theme notes and usage guide.
- `themes/outputs/general-theme.json` – Power BI import file generated from the analysis.
- `docs/theme_properties_v3_4_3.md` / `docs/theme_mapping_v3_4_3.md` – Rainwater 3.4.3 table and matrix extraction docs.
- `themes/outputs/rainwater/v3_4_3/rainwater_theme_v3_4_3.json` – Rainwater theme without style presets aligned to AI Narrative screenshot.

## Working With Themes
- Raw Power BI visual templates live in `themes/inputs/visual_templates/` and follow lower_snake_case naming.
- Schema fixtures and validation helpers are under `themes/inputs/schemas/` (see `report_theme_schema-2_114.json` and `test_schema.json`).
- Client deliverables are grouped in `themes/outputs/` by client and version (e.g., `rainwater/v4_1/`).
- PBIP extracts used for QA reside in `themes/samples/` (e.g., `themes/samples/spend_cube_report/`).
- The canonical manifest at `themes/MANIFEST.json` declares available inputs, outputs, and schema requirements.

## Automation Scripts
All automation entry points live in `src/scripts/`:
- `build_table_matrix_templates.py` generates table/matrix presets from catalog insights.
- `integrate_table_matrix_templates.py` merges generated presets into the Rainwater theme.
- `table_matrix_style_report.py` emits attribute summaries for table and matrix visuals.
- `theme_summary_comparison.py` compares theme coverage against scanned catalog data and enforces font standards.

Scripts use prompt configurations in `docs/prompts/`. Invoke them with `python src/scripts/<script>.py --prompt docs/prompts/<prompt>.xml` to reproduce prior runs.

## Validation & Reporting
- Generated analytics, manifests, and scorecards are grouped in `reports/`:
  - `reports/datasets/` — CSV and JSON source data (catalog, inventories, change logs).
  - `reports/diffs/` — JSON/CSV comparisons between theme versions and catalog scans.
  - `reports/table_matrix/` — manifests, validation logs, and metrics for table/matrix workstreams.
  - `reports/summaries/` — executive summaries and verification notes.
  - `reports/scorecards/` — `scorecard.v1` records for each automation run.
- Always update or regenerate the relevant report when modifying associated assets.

## Documentation
- Start with `docs/index.md` for navigation across setup notes, schema references, prompts, and project archives.
- Project-specific materials (e.g., Spend Cube engagement) live under `docs/projects/`.
- Policy documents (Code of Conduct, Contributing) are in `docs/policies/`.
- Prompt archives, including this reorganization brief, live in `docs/prompts/`.
- Historical READMEs remain preserved in `docs/legacy/`.

## Change History
This README covers the current structure introduced in October 2025. Earlier workflows referencing `1.Visual Templates`, `2.Custom Themes`, and `3.Sample Files` are now retired. Track future updates in `CHANGELOG.md`.

For machine-readable automation hints see `README.machine.md`; for additional detail on any directory consult the README inside that folder.
