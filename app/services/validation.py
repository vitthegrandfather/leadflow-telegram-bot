from __future__ import annotations

import re

from app.models.enums import ContactMethod, ServiceCategory


class ValidationError(ValueError):
    pass


NAME_MIN = 2
NAME_MAX = 80
DESCRIPTION_MIN = 10
DESCRIPTION_MAX = 1000
PHONE_MIN_DIGITS = 8
PHONE_MAX_DIGITS = 15


def validate_name(raw: str) -> str:
    name = " ".join((raw or "").split())
    if not NAME_MIN <= len(name) <= NAME_MAX:
        raise ValidationError("Enter a full name using 2–80 characters.")
    if re.search(r"https?://|www\.", name, flags=re.IGNORECASE):
        raise ValidationError("Enter a name, not a link.")
    if not any(ch.isalpha() for ch in name):
        raise ValidationError("Enter a full name using letters.")
    return name


def normalize_phone(raw: str) -> str:
    text = (raw or "").strip()
    if text.startswith("00"):
        text = f"+{text[2:]}"
    digits = re.sub(r"\D", "", text)
    if not PHONE_MIN_DIGITS <= len(digits) <= PHONE_MAX_DIGITS:
        raise ValidationError("Enter a phone number with 8 to 15 digits.")
    return f"+{digits}"


def validate_description(raw: str) -> str:
    text = (raw or "").strip()
    if len(text) < DESCRIPTION_MIN:
        raise ValidationError("Describe the project in at least 10 characters.")
    if len(text) > DESCRIPTION_MAX:
        raise ValidationError("Keep the description under 1,000 characters.")
    return text


def parse_category(value: str) -> ServiceCategory:
    try:
        return ServiceCategory(value)
    except ValueError as exc:
        raise ValidationError("Choose a service from the list.") from exc


def parse_contact_method(value: str) -> ContactMethod:
    try:
        return ContactMethod(value)
    except ValueError as exc:
        raise ValidationError("Choose a contact method from the list.") from exc
