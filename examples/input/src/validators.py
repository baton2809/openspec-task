"""Email validation module — to be implemented per design.md."""


class EmailValidator:
    """Validates email format via regex. See openspec/changes/add-email-validation/design.md."""

    def validate(self, email: str) -> bool:
        raise NotImplementedError(
            "See openspec/changes/add-email-validation/design.md — Интерфейсы / Контракты"
        )
