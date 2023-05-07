import graphene
from graphene_django import DjangoObjectType
from djolowin_graphql.account.types import CustomUserType

from account.models import CustomUser


class CustomUserInput(graphene.InputObjectType):
    """Base Input for Account"""

    id = graphene.GlobalID()
    email = graphene.String()
    username = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()

    last_login = graphene.DateTime()
    date_joined = graphene.DateTime()
    updated_at = graphene.DateTime()
    is_staff = graphene.Boolean()
    is_active = graphene.Boolean()
    is_superuser = graphene.Boolean()


class CreateCustomUser(graphene.Mutation):
    """Mutation to create a CustomUser"""

    class Arguments:
        user_data = CustomUserInput(required=True)

    customuser = graphene.Field(CustomUserType)

    @staticmethod
    def mutate(root, info, user_data=None):
        user_instance = CustomUser(
            email=user_data.email,
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            last_login=user_data.last_login,
            date_joined=user_data.date_joined,
            updated_at=user_data.updated_at,
            is_staff=user_data.is_staff,
            is_active=user_data.is_active,
            is_superuser=user_data.is_superuser,
        )
        user_instance.save()
        return CreateCustomUser(customuser=user_instance)


class UpdateCustomUser(graphene.Mutation):
    """Mutation to update a CustomUser"""

    class Arguments:
        user_data = CustomUserInput(required=True)

    customuser = graphene.Field(CustomUserType)

    @staticmethod
    def mutate(root, info, user_data=None):
        user_instance = CustomUser.objects.get(pk=user_data.id)
        if user_instance:
            user_instance.email = user_data.email
            user_instance.username = user_data.username
            user_instance.first_name = user_data.first_name
            user_instance.last_name = user_data.last_name
            user_instance.last_login = user_data.last_login
            user_instance.date_joined = user_data.date_joined
            user_instance.updated_at = user_data.updated_at
            user_instance.is_staff = user_data.is_staff
            user_instance.is_active = user_data.is_active
            user_instance.is_superuser = user_data.is_superuser
            user_instance.save()
            return UpdateCustomUser(customuser=user_instance)
        return UpdateCustomUser(customuser=None)


class DeleteCustomUser(graphene.Mutation):
    """Mutation to delete a CustomUser"""

    class Arguments:
        id = graphene.ID()

    customuser = graphene.Field(CustomUserType)

    @staticmethod
    def mutate(root, info, id):
        user_instance = CustomUser.objects.get(pk=id)
        user_instance.delete()
        return None
