from django.contrib.staticfiles import finders
from django.test import TestCase


class TestStatics(TestCase):
    def test_statics(self):
        main_dir = 'resolvers/'
        static_dirs = ('/js/page_resolvers.js', '/css/page_resolvers.css')

        for path in static_dirs:
            full_path = finders.find(main_dir + path)
            self.assertIsNotNone(
                full_path,
                msg=f'Static file {path} not found',
            )
