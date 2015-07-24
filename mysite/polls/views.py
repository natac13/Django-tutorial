from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Question

# Views are really the controller in the MVC model. Therefore these can read
# database records, use Django templates, generate PDF, zip or even an XML
# file. Can also use any Python library I want. All views needs to return is
# an HttpResponse() or an exception Http404

# Create your views here.
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
    response = "You're looking at the results of question {0}."
    return HttpResponse(response.format(question_id))


def vote(request, question_id):
    return HttpResponse("You're voting on question: {0}.".format(question_id))
