from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель Пользователя"""

    USER = "user"
    ADMIN = "admin"

    ROLE_CHOICES = [
        (USER, "User"),
        (ADMIN, "Admin"),
    ]
    username = None
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(choices=ROLE_CHOICES, default=USER)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    token = models.CharField(
        max_length=100, verbose_name="Token", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
