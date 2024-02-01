from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from users.models import FoodgramUser, Subscription
from api.serializers import FoodgramUserSerializer, SubscriptionSerializer
from api.pagination import CustomPageNumberPagination


class FoodgramUserViewSet(UserViewSet):
    queryset = FoodgramUser.objects.all()
    serializer_class = FoodgramUserSerializer
    pagination_class = CustomPageNumberPagination

    @action(detail=True, methods=('post', 'delete'),
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id):
        subscriber = request.user
        subscription_target = get_object_or_404(FoodgramUser, pk=id)

        if subscriber == subscription_target:
            raise ValidationError({'error': 'Cannot subscribe to yourself'})

        if request.method == 'POST':
            if Subscription.objects.filter(
                    subscriber=subscriber,
                    subscribed_to=subscription_target).exists():
                raise ValidationError({'error': 'Subscription already exists'})

            serializer = SubscriptionSerializer(
                subscription_target, context={'request': request}
            )
            Subscription.objects.create(subscriber=subscriber,
                                        subscribed_to=subscription_target)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            subscription = Subscription.objects.filter(
                subscriber=subscriber, subscribed_to=subscription_target
            ).first()

            if not subscription:
                raise ValidationError({'error': 'Subscription does not exist'})

            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        current_user = request.user
        subscriptions = FoodgramUser.objects.filter(
            subscribers__subscriber=current_user)
        page = self.paginate_queryset(subscriptions)
        serializer = SubscriptionSerializer(page,
                                            many=True,
                                            context={'request': request})
        return self.get_paginated_response(serializer.data)
