import graphene
from graphene_django import DjangoObjectType

from account.models import CustomUser

from .mutations.account import CreateCustomUser, UpdateCustomUser, DeleteCustomUser
from .types import CustomUserType


class AccountQueries(graphene.ObjectType):
    """Queries for Account"""

    account = graphene.Field(CustomUserType, id=graphene.Int(required=True))
    all_accounts = graphene.List(CustomUserType)

    def resolve_account(self, info, id):
        """Get account by id"""
        return CustomUser.objects.get(id=id)

    def resolve_all_accounts(self, info, **kwargs):
        """Get all accounts"""
        return CustomUser.objects.all()


class AccountMutations(graphene.ObjectType):
    """Mutations for Account"""
    create_account = CreateCustomUser.Field()
    update_account = UpdateCustomUser.Field()
    delete_account = DeleteCustomUser.Field()


schema = graphene.Schema(query=AccountQueries, mutation=AccountMutations)
