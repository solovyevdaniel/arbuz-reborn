from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.utils import timezone


class Building(models.Model):
    street = models.CharField(max_length=100)
    number = models.IntegerField()
    longitude = models.DecimalField(max_digits=19, decimal_places=15)
    latitude = models.DecimalField(max_digits=19, decimal_places=15)
    quadkey = models.FloatField(db_index=True)


class Crimes(models.Model):
    building_id = models.ForeignKey(Building, related_name='crimes')
    year_month = models.DateField(max_length=8)
    total = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    bodily_harm_with_fatal_cons = models.IntegerField(default=0)
    brigandage = models.IntegerField(default=0)
    drugs = models.IntegerField(default=0)
    extortion = models.IntegerField(default=0)
    fraud = models.IntegerField(default=0)
    grave_and_very_grave = models.IntegerField(default=0)
    hooliganism = models.IntegerField(default=0)
    intentional_injury = models.IntegerField(default=0)
    looting = models.IntegerField(default=0)
    murder = models.IntegerField(default=0)
    rape = models.IntegerField(default=0)
    theft = models.IntegerField(default=0)


class AdminUserManager(BaseUserManager):
    def create_user(self, first_name=None, last_name=None, middle_name=None, phone_number=None,
                    user_email=None, password=None):
        if not first_name or not last_name or not middle_name or not phone_number or not user_email:
            raise ValueError("All fields are required")
        user = self.model(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            user_email=user_email
        )
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name=None, last_name=None, middle_name=None, phone_number=None,
                    user_email=None, password=None):
        user = self.create_user(first_name, last_name, middle_name, phone_number, user_email, password)
        return user


class AdminUser(AbstractUser):
    user_email = models.EmailField(unique=True)
    middle_name = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=52)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    send_date = models.DateTimeField(default=timezone.now)

    objects = AdminUserManager()

    USERNAME_FIELD = 'user_email'