import os

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

import django

django.setup()

import random
import string
from datetime import datetime

import pytest

from ad.models import Ad, Review
from users.models import User


# Функция для генерации случайного адреса электронной почты с использованием строчных букв и фиксированного домена.
def generate_random_email():
    letters = string.ascii_lowercase
    username = "".join(random.choice(letters) for i in range(8))
    domain = "mail.ru"
    return f"{username}@{domain}"


# Фикстура для создания пользователя user1 с случайным адресом электронной почты.
@pytest.fixture
def user1():
    email = generate_random_email()
    return User.objects.create(email=email)


# Фикстура для создания пользователя user2 с случайным адресом электронной почты.
@pytest.fixture
def user2():
    email = generate_random_email()
    return User.objects.create(email=email)


# Фикстура для создания объявления, связанного с user1.
@pytest.fixture
def ad_obj(user1):
    return Ad.objects.create(
        title="Test Ad",
        price=100,
        description="Test Description",
        author=user1,
        created_at=datetime.now(),
    )


# Фикстура для создания отзыва, связанного с ad_obj и user2.
@pytest.fixture
def review_obj(ad_obj, user2):
    return Review.objects.create(
        text="Test Review", ad=ad_obj, author=user2, created_at=datetime.now()
    )


# Тест для создания объявления.
def test_create_ad(ad_obj):
    assert Ad.objects.count() == 1


# Тест для просмотра объявления
def test_read_ad(ad_obj):
    ad = Ad.objects.filter(title="Test Ad").first()
    assert ad.price == 100


# Тест для обновления заголовка объявления
def test_update_ad():
    ad = Ad.objects.get(pk=1)
    ad.title = "New Title"
    ad.save()
    updated_ad = Ad.objects.get(pk=1)
    assert updated_ad.title == "New Title"


# Тест для удаления объявления
def test_delete_ad():
    Ad.objects.filter(title="Test Ad").delete()
    assert Ad.objects.filter(title="Test Ad").count() == 0


# Тест для создания отзыва
def test_create_review(review_obj):
    assert Review.objects.count() == 1


# Тест для просмотра отзыва
def test_read_review():
    review = Review.objects.filter(text="Test Review").first()
    assert review.ad.title == "Test Ad"


# Тест для обновления текста отзыва
def test_update_review():
    review = Review.objects.filter(text="Test Review").first()
    review.text = "Updated Review Text"
    review.save()
    updated_review = Review.objects.filter(text="Updated Review Text").first()
    assert updated_review is not None


# Тест для удаления отзыва
def test_delete_review():
    Review.objects.filter(text="Test Review").delete()
    assert Review.objects.filter(text="Test Review").count() == 0
