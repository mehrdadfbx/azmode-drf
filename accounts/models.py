from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
        #create normal user
        def create_user(self, username, password=None, **extra_fields):
            if not username:
                raise ValueError('user not be null')

            user = self.model(username = username, **extra_fields)
            user.set_password(password)
            user.save(using= self._db)
            return user

        def create_superuser(self, username, password=None, **extra_fields):
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)
            extra_fields.setdefault('is_admin', True)

            if extra_fields.get('is_staff') is not True:
                raise ValueError('Superuser must have is_staff=True.')
            if extra_fields.get('is_superuser') is not True:
                raise ValueError('Superuser must have is_superuser=True.')

            return self.create_user(username, password, **extra_fields)

        

class User(AbstractBaseUser, PermissionsMixin):
    username    = models.CharField(max_length=150, unique=True)
    email       = models.EmailField(max_length=255, null=True, blank=True)
    phone       = models.CharField(max_length=20)
    is_admin    = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  # فیلدهایی که createsuperuser علاوه بر username و password می‌پرسه

    def __str__(self):
        return self.username
    