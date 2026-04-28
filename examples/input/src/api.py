"""User registration API."""


def register_user(email: str, name: str) -> dict:
    # TODO: integrate EmailValidator per openspec/changes/add-email-validation/design.md task 3.2
    return {"email": email, "name": name, "status": "registered"}
