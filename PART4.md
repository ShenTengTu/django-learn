PART4
=====

## 建立簡單的表單
在投票應用程序 **detail.html** 建立網頁得表單(使用HTML的`<form>`)：
```html
<h1>{{ question.question_text }}</h1>
{% if error_message %}
    <p><strong>{{ error_message }}</strong></p>
{% endif %}
<form action="{% url 'polls:vote' question.id %}" method="post">
    {% csrf_token %}
    {% for choice in question.choice_set.all %}
        <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
        <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label>
        <br>
    {% endfor %}
    <input type="submit" value="Vote">
</form>
```
- 上面的模板將顯示每個投票問題選擇的單選按鈕。每個單選按鈕的`value`是相關的問題 **choice** 的ID。每個單選按鈕的`name`是 **choice** 。
- 當選擇其中一個單選按鈕並提交表單時，它將發送POST數據`choice=#`，其中`#`是所選 **choice** 的ID。
- 將表單的 **action** 設置為`{％url'polls：vote'search.id％}`，然後設置`method ="post"`。
- 使用`method ="post"`（而不是`method ="get"`）非常重要，因為提交此表單的行為將改變服務器端的資料庫。
-  **forloop.counter** 表示`{% for %}`標籤經過循環的次數。
- 由於POST表單具有修改數據的效果，因此需要擔心跨站點請求偽造(Cross Site Request Forgeries)。Django帶有一個非常易於使用的系統來防範它。簡而言之，所有針對服務器端內部URL的POST表單內都應該使用`{％csrf_token％}`模板標記。

現在，讓我們創建一個Django視圖來處理提交的數據並對其進行處理。

之前在 **polls/urls.py** 創建了一個關於vote的 **URLconf path** ：
```py
path('<int:question_id>/vote/', views.vote, name='vote')
```
還創建了 **vote()** 視圖函數的虛擬實現。現在創建一個實際功能的版本。將以下內容添加到 **polls/views.py** ：
```py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Question, Choice

#...

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
  ```
  -  **request.POST** 是一個類似字典的物件，允許您透過鍵名稱訪問表單提交的數據。在上述情況下，`request.POST['choice']`返回所選選項的ID，資料類型為string。 **request.POST** 值始終是string。
  - 如果POST數據中沒有提供 **choice** ，`request.POST['choice']`將引發 **KeyError** 。
  - 遞增選項票數後，代碼返回 **HttpResponseRedirect** ，讓用戶被重定向到指定的URL。
  - 上述例子中使用了 **reverse()** 函數在 **HttpResponseRedirect** 構造函數中，有助於避免在視圖函數中對URL進行硬編碼。
  - 函數 **reverse()** 給出了想要將控制權傳遞給視圖的名稱以及指向該視圖的URL模式的可變參數。在上述情況下，調用 **reverse()** 將返回一個字符串像是`'/polls/1/results/'`

在用戶投票完成後， **vote()** 視圖會重定向到問題的 **results** 頁面。在results視圖中撰寫：
```py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice

# ...

def results(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'results.html', {'question': question})
```

現在，創建一個 **results.html** 模板：
```html
<h1>{{ question.question_text }}</h1>
<ul>
  {% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
  {% endfor %}
</ul>
<a href="{% url 'polls:detail' question.id %}">再次投票?</a>
```

現在，轉到瀏覽器中的/polls/1/並在問題中投票，應該會看到每次投票時都會更新的結果頁面。如果在未選擇的情況下提交表單，則應該看到錯誤消息。

>  **vote()** 視圖的代碼有一個小問題。它首先從資料庫中獲取`selected_choice`物件，然後計算新的投票值，然後將其保存回數據庫。如果網站的兩個用戶嘗試在同一時間投票，則可能會出錯：他們將檢索相同的值（例如42）進行投票。然後對於兩個用戶新值43被計算並保存，但是期望值將是44。 這被稱為競爭條件。可以閱讀[使用F()來避免競爭條件](https://docs.djangoproject.com/en/2.1/ref/models/expressions/#avoiding-race-conditions-using-f)，以了解如何解決此問題。

## 使用通用視圖
視圖函數 **detail()** 和 **results()** 視圖幾乎完全相同。唯一的區別是模板名稱。而 **index()** 視圖顯示投票問題列表，類似前兩個視圖。這些視圖代表了基本Web開發的常見情況：根據URL中傳遞的參數從數據庫獲取數據，加載模板並返回呈現的模板。因為這是如此常見，Django提供了一種稱為 **通用視圖(generic view)** 系統的快捷方式。

將投票應用程序轉換為使用通用視圖系統，這樣就可以刪除一堆代碼。我們只需要採取一些步驟進行轉換：
- 轉換 **URLconf** 
- 刪除一些舊的，不需要的視圖。
- 採用基於Django通用視圖的新視圖。

### 修改URLconf
首先打開 **polls/urls.py** ，並將URLconf更改為：
```py
from django.urls import path
from . import views

app_name = 'polls' # application namespace
urlpatterns = [
  # path('', views.index, name='index'),
  path('', views.IndexView.as_view(), name='index'), # route , veiw, kwargs, name
  # path('<int:question_id>/', views.detail, name='detail'),
  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
  # path('<int:question_id>/results/', views.results, name='results'),
  path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
  path('<int:question_id>/vote/', views.vote, name='vote'),
]
```
- 第二個和第三個模式的路徑字符串中匹配模式的名稱已從`<int:question_id>`更改為`<int:pk>`。

### 修改視圖
接下來將刪除舊的 **index()** 、 **detail()** 和 **results()** 視圖，並使用Django的通用視圖。為此，請打開 **polls/views.py** 文件並進行更改，如下所示：
```py
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

# ...
```
- 這裡使用兩個通用視圖： **ListView** 和 **DetailView** 。這兩個視圖分別提取出“顯示物件列表”和“顯示特定類型物件的詳細頁面”的概念。
- 每個通用視圖都需要知道它將採用什麼模型。這是使用 **model** 屬性提供的。
-  **DetailView** 通用視圖期望從URL捕獲的主鍵值被稱為 **pk** ，因此已將`question_id`更改為`pk`以獲取通用視圖。
- 默認情況下， **DetailView** 通用視圖使用名為`<app name>/<model name>_detail.html`的模板。 **template_name** 屬性用於告訴Django使用特定的模板名稱( **detail.html** 及 **results.html** )而不是自動生成的默認模板名稱。
- 類似地， **ListView** 通用視圖使用名為`<app name>/<model name>_detail.html`的默認模板；使用 **template_name** 屬性告訴ListView使用我們現有的 **index.html** 模板。
- 對於 **ListView** ，自動生成的上下文(context)變量名稱是 **question_list** 。要覆蓋它，Django提供了 **context_object_name** 屬性，指定我們要使用 **latest_questions** 。

運行服務器，並使用基於通用視圖的新投票應用程序。有關通用視圖的完整詳細信息，請參閱[通用視圖文檔](https://docs.djangoproject.com/en/2.1/topics/class-based-views/)。