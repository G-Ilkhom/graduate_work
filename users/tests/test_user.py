import os

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
import django

django.setup()
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


# Регистрация пользователя
@pytest.mark.django_db
def test_user_registration_valid(client):
    url = reverse("users:register")
    data = {
        "email": "test@example.com",
        "password": "testpassword",
        "first_name": "Test",
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# Подтверждение почты
@pytest.mark.django_db
def test_email_confirmation_valid(client):
    url = reverse("users:email_confirm", kwargs={"token": "valid_token"})
    response = client.get(url)
    assert response.status_code == status.HTTP_302_FOUND


# Вход в учетную запись
@pytest.mark.django_db
def test_user_login_valid(client):
    url = reverse("users:login")
    data = {
        "email": "test@example.com",
        "password": "testpassword",
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# Выход
@pytest.mark.django_db
def test_user_logout_valid(client):
    url = reverse("users:logout")
    response = client.post(url)
    assert response.status_code == status.HTTP_302_FOUND


# Подтверждение сброса пароля
@pytest.mark.django_db
def test_reset_password_confirm_valid(client):
    url = reverse("users:reset_password_confirm")
    data = {
        "new_password": "newpassword",
        "token": "valid_token",
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
