# Infra Adapter Pattern

Each adapter should have:

- `abstract.py` for interfaces
- one concrete implementation module
- `memory.py` for tests or local fallback
- dependency wiring in `app/core/dependencies.py`

Keep business code independent from the vendor SDK.
