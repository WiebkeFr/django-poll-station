from django.shortcuts import render
# replaces: loader.get_template and template.render
from django.shortcuts import get_object_or_404
# replaces: try and except Question.DoesNotExist

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'

def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()
    summed_votes = sum([choice.votes for choice in choices])
    updated_choices = [{"choice_text": choice.choice_text, "votes": choice.votes, "relative_votes": round(choice.votes / all_votes * 100)} for choice in choices]
    return render(request, "polls/results.html", {"question": question, "choices": updated_choices})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/details.html", {"question": question, "error": "You didn't select a value."})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("results", args= (question_id,)))