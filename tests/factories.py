import factory


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'app.Post'

    title = factory.Faker('sentence', nb_words=10)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'app.Comment'

    title = factory.Faker('sentence', nb_words=10)
    post = factory.SubFactory(PostFactory)
