# Changelog
All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) where applicable.

## [Unreleased]
### Added
- `docs/theme_properties.md` cataloging general theme colors, borders, and fonts from the License Cost Analysis report.
- `themes/outputs/general-theme.json` providing the reusable Power BI general theme.
- `docs/theme_readme.md` documenting theme properties, usage guidance, and repository inventories.

### Changed
- Updated root `README.md` with a Themes section referencing the new assets.

## [2025-10-09]
### Added
- New developer-first repository layout with `docs/`, `reports/`, `src/`, and `themes/` roots.
- `themes/MANIFEST.json` plus folder-level README files and machine specs.
- Documentation index at `docs/index.md` and refreshed root README pairing with `README.machine.md`.

### Changed
- Migrated legacy `1.Visual Templates`, `2.Custom Themes`, `3.Sample Files`, `_reports`, `tools`, and `tests` into the new structure.
- Normalised file naming to lower_snake_case across inputs, outputs, prompts, and scripts.
- Updated prompts and Python automation scripts to point at the new directories and filenames.

### Removed
- Deprecated scaffolding folders (`1.Visual Templates`, `2.Custom Themes`, `3.Sample Files`, `4.Documentation`, `_reports`, `tools`, `tests`).

## [2025-10-01]
### Added
- Initial onboarding README, workflow contracts, and scorecard guidance.
- Archived prior README references in `docs/legacy/`.
