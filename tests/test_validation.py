import pytest

from app.services.validation import (
    ValidationError,
    normalize_phone,
    validate_description,
    validate_name,
)


def test_validate_name_accepts_letters() -> None:
    assert validate_name("  Maya   Chen ") == "Maya Chen"


def test_validate_name_rejects_short() -> None:
    with pytest.raises(ValidationError):
        validate_name("A")


def test_validate_name_rejects_urls() -> None:
    with pytest.raises(ValidationError):
        validate_name("https://example.com")


def test_validate_name_requires_letters() -> None:
    with pytest.raises(ValidationError):
        validate_name("123456")


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("+1 (415) 555-0114", "+14155550114"),
        ("00491511234567", "+491511234567"),
        ("380501112233", "+380501112233"),
    ],
)
def test_normalize_phone(raw: str, expected: str) -> None:
    assert normalize_phone(raw) == expected


def test_normalize_phone_rejects_short() -> None:
    with pytest.raises(ValidationError):
        normalize_phone("12345")


def test_description_bounds() -> None:
    with pytest.raises(ValidationError):
        validate_description("too short")
    long_text = "x" * 1001
    with pytest.raises(ValidationError):
        validate_description(long_text)
    assert validate_description("Need a brochure site with a contact form.")
