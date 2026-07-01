import pytest
from pydantic import ValidationError

from app.schemas.user import UserCreate


def test_password_corta_se_rechaza():

    with pytest.raises(ValidationError):
        UserCreate(email="abc@example.com", password="corta")


def test_password_valida_se_acepta():

    user = UserCreate(email="abc@example.com", password="password_segura")
    assert user.email == "abc@example.com"
    assert user.password == "password_segura"
