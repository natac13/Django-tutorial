from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


# This class needs to be created in order to customize the admin form.

class QuestionAdmin(admin.ModelAdmin):

    # fields = ['pub_date', 'question_text']  # changes ordering of HTML form
    # where below which splits it up into fieldsets.
    fieldset = [
        (None,      {'fields': ['question_text']}),
        ('Date Information', {'fields': ['pub_date']}),
    ]

    # add Choices to the same edit page as Question, therefore these choices
    # will belong via foreign key to the Question.
    inlines = [ChoiceInline]

    # What is displayed on the list out page of Questions
    list_display = ('question_text', 'pub_date', 'was_published_recently')

    # makes a sidebar which dpending on the type of field in the database,
    # Django knows what kind of filters to create. In this case date types.
    list_filter = ['pub_date']

    # add in search fields
    search_fields = ['question_text']

# Register your models here.
# This is the common workflow to have access to the models in the admin form,
# as well as being able to modify the form itself.
admin.site.register(Question, QuestionAdmin)
