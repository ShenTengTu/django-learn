from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic # 通用View
from .models import Question, Choice

# Create your views here.
'''
def index(request):
  latest_questions = Question.objects.order_by('pub_date')[:5]
  context = {
    'latest_questions': latest_questions,
  }
  return render(request, 'index.html', context)
'''
class IndexView(generic.ListView):
  template_name = 'index.html'
  context_object_name = 'latest_questions'

  def get_queryset(self):
    '''返回最近發布的五個問題。'''
    return Question.objects.order_by('pub_date')[:5]

'''
def detail(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'detail.html', {'question': question})
'''
class DetailView(generic.DetailView):
  model = Question
  template_name = 'detail.html'

'''
def results(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'results.html', {'question': question})
'''
class ResultsView(generic.DetailView):
  model = Question
  template_name = 'results.html'

def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    # 當異常發生時重新顯示問題投票表單及顯示錯誤訊息
    return render(request, 'detail.html', {
      'question': question,
      'error_message': '你沒有選擇一個選項'
    })
  else:
    # 增加選項票數並儲存到資料庫
    selected_choice.votes += 1
    selected_choice.save()
    # 成功處理POST數據後，始終返回HttpResponseRedirect。
    # 如果用戶點擊瀏覽器的“上一頁”按鈕，這可以防止數據被發布兩次。
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))