from django.contrib import admin

from users.models import FoodgramUser, Subscription


@admin.register(FoodgramUser)
class FoodgramUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')
    list_filter = ('email', 'username')
    search_fields = ('id', 'username')
    ordering = ('id',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'subscriber', 'subscribed_to')
    list_filter = ('subscriber', 'subscribed_to')
    search_fields = ('subscriber', 'subscribed_to')
    ordering = ('id',)
