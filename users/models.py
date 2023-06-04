import datetime

from django.db import models
from django.db.models import TextChoices
from django.contrib.auth.models import AbstractUser

from users.validators import check_birth, check_domains


class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    lon = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return self.name


class UserRoles(TextChoices):
    MEMBER = "member", "Пользователь"
    MODERATOR = "moderator", "Модератор"
    ADMIN = "admin", "Администратор"


class User(AbstractUser):
    role = models.CharField(max_length=10, choices=UserRoles.choices, default=UserRoles.MEMBER)
    age = models.PositiveSmallIntegerField(null=True)
    locations = models.ManyToManyField(Location)
    birth_date = models.DateField(null=True, validators=[check_birth])
    email = models.EmailField(validators=[check_domains], unique=True)

    def save(self, *args, **kwargs):
        self.set_password(raw_password=self.password)
        today = datetime.date.today()
        if self.birth_date:
            self.age = (today.year - self.birth_date.year - 1) + (
                    (today.month, today.day) >= (self.birth_date.month, self.birth_date.day))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
