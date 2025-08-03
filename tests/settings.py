SECRET_KEY = '0JC0-AJSF0-J10U291U20FJFJASOJFAOSJGO1U(UJA9'
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'tests.app',
    'django_page_resolver',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            # ... some options here ...
        },
    },
]

USE_TZ = False
