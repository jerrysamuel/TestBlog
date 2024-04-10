import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from content.models import BlogPost
import graphql_jwt
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    # password_set = mutations.PasswordSet.Field() # For passwordless registration
    password_change = mutations.PasswordChange.Field()
    update_account = mutations.UpdateAccount.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    send_secondary_email_activation =  mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()
    remove_secondary_email = mutations.RemoveSecondaryEmail.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()


class BlogPostType(DjangoObjectType):
    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'subTitle', 'body', 'dateCreated')
    

class CreatePostMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        subTitle = graphene.String()
        body = graphene.String()

    post = graphene.Field(BlogPostType)

    def mutate(self, info, title, subTitle, body):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in to create a post.")

        post = BlogPost(title=title, subTitle=subTitle, body=body, author=user)
        post.save()
        return CreatePostMutation(post=post)

class DeletePostMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()

    def mutate(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in to delete a post.")

        try:
            post = BlogPost.objects.get(pk=id)
        except BlogPost.DoesNotExist:
            raise GraphQLError("Post does not exist.")

        if post.author != user:
            raise GraphQLError("You are not authorized to delete this post.")

        post.delete()
        return DeletePostMutation(message="Post deleted successfully.")

class UpdatePostMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        subTitle = graphene.String()
        body = graphene.String()

    message = graphene.String()
    post = graphene.Field(BlogPostType)

    def mutate(self, info, id, title, subTitle, body):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in to update a post.")

        try:
            post = BlogPost.objects.get(pk=id)
        except BlogPost.DoesNotExist:
            raise GraphQLError("Post does not exist.")

        if post.author != user:
            raise GraphQLError("You are not authorized to update this post.")

        post.title = title
        post.subTitle = subTitle
        post.body = body
        post.save()

        return UpdatePostMutation(post=post, message="Post updated successfully.")

class Query(UserQuery, MeQuery, graphene.ObjectType):
    blogPosts = graphene.List(BlogPostType)
    post = graphene.Field(BlogPostType, id=graphene.ID())

    def resolve_blogPosts(self, info):
        return BlogPost.objects.all()

    def resolve_post(self, info, id):
        return BlogPost.objects.get(pk=id)

class Mutation(AuthMutation, graphene.ObjectType):
    create_post = CreatePostMutation.Field()
    delete_post = DeletePostMutation.Field()
    update_post = UpdatePostMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
