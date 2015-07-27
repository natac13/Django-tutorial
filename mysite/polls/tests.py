import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Question

# I run in the terminal `python manage.py test polls`, it look for a subclass
# of the django.test.TestCase class, creates a special testing database.
# Then looks for methods that start with "test"


class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_date(self):
        """Will create a Question object with a day in the future"""

        time = timezone.now() + datetime.timedelta(days=30)
        test_case = Question(pub_date=time)
        self.assertEqual(test_case.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=30)
        test_case = Question(pub_date=time)
        self.assertEqual(test_case.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=2)
        test_case = Question(pub_date=time)
        self.assertEqual(test_case.was_published_recently(), True)
