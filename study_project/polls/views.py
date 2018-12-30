from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Question

# Create your views here.
def index(request):
  latest_questions = Question.objects.order_by('pub_date')[:5]
  context = {
    'latest_questions': latest_questions,
  }
  return render(request, 'index.html', context)

def detail(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'detail.html', {'question': question})

def results(request, question_id):
  response = '問題{:d}結果'.format(question_id)
  return HttpResponse(response)

def vote(request, question_id):
  response = '問題{:d}投票'.format(question_id)
  return HttpResponse(response)