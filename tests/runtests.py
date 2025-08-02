import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
django.setup()

if __name__ == '__main__':
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['tests'])
    sys.exit(bool(failures))
