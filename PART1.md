PART1
=====

## 創建 Project
在目錄中執行下列命令：
```
django-admin startproject study_project
```
- **django-admin**是Django用於管理任務的命令行實用程序。
- `startproject`命令將為當前目錄創建Django Project目錄結構。

Django Project 目錄結構如下：
```
study_project/
    manage.py
    study_project/
        __init__.py
        settings.py
        urls.py
        wsgi.py
```

- **study_project/**根目錄只是Project的容器。
- **manage.py**：等同於django-admin。 (官方說明：[django-admin and manage.py](https://docs.djangoproject.com/en/2.1/ref/django-admin/))
- 內部的**study_project/**目錄代表project的Python程式包。
  - **__init__.py**：將目錄定義為Python程式包的必要檔案。(官方說明：[6.4. Packages](https://docs.python.org/3/tutorial/modules.html#tut-packages))
  -  **settings.py**：Django project的配置檔。
  -  **urls.py**：Django project的URL宣告(路由配置)。
  -  **wsgi.py**：兼容WSGI的Web服務器的入口點，為project提供伺服。

## 啟動開發伺服器
將目錄轉至**study_project/**並執行：
```
python manage.py runserver
```
將會在http://127.0.0.1:8000/啟動開發服務器。

## 創建 App (投票應用程序)
Project和App之間有什麼區別？
- App是執行某些操作的Web應用程序
  - 例如Weblog系統，或簡單的投票應用程序。
- Project是特定網站的配置和應用程序的集合。

在**study_project/**根目錄(**manage.py**旁邊)建立應用程序**polls**，輸入此命令：
```
python manage.py startapp polls
```
- `startapp`命令將為當前目錄創建Django應用程序目錄結構。

Django應用程序目錄結構如下：
```
polls/
    migrations/
        __init__.py
    __init__.py
    admin.py
    apps.py
    models.py
    tests.py
    views.py
```

## 創建 View
建立一個簡單的**index** View，在**polls / views.py**將以下Python程式碼放入其中：
```py
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
  return HttpResponse('投票首頁')
```

要調用View，必須將其映射到URL，為此需要一個URL配置(URLconf)。

在polls目錄中創建**urls.py**的文件，並讓其包含以下程式碼：
```py
from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'), # route , veiw, kwargs, name
]
```

函數`path()`有四個參數，兩個必需：route和view，以及兩個可選：kwargs和name。
- **route**： 是一個包含URL pattern的字符串。處理請求時，Django從`urlpatterns`中的第一項URL pattern開始，沿著列表向下移動，將請求的URL與每個模式進行比較，直到找到匹配的pattern。
- **view**： 當Django找到匹配的pattern時，它調用指定的View函數，其中`HttpRequest`物件作為View函數的第一個參數，並且路由中的任何captured values作為關鍵字參數。
- **kwargs**： 任意關鍵字參數可以在目錄中傳遞到目標View。
- **name**： 命名您的URL可讓您從Django的其他地方明確地引用它，尤其是在模板(Template)中。

下一步是將根目錄URLconf指向**polls.urls** module。

在**study_project/urls.py**中，導入`django.urls.include`，並在`urlpatterns`列表中插入函數`include()`，如以下程式碼：
```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
]
```

函數`include()`讓根目錄URLconf能引用其他URLconf。`include()`背後的想法是使URL即插即用變得容易。

由於投票應用程序在他們自己的URLconf(**polls/urls.py**)中，因此可以將它們放在URL路徑"/polls/”下，或“/fun_polls/”下，或“/content/polls/”下，或任何其他URL根路徑下，該應用程序仍然可以正常工作。

您現在已將**index** View 連接到URLconf。讓我們驗證它是否正常工作，運行以下命令：
```
python manage.py runserver
```
- 在瀏覽器中轉到http://127.0.0.1:8000/polls/，可以應該看到“投票首頁“的文字。