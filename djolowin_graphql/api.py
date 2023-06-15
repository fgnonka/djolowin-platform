import graphene
from .account.schema import AccountMutations, AccountQueries

class Mutation(AccountMutations, graphene.ObjectType):
    pass

class Query(AccountQueries, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)