from datetime import timedelta
from typing import List

import factory
from django.utils import timezone
from factory.base import T


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'app.Post'

    title = factory.Faker('sentence', nb_words=10)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'app.Comment'

    title = factory.Faker('sentence', nb_words=10)
    post = factory.SubFactory(PostFactory)

    created_at = factory.Faker('date_time')

    @classmethod
    def create_batch(cls, size: int, **kwargs) -> List[T]:
        # We need to add some time gap in each `created_at`
        # to properly test comments with different `created_at` fields,
        # because factory_boy creates instances instantly with delay of milliseconds.
        with_delay = kwargs.pop('with_delay', False)
        if with_delay:
            objs = []
            current_time = timezone.now()
            for _ in range(size):
                current_time += timedelta(minutes=10)  # May it be 10 minutes
                kwargs['created_at'] = current_time
                objs.append(cls.create(**kwargs))
            return objs

        return super().create_batch(size=size, **kwargs)
