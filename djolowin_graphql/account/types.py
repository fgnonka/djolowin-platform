import graphene
from graphene_django import DjangoObjectType

from django.contrib.auth import get_user_model
from graphene import relay
from promise import Promise

from account import models


class AddressType(DjangoObjectType):
    class Meta:
        description = "Represents user address data."
        model = models.Address
        fields = "__all__"


class CustomUserType(DjangoObjectType):
    class Meta:
        description = "Represents user data."
        model = models.CustomUser
        fields = "__all__"
