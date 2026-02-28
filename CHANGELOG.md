# Changelog

All notable changes to this project are documented in this file.

This changelog uses Semantic Versioning (`MAJOR.MINOR.PATCH`) and Keep a Changelog style sections.

Historical versions were inferred from git commit history because this repository does not currently use version tags.

## [Unreleased]

Target release: **2.1.0** (`MINOR`) - new user-facing functionality without breaking the API contract.

### Added
- Added a Jira-style task List View at `/project/list` with table columns for work, assignee, reporter, priority, status, created/updated timestamps, and resolution.
- Added list-level filtering controls (search, assignee avatars, "Only my tasks", and status toggles).
- Added a dedicated issue details page for list items at `/project/list/issues/:issueId` with:
  - back-to-list navigation,
  - two-column details layout (main content + metadata sidebar),
  - editable issue fields reusing existing issue details modules (type, title, description, comments, status, assignees/reporter, priority, estimate/time tracking, dates).

### Changed
- Changed list issue opening behavior from modal-based display to full-page details route for a richer, persistent context.
- Refined list table cell layout and responsive behavior to match Jira-like alignment and readability.

### Fixed
- Fixed React hook-order crash in `ProjectListView` (`Rendered more hooks than during the previous render`).
- Fixed list table rendering issues caused by flex styles on `<td>` elements.
- Added null-safe issue/user/date handling in List View to prevent blank screens when payload fields are missing.

### Notes
- These frontend changes are currently in working tree state and should be committed before tagging `2.1.0`.

## [2.0.0] - 2026-02-28

`MAJOR` release due to backend runtime and developer workflow breakage (Node/TypeScript backend removed, Python/Flask backend required).

### Changed
- Updated client webpack scripts to run with `NODE_OPTIONS=--openssl-legacy-provider`, allowing `webpack@4` to run on modern Node versions.
- Updated API startup to fail fast with clear logs when the database is unavailable.
- Added database connection timeout support via `DB_CONNECT_TIMEOUT_MS` (defaults to `5000` ms).
- Migrated backend runtime from TypeScript/Express/TypeORM to Python/Flask/SQLAlchemy while keeping the client-facing REST contract.
- Removed legacy TypeScript backend sources (`api/src`) and TypeScript-specific backend config files.
- Switched backend operational commands to direct Python (`python3 run.py`) rather than npm wrappers in `api`.

### Fixed
- Fixed `ERR_OSSL_EVP_UNSUPPORTED` when starting the client on Node 22+.
- Fixed API "clean exit" behavior that hid database boot failures.
- Fixed backend compatibility issues on modern PostgreSQL and Node by replacing legacy backend runtime.

### Notes
- Lockfiles were updated by npm during dependency upgrades (`client/package-lock.json`, root `package-lock.json`, and `client/yarn.lock`), and `api/package-lock.json` was removed as part of the Python-native backend migration.
- Backend dependency installation now uses `api/requirements.txt` via `python3 -m pip install`.

### Commits
- `3955210` changed node api implementation to flask, replaced node completely with python for backend
- `a79a2bd` project updated and now works

## [1.0.0] - 2021-10-20

### Changed
- Project documentation and top-level README refresh.

### Commits
- `26a9e77` Update README.md
- `190dfcd` Readme formatting
- `9ec69d7` Added contributing guidelines
- `8788891` Added a MIT license

## [0.6.0] - 2020-01-11

### Added
- Production/deployment-oriented API and client configuration.

### Changed
- Client/API port and URL configuration cleanup.
- PM2 process naming for production startup.

### Commits
- `10e5696` Configured api and client for production builds
- `fe4ef2f` Extracted routes from controllers, wrote readme's
- `f1f79da` Fixed ports
- `544b1f7` Added API_PORT to client env
- `7be6b72` Changed default port for client server
- `27b8578` Added API_URL to client env
- `dc5c8b8` Added names for PM2 production processes

## [0.5.0] - 2020-01-05

### Added
- End-to-end test suite with Cypress.

### Commits
- `64b237e` Wrote end-to-end cypress tests

## [0.4.0] - 2019-12-27

### Added
- Project settings page.
- Issue search modal.
- Issue creation flow.
- Shared breadcrumbs component.

### Changed
- UI polish and module refactoring.

### Fixed
- Select component bug.

### Commits
- `4941261` Implemented issue create modal, further polish
- `7ceb18e` Implemented project settings page, search issues modal, general refactoring
- `2fb374b` Extracted breadcrumbs into a shared component, added it to project settings page
- `821547e` Fixed a select component bug
- `bbda9b9` Added withClearValue prop to select component

## [0.3.0] - 2019-12-18

### Added
- Issue details modal and issue comments support.

### Commits
- `386694d` Implemented first draft of issue modal
- `32170e9` Implemented issue comments

## [0.2.0] - 2019-12-14

### Added
- Kanban board lists.
- Drag-and-drop issue movement.

### Commits
- `73b4ff9` Implemented kanban board page with lists of issues
- `f48b2a9` Implemented issue drag and drop

## [0.1.0] - 2019-12-03

### Added
- Initial API/client split and foundational project structure.
- Core entities, routes, seed scripts, and shared client building blocks.

### Commits
- `5a08433` Implemented basic entities, routes, seed scripts
- `84f0897` Moved api into it's own folder
- `6be3ac2` Initial client setup
- `3143f66` Added some basic shared components, utils, hooks

## [0.0.1] - 2019-11-20

### Added
- Initial repository setup.

### Commits
- `9edb74c` Initial setup
