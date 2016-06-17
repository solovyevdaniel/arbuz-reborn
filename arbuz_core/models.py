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

    def get_crimes_total_count(self):
        result = self.bodily_harm_with_fatal_cons + self.brigandage + self.drugs + self.extortion +\
            self.fraud + self.grave_and_very_grave + self.hooliganism + self.intentional_injury + self.looting +\
            self.murder + self.rape + self.theft
        return result


class AdminUserManager(BaseUserManager):
    def create_user(self, first_name=None, last_name=None, middle_name=None, phone_number=None,
                    user_email=None, password=None):
        if not user_email:
            print "Fail"
        print user_email
        if not first_name:
            first_name = ''
        if not last_name:
            last_name = ''
        if not middle_name:
            middle_name = ''
        if not phone_number:
            phone_number = ''
        user = self.model(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            user_email=user_email,
            is_staff=True
        )
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name=None, last_name=None, middle_name=None, phone_number=None,
                    user_email=None, password=None):
        user = self.create_user(first_name, last_name, middle_name, phone_number, user_email, password)
        user.is_admin = True
        user.save()
        return user


class AdminUser(AbstractBaseUser):
    first_name = models.CharField(max_length=256, null=False, default='')
    last_name = models.CharField(max_length=256, null=False, default='')
    user_email = models.EmailField(unique=True, null=False, default='')
    middle_name = models.CharField(max_length=256, null=False, default='')
    phone_number = models.CharField(max_length=52, null=False, default='')
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    is_activated = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = AdminUserManager()

    USERNAME_FIELD = 'user_email'

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name + ' ' + self.middle_name


class CrimeStat(models.Model):
    longitude = models.DecimalField(max_digits=19, decimal_places=15)
    latitude = models.DecimalField(max_digits=19, decimal_places=15)
    crimes_coefficient = models.FloatField()
