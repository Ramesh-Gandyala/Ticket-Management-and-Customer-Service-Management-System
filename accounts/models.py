
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    email = models.EmailField(
        unique=True,
        max_length=255
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    is_email_verified = models.BooleanField(
        default=False
    )

    google_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username
