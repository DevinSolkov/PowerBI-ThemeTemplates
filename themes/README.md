# Themes Directory
- `inputs/visual_templates/`: canonical per-visual templates. Lower_snake_case file names match Power BI visual types.
- `inputs/schemas/`: theme schema references (`report_theme_schema-2_114.json`, `test_schema.json`).
- `outputs/`: client deliverables grouped by client/version (`rainwater/v4_1`, `spend_cube`, `virginia_forest`).
- `samples/`: PBIP exports for regression testing (e.g., `spend_cube_report`).
- `MANIFEST.json`: machine-readable index of inputs, outputs, schema versions, and sample coverage.

Update the manifest and relevant READMEs whenever new clients, versions, or samples are added.
