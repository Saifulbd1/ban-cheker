# Changelog

All notable changes to the **FF Ban Check** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-08-21

### Added
- **Interactive Web Interface**: Built a responsive, dark gaming-themed UI template (`templates/index.html`).
- **Quick Sample Testing**: One-click test chips for sample Banned and Clean Free Fire UIDs.
- **Dedicated Endpoints**: Added `/developer` endpoint returning complete developer and social contact data.
- **Developer Branding**: Integrated **Refat Rahman** (`refatbd`) contact card including Website (`refat.ovh`), GitHub, Facebook, Instagram, Telegram, and WhatsApp.
- **JSON Negotiation**: Root endpoint (`/`) dynamically serves HTML to browsers or JSON when requested with `?format=json` or `Accept: application/json`.
- **Project Renaming**: Rebranded the project and GitHub repository to **`ff-ban-check`**.

### Changed
- Refactored `app.py` for template rendering and modular route handling.
- Updated `README.md` with comprehensive usage, API schemas, and deployment instructions.
- Configured license and repository origin to `https://github.com/refatbd/ff-ban-check.git`.

---

## [1.0.0] - 2026-08-21

### Added
- **Core Ban Check API**: Query Free Fire player ban status & ban duration directly from Garena's official Anti-Hack backend.
- **API Key Security**: Simple token authorization middleware (`/check_key` and `/bancheck`).
- **CORS Support**: Global cross-origin resource sharing for third-party integrations.
- **Serverless Support**: Configured `vercel.json` for one-click deployment on Vercel.
- **Initial Documentation**: Requirements list and setup guide.
