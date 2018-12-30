PART3
=====

## 概觀
視圖(View)是Django應用程序中Web頁面的“類型”，通常用於特定功能並具有特定模板。在投票應用程序中，我們將有以下四種視圖： 
- Question index頁面：顯示最新的幾個問題。
- Question detail頁面：顯示問題文本，沒有結果，但有一個表單可以投票。
- Question result頁面：顯示特定問題的結果。
- Vote action：處理特定問題中特定選擇的投票。

在Django中，網頁和其他內容由視圖提供。每個視圖都由一個簡單的Python函數（或基於類別的視圖的方法）表示。 Django將通過檢查所請求的URL（確切地說，是域名後面的URL部分）來選擇視圖。

為了從URL到視圖，Django使用**URLconfs**將URL模式映射到視圖。(官方說明：[URL dispatcher](https://docs.djangoproject.com/en/2.1/topics/http/urls/))

## 路由(Routing)
```py
from django.urls import path

from . import views

urlpatterns = [
  path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail),
]
```
- 要從URL捕獲數值，請使用尖括號定義路由參數。
- 路由參數可以選擇轉換器類型。例如，使用`<int:year>`捕獲整數參數。如果未包含轉換器，則匹配除`/`字符之外的任何字符串。
- 沒有必要添加前導斜杠。用`articles` 而不是`/articles`
- **/articles/2003/03/building-a-django-site/** 會調用函數：
  ```py
  views.article_detail(request，year= 2003, month= 3, slug='building-a-django-site')
  ```

## 開始撰寫視圖
根據上述列出的四種視圖，在 **polls/views.py** 定義視圖函數：
```py
from django.http import HttpResponse

# Create your views here.
def index(request):
  return HttpResponse('投票首頁')

def detail(request, question_id):
  response = '問題{:d}詳細文本'.format(question_id)
  return HttpResponse(response)

def results(request, question_id):
  response = '問題{:d}結果'.format(question_id)
  return HttpResponse(response)

def vote(request, question_id):
  response = '問題{:d}投票'.format(question_id)
  return HttpResponse(response)
```

通過添加以下調用 **path()** 將這些新視圖連接到 **polls.urls** 模組：
```py
from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'), # route , veiw, kwargs, name
  path('<int:question_id>/', views.detail, name='detail'),
  path('<int:question_id>/results/', views.results, name='results'),
  path('<int:question_id>/vote/', views.vote, name='vote'),
]
```

使用`python manage.py runserver`啟動server並用瀏覽器嘗試連結(假設本地網域為`http://127.0.0.1:8000`)：
- `http://127.0.0.1:8000/polls/` : 投票首頁
- `http://127.0.0.1:8000/polls/0/` : 問題0詳細文本
- `http://127.0.0.1:8000/polls/0/results/` : 問題0結果
- `http://127.0.0.1:8000/polls/0/vote/` : 問題0投票

## 寫出實際做某事的視圖
每個視圖負責執行以下兩項操作之一：返回包含所請求頁面內容的 **HttpResponse** 物件，或者引發 **Http404** 等異常。剩下的由開發者決定。
- 可以讀取數據庫中的記錄
- 可以使用模板系統
- 以生成PDF文件，輸出XML，動態創建ZIP文件...

這裡有一個新的 **index()** 視圖，將根據 **Question** 發布日期顯示系統中最新的5個投票問題，並用逗號分隔：
```py
from django.http import HttpResponse
from .models import Question

# Create your views here.
def index(request):
  latest_questions = Question.objects.order_by('pub_date')[:5]
  output = ', '.join([q.question_text for q in latest_questions])
  return HttpResponse(output)
```
- 這裡存在一個問題：頁面的設計在視圖中是硬編碼的。如果要更改頁面的外觀，則必須編輯此Python代碼。

## 使用Django模板系統
Django模板系統通過創建視圖可以使用的模板(Template)將頁面設計與Python代碼分離。

首先，在**polls**目錄中創建一個名為 **templates** 的目錄。 Django會在 **templates** 目錄尋找模板檔案。

Project的 **TEMPLATES** 設置描述了Django如何加載和呈現模板。默認設置文件配置一個 **DjangoTemplates** 後端，其 **APP_DIRS** 選項設置為`True`。按照慣例， **DjangoTemplates** 在每個 **INSTALLED_APPS** 中查找templates子目錄。

在剛剛創建的 **polls/templates** 目錄中創建一個名為 **index.html** 的文件。換句話說，模板應位於 **polls/templates/index.html** 。由於 **app_directories** 模板加載器的工作方式如上所述，您可以將Django中的此模板簡單地稱為`index.html`。

在 **polls\templates\index.html** 定義模板結構：
```html
{% if latest_questions %}
    <ul>
    {% for question in latest_questions %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```
- 模板系統使用dot-lookup語法來訪問變量屬性。
- `{% if %} ... {% endif %}`中，從上下文(context)查找 **latest_questions** 列表是否存在。
- 使用`{% for %} ... {% endfor %}`來迭代 **latest_questions** 列表。
- 在`{{question.question_text}}`中，從 **question** 物件查找 **question_text** 屬性。
-  (官方說明：[template guide](https://docs.djangoproject.com/en/2.1/topics/templates/))

現在更新 **polls/views.py** 中的 **index()** 視圖以使用 **index.html** 模板：
```py
from django.http import HttpResponse
from django.template import loader
from .models import Question

# Create your views here.
def index(request):
  latest_questions = Question.objects.order_by('pub_date')[:5]
  template = loader.get_template('index.html')
  context = {
    'latest_questions': latest_questions,
  }
  return HttpResponse(template.render(context, request))
```
- **django.template.loader** 加載 **index.html** 模板並傳遞上下文(context)給模板。
- 上下文(context)是將模板中的變數名稱映射到Python的字典。
- 通過將瀏覽器指向 **/polls/** 來加載頁面，您應該會看到一個項目符號列表，其中包含從資料庫查詢出來的投票問題文本。

### render()函數
加載模板並傳遞上下文，並使將模板的呈現結果返回 **HttpResponse** 物件是一種非常常見的習慣用法。Django提供了 **render()** 函數的捷徑。以下是重寫的完整 **index()** 視圖：
```py
from django.shortcuts import render
from .models import Question

# Create your views here.
def index(request):
  latest_questions = Question.objects.order_by('pub_date')[:5]
  context = {
    'latest_questions': latest_questions,
  }
  return render(request, 'index.html', context)
```
- 一旦在所有視圖中使用 **render()** ，就不再需要導入 **loader** 和 **HttpResponse**
-  **render()** 函數將 **request** 物件作為其第一個參數，將模板名稱作為其第二個參數，將 **context** 字典作為其可選的第三個參數。它返回使用上下文呈現模板的 **HttpResponse** 物件。

## 引發404錯誤
現在實作 **detail()** 視圖，經由URL的路由參數`question_id`從資料庫中的資料表中取得指定的**Question**物件：
```py
from django.shortcuts import render
from django.http import Http404
from .models import Question

#...

def detail(request, question_id):
  try:
    question = Question.objects.get(pk=question_id)
  except Question.DoesNotExist:
    raise Http404('沒有此問題!!')
  return render(request, 'detail.html', {'question': question})
```
- 如果不存在`question_id`的 **Question** 物件，則視圖會引發 **Http404** 異常。
- 在**polls/detail.html**模板中添加`{{ question }}`來快速檢視結果

### get_object_or_404()函數
如果物件不存在，使用 **get()** 並引發 **Http404** 是一種非常常見的習慣用法。Django提供了 **get_object_or_404()** 函數的捷徑。以下是重寫的完整 **detail()** 視圖：
```py
from django.shortcuts import render, get_object_or_404
from .models import Question

#...

def detail(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'detail.html', {'question': question})
```
- **get_object_or_404()** 函數將Django Model作為其第一個參數和任意數量的關鍵字參數，並將其傳遞給Model Manager的**get()**函數。如果物件不存在，它會引發**Http404**。

從 **detail()** 視圖傳遞上下文的變數`question`，在 **detail.html** 模板顯示 **Question** 物件的文本以及相關聯的 **Choice** 物件的文本：
```html
<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
{% endfor %}
</ul>
```

## 刪除模板中的硬編碼URL
在polls / index.html模板中編寫問題鏈接時，鏈接部分硬編碼如下：
```html
<li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
```

硬編碼的緊密耦合的問題在於，在具有大量模板的Project上更改URL變得具有挑戰性。

由於在 **polls.urls** 模塊的**path()**函數中定義了`name`參數，因此可以使用`{％url％}`模板標記來消除對特定URL路徑的依賴：
```html
<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
```

## 命名空間URL名稱
目前的學習Project只有一個投票應用程序。在真正的Django Project中，可能有五個，十個，二十個應用程序或更多。Django如何區分它們之間的URL名稱？

例如，投票應用程序具有 **detail()** 視圖，而同一Project中的Blog應用程序可能也有 **detail()** 視圖。如何讓Django知道在使用`{％url％}`模板標記時為網址創建哪個應用程序的視圖？

答案是為 **URLconf** 添加名稱空間。在 **polls/urls.py** 文件中，添加 **app_name** 變數以設置應用程序名稱空間：
```py
from django.urls import path
from . import views

app_name = 'polls' # application namespace
urlpatterns = [
  path('', views.index, name='index'), # route , veiw, kwargs, name
  path('<int:question_id>/', views.detail, name='detail'),
  path('<int:question_id>/results/', views.results, name='results'),
  path('<int:question_id>/vote/', views.vote, name='vote'),
]
```
現在更改投票應用程序**index.html**模板指向`polls`命名空間中的 **detail()** 視圖：
```html
<li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
```




