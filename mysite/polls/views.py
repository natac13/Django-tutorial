from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

# Views are really the controller in the MVC model. Therefore these can read
# database records, use Django templates, generate PDF, zip or even an XML
# file. Can also use any Python library I want. All views needs to return is
# an HttpResponse() or an exception Http404

# NOTE 9 explains how these classes are created without me doing anything....


class IndexView(generic.ListView):
    model = Question
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions. Not including those
        published in the future."""
        # Question.objects.filter() returns a queryset containing Questions
        # whose published date is less than or equal to (earlier) timezone.now
        # NOTE 11.
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            '-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    # get Question off PRIMARY KEY
    #
    # request.POST is a dictionary-like object which gives me access to the
    # submitted date by referring to it by the name given.
    try:
        selected_choice = q.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        dict_vars = {
            'question': q,
            'error_message': "You didn't select a choice.",
        }
        return render(request, 'polls/detail.html', dict_vars)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return a HttpResponseRedirect after successfully dealing with
        # POST data. NOTE 7. This prevents data from being posted twice if a
        # user hits the Back button.
        #
        # reverse() is used so I do not have to hard code a URL in the views
        # function. It is given the name of the view(assigned in polls/url.py)
        # and the variable portion that it is looking for. It will return
        # something like '/polls/3/resutls'
        # reverse() also allow me to use the name urls instead of hard coding.
        # reverse will recall the page via polls/urls.py which then will call
        # the result function again with given args, or kwargs.
        # With render above it is directly calling the template itself. Were
        # vote() will utilize HttpResposeRedirect() to use the polls/urls.py
        # path instead.
        return HttpResponseRedirect(reverse('polls:results', args=(q.id,)))

# These are the functions that get called by ulr() when it matches the regular
# expression that is given as the first argument.
# The request argument I think has to be there and then the other arguments
# are like question_id get filled by the values from the 'named groups'
# (docs.djangoproject.com/en/1.8/topics/http/urls/). There is more to this
# in the polls/urls.py script.


def index(request):
    """ loads a template called polls/index.html and passes in a context.
    The context is a dictionary mapping template variable names to Python
    objects.
    """

    # I no longer need loader or RequestContext.
    # render() takes the request object, a template name and a dictionary as
    # arguments and will return an HttpResponse of the given template with the
    # given context.
    # The dictionary that is passed to render is how I access the variables in
    # the html template page. That is how I call latest_question_list in
    # index.html
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    """ Gets the question object from database based off the question_id,
    searched by the primary key(pk=).

    Raises a Http404() if the Question objects could not found in the
    database based off the given question_id
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
