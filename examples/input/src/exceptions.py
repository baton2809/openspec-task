"""Custom exceptions for the registration API."""


class EmailValidationError(Exception):
    """Raised when email is empty, None, or has invalid format."""
    pass
