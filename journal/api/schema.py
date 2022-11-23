import graphene

from graphene_django import DjangoObjectType, DjangoListField
from .models import Post


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = "__all__"


class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    post = graphene.Field(PostType, post_id=graphene.Int())

    def resolve_all_posts(self, info, **kwargs):
        return Post.objects.all()

    def resolve_post(self, info, post_id):
        return Post.objects.get(pk=post_id)


class PostInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    body = graphene.String()
    date = graphene.DateTime()


class CreatePost(graphene.Mutation):
    class Arguments:
        post_data = PostInput(required=True)

    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, post_data=None):
        post_instance = Post(
            title=post_data.title,
            body=post_data.body,
            date=post_data.date,
        )
        post_instance.save()
        return CreatePost(post=post_instance)


class UpdatePost(graphene.Mutation):
    class Arguments:
        post_data = PostInput(required=True)

    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, post_data=None):

        post_instance = Post.objects.get(pk=post_data.id)

        if post_instance:
            post_instance.title = post_data.title
            post_instance.dody = post_data.body
            post_instance.date = post_data.date
            post_instance.save()

            return UpdatePost(post=post_instance)
        return UpdatePost(post=None)


class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, id):
        post_instance = Post.objects.get(pk=id)
        post_instance.delete()

        return None


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
