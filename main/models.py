from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager


# Create your models here.
class CustomUser(AbstractUser):
    USERTYPE_CHOICES = [
        ("conductor", "Conductor"),
        ("owner", "Owner"),
        ("admin", "Admin"),
    ]
    usertype = models.CharField(
        max_length=30, choices=USERTYPE_CHOICES, blank=True, null=True
    )

    def __str__(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return super().__str__()


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(username, password, **extra_fields)


class Bus(models.Model):
    bus_number = models.CharField(max_length=30)
    conductor = models.OneToOneField(CustomUser, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.bus_number


class Record(models.Model):
    recorder = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    bus = models.ForeignKey(Bus, null=True, on_delete=models.SET_NULL)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    income = models.FloatField()
    expense = models.FloatField()
