from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser

class CustomUserManager(AbstractBaseUser):
    def create_user(self, username, email=None, password=None, date_of_birth=None, profile_photo=None, **other_fiels):
        if not username:
            raise ValueError("Users must have a username.")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, password=password, date_of_birth=date_of_birth, profile_photo=profile_photo, **other_fiels)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, email=None, password=None, **extra_fiels):
        extra_fiels.setdefault("is_staff", True)
        extra_fiels.setdefault("is_superuser", True)
        extra_fiels.setdefault("is_active", True)

        if extra_fiels.get('is_staff') is not True:
            raise ValueError("superuser must have is_staff=True")
        
        if extra_fiels.get('is_superuser') is not True:
            raise ValueError("superuser must have is_superuser=True")
        
        return self.create_user(username=username, email=email, password=password, **extra_fiels)


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to="static/", null=True, blank=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username
