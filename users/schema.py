import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from users.models import Account as User, Profile

class AuthMutation(graphene.Mutation):
    pass

