from django.db import models
from enum import Enum
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Permission
from ..authorization.models import Role
from django.conf import settings


GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]


class UserManager(BaseUserManager):

    def create_superuser(self, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    # user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    phone_number = models.CharField(max_length=20, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    roles = models.ManyToManyField(
        Role, db_table='user_roles_map', related_name='users')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_role(self, role_name):
        return self.roles.filter(name=role_name).exists()

    def has_permission(self, permission):
        return self.roles.filter(permissions__codename=permission).exists()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = "user"


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_constraint=True, db_column='user_id'),
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', null=True, blank=True)
    about = models.TextField(_(
        'about'), max_length=500, null=True, blank=True)
    date_modified = models.DateTimeField(User, auto_now=True)

    class Meta:
        db_table = "user_profile"

    def __str__(self):
        return self.user.email


class Address(models.Model):   
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses', db_constraint=True)
    
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    date_modified = models.DateTimeField(User, auto_now=True)

    class Meta:
        db_table = "user_addresses"

    def __str__(self):
        return f"{self.user.username}'s Address: {self.address_line1}, {self.city}, {self.state}, {self.postal_code}"
