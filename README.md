# Configurator Lite

**Configurator Lite** is a minimal, deterministic configuration validation and bundling tool designed to run reliably on constrained or hostile environments (e.g., broken macOS systems, fresh Windows installs, recovery workflows).

It exists to answer one question with certainty:

> “Is this configuration valid, enforceable, and reproducible?”

If the answer is yes, Configurator Lite produces a portable bundle artifact.  
If the answer is no, it fails fast and tells you why.

---

## Design Goals

- **Offline-first** — no network access required at runtime
- **Deterministic output** — same input produces the same bundle
- **Strict contracts** — Lite mode cannot silently grow scope
- **Cross-platform** — Windows, macOS, Linux
- **Minimal surface area** — no background services, no daemons
- **Fail fast** — configuration errors stop execution immediately

This tool was intentionally designed to run from **Windows** in order to recover, validate, and repair **macOS systems** when native tooling is unavailable or unreliable.

---

## What It Does

1. Loads a configuration file (`.yaml`, `.yml`, or `.json`)
2. Validates it against a JSON Schema
3. Enforces the **Lite contract**
4. Emits a **bundle artifact** to `dist/`
5. Exits cleanly

---

## What It Does *Not* Do

- ❌ No automatic system changes
- ❌ No network calls
- ❌ No credential storage
- ❌ No background processes
- ❌ No self-updating
- ❌ No hidden side effects

Configurator Lite is **deliberately boring**. That’s a feature.

---

## Requirements

- Python **3.11+**
- OS: Windows, macOS, or Linux

Python dependencies (installed via `requirements.txt`):

- `pyyaml`
- `click`
- `rich`
- `jsonschema`

---

## Installation

### Clone the repository
```bash
git clone git@github.com:datareccer/ConfiguratorLite.git
cd ConfiguratorLite
reate and activate a virtual environment

Windows (Git Bash):

python -m venv .venv
source .venv/Scripts/activate


macOS / Linux:

python3.11 -m venv .venv
source .venv/bin/activate

Install dependencies
pip install -r requirements.txt

Usage
Run with a config file
python src/configurator_lite.py config.yaml

Example output
Configurator Lite v1.1.0
Configurator Lite Output
{'name': 'test', 'mode': 'lite', 'enabled': True}
Bundle written to dist/bundle-test.json

Configuration Example
config.yaml
name: test
mode: lite
enabled: true

Output Bundle

Configurator Lite writes an immutable bundle to dist/:

{
  "tool": "Configurator Lite",
  "version": "1.1.0",
  "generated_at": "2025-12-23T12:34:56Z",
  "config": {
    "name": "test",
    "mode": "lite",
    "enabled": true
  }
}


This bundle can be:

Archived

Transported to another system

Used as a validation artifact

Attached to releases or audits

Lite Contract

Lite mode is intentionally constrained.

Guaranteed properties:

No network access

No system mutation

Schema-validated input

Deterministic output

Violating the Lite contract results in immediate termination.

Versioning

Current release: v1.1.0

Semantic versioning

Tags are immutable once published

Intended Use Cases

macOS recovery workflows from Windows

Configuration validation in CI

Offline system preparation

Disaster recovery tooling

Minimal config enforcement pipelines

Philosophy

If a system cannot validate its own configuration,
it should not be trusted to change anything else.

Configurator Lite exists to restore control, clarity, and determinism in environments where those qualities are missing.

License

MIT (or replace with your preferred license)

Author

Built by Wesley Middleton
For environments where reliability matters more than convenience.


---
