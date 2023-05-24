from django.db import models
from django.db.models import TextChoices


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


# id,first_name,last_name,username,password,role,age,location_id
class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    role = models.CharField(max_length=10, choices=UserRoles.choices, default=UserRoles.MEMBER)
    age = models.PositiveSmallIntegerField()
    locations = models.ManyToManyField(Location)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
