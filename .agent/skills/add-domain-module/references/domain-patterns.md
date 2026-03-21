# Domain Module Pattern

A standard module contains:

- `router.py`
- `schemas.py`
- `models.py`
- `service.py`
- `repository.py`
- `repository_sa.py`
- `uow.py`
- matching service tests under `tests/domain/<module>/`

Prefer router-only HTTP concerns, keep business logic in `service.py`, and keep persistence behind repository interfaces.
