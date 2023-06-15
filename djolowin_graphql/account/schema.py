import graphene
from graphql_auth.schema import UserQuery, MeQuery

from .mutations import AuthMutation
from .types import CustomUserType, AddressType
from .resolvers import Resolvers


class AccountQueries(UserQuery, MeQuery, graphene.ObjectType, Resolvers):
    """Queries for Account"""

    user = graphene.Field(CustomUserType, id=graphene.Int(required=True))
    users_by_joined_date = graphene.List(
        CustomUserType, date_joined=graphene.Date(required=True)
    )
    address = graphene.Field(AddressType, id=graphene.Int(required=True))
    all_users = graphene.List(CustomUserType)
    all_staff = graphene.List(CustomUserType)
    all_addresses = graphene.List(AddressType)


class AccountMutations(AuthMutation, graphene.ObjectType):
    """Mutations for Account"""

    pass


schema = graphene.Schema(query=AccountQueries, mutation=AccountMutations)
