import datetime

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase

from .models import Question, Choice

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


def create_question(question_text, days):
    """
    Creates a question with @param 'question_text', published the given
    number of @param 'days' offset from now. (negative for dates in the past
    and positive value for published date set in the future.)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    # shortcut to instantiating the Question object than using the save()
    # method to store in database.
    return Question.objects.create(question_text=question_text, pub_date=time)


def create_choice_for_question(question, choice_text):
    """Creates a Choice for a given Question object."""
    return Choice.objects.create(question=question, choice_text=choice_text)


class QuestionIndexViewsTest(TestCase):
    # NOTE 10  #######

    def test_index_view_with_no_question(self):
        """With no question existing a message should appear instead"""
        # @var response - will set up a client object and run a GET request on
        # the given url. Which reverse() is used so I can use the named urls.
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question(self):
        """Questions with a future date should not be displayed on the index
        page.
        """
        create_question(question_text="Future Question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.",
                            status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_past_question_no_choice(self):
        """Questions with a pub_date in the past should appear in the view"""
        q = create_question(question_text="Past Question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertNotContains(response, q.question_text, status_code=200)

    def test_index_view_with_past_question_with_choice(self):
        """Questions with a pub_date in the past should appear in the view"""
        q = create_question(question_text="Past Question", days=-30)
        create_choice_for_question(question=q, choice_text="Choice P1")
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "Past Question", status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past Question>'])

    def test_index_view_with_future_and_past_question_with_choice(self):
        """Only the past question should appear"""
        q = create_question(question_text="Past Question", days=-30)
        create_choice_for_question(question=q, choice_text="Choice P1")
        create_question(question_text="Future Question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "Past Question", status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past Question>'])

    def test_index_view_with_two_past_questions_one_with_choice(self):
        """Both of the past questions should appear."""
        q = create_question(question_text="Past 1", days=-10)
        create_choice_for_question(question=q, choice_text="Choice P1")
        create_question(question_text="Past 2", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past 1>'])

    def test_index_view_with_two_past_questions_with_choices(self):
        """Both of the past questions should appear."""
        q = create_question(question_text="Past 1", days=-10)
        create_choice_for_question(question=q, choice_text="Choice P1")
        q2 = create_question(question_text="Past 2", days=-30)
        create_choice_for_question(question=q2, choice_text="Choice P2")
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past 1>', '<Question: Past 2>']
                                 )


class QuestionDetailViewTest(TestCase):

    def test_detail_view_with_a_future_question(self):
        """The Detail view that points to a question published in the future
        should have a status_code of 404 NOT FOUND.
        """
        future_question = create_question(question_text="Future", days=20)
        response = self.client.get(reverse('polls:detail',
                                           kwargs={'pk': future_question.id, })
                                   )
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_past_question_no_choice(self):
        """Detail view should display the question_text for any Question in the
        past
        """
        past_question = create_question(question_text="Past", days=-20)
        response = self.client.get(reverse('polls:detail',
                                           kwargs={'pk': past_question.id, })
                                   )
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_past_question_with_choice(self):
        """Detail view should display the question_text for any Question in the
        past
        """
        past_question = create_question(question_text="Past", days=-20)
        c = create_choice_for_question(question=past_question,
                                       choice_text="Choice P1")
        response = self.client.get(reverse('polls:detail',
                                           kwargs={'pk': past_question.id, })
                                   )
        self.assertContains(response, past_question.question_text,
                            status_code=200)
        self.assertContains(response, c.choice_text)


class QuestionResultsViewTest(TestCase):

    def test_results_view_with_a_future_question(self):
        """The results view that points to a question published in the future
        should have a status_code of 404 NOT FOUND.
        """
        future_question = create_question(question_text="Future", days=20)
        response = self.client.get(reverse('polls:results',
                                           kwargs={'pk': future_question.id, })
                                   )
        self.assertEqual(response.status_code, 404)

    def test_results_view_with_past_question_no_choice(self):
        """results view should display the question_text for any Question in the
        past
        """
        past_question = create_question(question_text="Past", days=-20)
        response = self.client.get(reverse('polls:results',
                                           kwargs={'pk': past_question.id, })
                                   )
        self.assertEqual(response.status_code, 404)

    def test_results_view_with_past_question_with_choice(self):
        """results view should display the question_text for any Question in the
        past
        """
        past_question = create_question(question_text="Past", days=-20)
        c = create_choice_for_question(question=past_question,
                                       choice_text="Choice P1")
        response = self.client.get(reverse('polls:results',
                                           kwargs={'pk': past_question.id, })
                                   )
        self.assertContains(response, past_question.question_text,
                            status_code=200)
        self.assertContains(response, c.choice_text)

    def test_results_view_with_past_question_with_two_choices(self):
        """results view should display the question_text for any Question in the
        past
        """
        past_question = create_question(question_text="Past", days=-20)
        c1 = create_choice_for_question(question=past_question,
                                        choice_text="Choice P1")
        c2 = create_choice_for_question(question=past_question,
                                        choice_text="Choice P2")
        response = self.client.get(reverse('polls:results',
                                           kwargs={'pk': past_question.id, })
                                   )
        self.assertContains(response, past_question.question_text,
                            status_code=200)
        self.assertContains(response, c1.choice_text)
        self.assertContains(response, c2.choice_text)
