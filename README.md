# E-commerce Project

## Project overview
A small e-commerce toy project implementing `User`, `Product`, `Card`, and `Order` classes with simple JSON-backed registries for persistence. Useful as a learning/experiment project for object design and simple file-based storage.

---

## Features
- User, Product, Card and Order classes with basic behavior (create users/products, make orders).
- Simple JSON file registries for users, products, carts and orders.
- Helper that ensures the data directories and baseline JSON files exist.

---

## Requirements
- Python 3.8+ (recommended)
- `cryptography` package

Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows (PowerShell)
pip install cryptography
```

---

## Quick start / How to run
> ⚠️ Note: paths in the code are currently Windows absolute paths (`c:/Users/...`). See *Path notes* below.

```bash
# from project root
python objects.py
```

This will:
- create product and user objects (the script ends with example `Product` and `User` instantiation).
- create / update JSON files under the configured `register_data` folders.

---

## File structure (important files)
- `objects.py` — class definitions for `User`, `Product`, `Card`, `Order` and example usage.
- `register.py` — JSON-based registries: `UserRegistery`, `ProductRegistery`, `CardRegistery`, `OrderRegistery`.
- `helper.py` — creates directories and default JSON files; generates a Fernet key.

---

## Path notes & running on non-Windows systems
The project currently uses hardcoded Windows-style paths (`c:/Users/jabar/...`) in `helper.py` and `register.py`. To run on other OSes, update these paths to relative paths or use `Path.home()` / `Path(__file__).parent`.

---

## Security & maintenance notes (must read)
- **Hardcoded secret key & AES-ECB**: `objects.py` decodes a base64 secret and uses AES in ECB mode for deterministic encryption of usernames/IDs. ECB is insecure for many use cases; avoid hardcoding keys and prefer authenticated modes (GCM) or use `Fernet` (already imported in helper) for symmetric encryption.
- **Helper overwrites files on every run**: `helper.py` writes empty `{}` to the data JSONs at import-time which will wipe data when the module is imported. Consider creating files only if missing (check `exists()` before writing).
- **Constructors with `input()` calls**: `User.__init__` requests `input()` for missing email/password and `card_register` asks for card balance interactively; constructors should avoid blocking I/O — move interactive prompts outside constructors.
- **No error handling for missing JSON keys / file I/O**: many registry lookups assume well-formed files and keys exist; add try/except and validation.


