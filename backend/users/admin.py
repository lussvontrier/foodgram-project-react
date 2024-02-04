from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from users.models import FoodgramUser, Subscription


@admin.register(FoodgramUser)
class FoodgramUserAdmin(UserAdmin):
    list_display = (
        'id', 'username', 'email', 'first_name',
        'last_name', 'pub_date'
    )
    list_filter = ('email', 'username')
    search_fields = ('id', 'username')
    ordering = ('-pub_date',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'subscriber', 'subscribed_to')
    list_filter = ('subscriber', 'subscribed_to')
    search_fields = ('subscriber', 'subscribed_to')
    ordering = ('subscriber', 'subscribed_to')


admin.site.unregister(Group)
