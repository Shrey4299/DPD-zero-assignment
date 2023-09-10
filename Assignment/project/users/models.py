from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, password, age, gender, full_name, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, password, age=age, gender=gender, full_name=full_name, **other_fields)

    def create_user(self, email=None, username=None, password=None, age=None, gender=None, full_name=None, **other_fields):
        if not username:
            raise ValueError(_('You must provide a username'))

        email = self.normalize_email(email) if email else None
        user = self.model(email=email, username=username, age=age, gender=gender, full_name=full_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

class RegisterUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=150)
    start_date = models.DateTimeField(default=timezone.now)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'age', 'gender', 'full_name']

    def __str__(self):
        return self.username
