import datetime

from django.db import models
from django.utils import timezone
"""Each model is being represented by a class which is a subclass of
models.Model. The variables of these classes are to become database field.
Each field is an instance of the some class Field which can be CharField,
EmailField, DateTimeField, and so on. Some can have required parameters.
"""


class Question(models.Model):

    # These become the attributes of the class.
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """ Returns true if the pub_date is within a day"""

        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    # These are method attributes which help Django display on the admin
    # page.
    # be careful of the indent
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):

    # These become the attributes of the class.
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
