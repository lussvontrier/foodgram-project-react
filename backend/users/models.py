from django.db import models
from django.contrib.auth.models import AbstractUser

USER_FIELD_MAX_LENGTH = 150
USER_EMAIL_FIELD_MAX_LENGTH = 254


class FoodgramUser(AbstractUser):
    email = models.EmailField(
        'Email Address',
        unique=True,
        max_length=USER_EMAIL_FIELD_MAX_LENGTH
    )
    first_name = models.CharField(
        'First Name',
        max_length=USER_FIELD_MAX_LENGTH
    )
    last_name = models.CharField(
        'Last Name',
        max_length=USER_FIELD_MAX_LENGTH
    )
    password = models.CharField(
        'Password',
        max_length=USER_FIELD_MAX_LENGTH
    )
    pub_date = models.DateTimeField(
        verbose_name='Date of creation.',
        auto_now_add=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'password', 'first_name', 'last_name')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        help_text='The user who is subscribing to another user'
    )
    subscribed_to = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='subscribers',
        help_text='The user who is being subscribed to'
    )

    class Meta:
        ordering = ('-subscriber', 'subscribed_to')
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        constraints = [
            models.UniqueConstraint(
                fields=('subscriber', 'subscribed_to'),
                name='unique_name_owner'
            ),
            models.CheckConstraint(
                check=~models.Q(subscriber=models.F('subscribed_to')),
                name='prevent_self_follow')
        ]

    def __str__(self):
        return f"{self.subscriber} subscribes to {self.subscribed_to}"
