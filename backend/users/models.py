from django.db import models
from django.contrib.auth.models import AbstractUser

USER_FIELD_MAX_LENGTH = 150
USER_EMAIL_FIELD_MAX_LENGTH = 254


class FoodgramUser(AbstractUser):
    email = models.EmailField('Email Address',
                              unique=True,
                              max_length=USER_EMAIL_FIELD_MAX_LENGTH)
    username = models.CharField('Username',
                                unique=True,
                                max_length=USER_FIELD_MAX_LENGTH)
    first_name = models.CharField('First Name',
                                  max_length=USER_FIELD_MAX_LENGTH)
    last_name = models.CharField('Last Name',
                                 max_length=USER_FIELD_MAX_LENGTH)
    password = models.CharField('Password',
                                max_length=USER_FIELD_MAX_LENGTH)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'password', 'first_name', 'last_name')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
