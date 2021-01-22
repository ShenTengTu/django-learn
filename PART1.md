PART1
=====

本教學將引導您創建基本的民意調查應用程式。

它由兩部分組成：
- 一個允許人們觀看民意調查並對其進行投票的公共網站。
- 一個允許您添加，更改和刪除民意調查的管理網站。

在終端機內執行以下命令來告訴獲得Django及安裝了哪個版本：
```
$ python -m django --version
```

## 創建 Project
第一次使用Django，則必須進行一些初始設置。您將需要自動生成一些代碼來建立Django專案—對Django實例的一組設置，包括資料庫配置，特定於Django的選項和特定於應用程式的設置。

在終端機內，使用`cd`進入要存儲代碼的目錄，然後執行下列命令：
```
$ django-admin startproject study_project
```

 [django-admin]是Django用於管理任務的命令行實用程序。

<dl>
  <dt><a href="https://docs.djangoproject.com/en/3.1/ref/django-admin/#startproject">startproject</a></dt>
  <dd>在當前目錄或給定目的地中為給定專案名稱創建Django專案目錄結構。
  </dd>
</dl>

Django Project 目錄結構如下：
```
study_project/
    manage.py
    study_project/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```

- 外部**study_project/**根目錄只是Django專案的容器。
- **manage.py**：一個命令行實用程序，可讓您通過各種方式與此Django專案進行交互。 (官方說明：[django-admin and manage.py])
- 內部的**study_project/**目錄代表專案實際的Python套件。
  - **__init__.py**：將目錄定義為Python套件的必要檔案。(官方說明：[6.4. Packages])
  -  **settings.py**：Django專案的配置檔。(官方說明：[Django settings])
  -  **urls.py**：Django專案的URL宣告(路由配置)。(官方說明：[URL dispatcher])
  -  **asgi.py**：[ASGI]兼容的Web伺服器為您的專案提供服務的入口點。(官方說明：[How to deploy with ASGI])
  -  **wsgi.py**：[WSGI]兼容[的Web伺服器為您的專案提供服務的入口點。(官方說明：[How to deploy with WSGI])
  
## 開發用伺服器
驗證Django專案的是否有效。進入外部**study_project**目錄，請運行以下命令：
```
$ python manage.py runserver
```

您會在終端機上看到以下輸出：
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
January 22, 2021 - 08:56:59
Django version 3.1.5, using settings 'study_project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

您已經啟動了Django開發用伺服器，這是一種僅用Python編寫的輕型Web伺服器。 我它包含在Django中，因此可以快速進行開發，而無需準備配置生產用服務器（例如Apache）。不要在類似於生產環境的任何環境中使用該伺服器。 

現伺服器已運行，請使用Web瀏覽器訪問`http://127.0.0.1:8000/`，您將會看到『The install worked successfully! Congratulations!』的訊息頁面。

預設情況下，[runserver]命令在內部IP的通訊埠8000上啟動開發用伺服器。 如果要更改伺服器的通訊埠，請將其作為命令行參數傳遞。例如，下方命令在通訊埠8080上啟動伺服器：
```
$ python manage.py runserver 8080
```

如果要更改伺服器的IP，請將其與通訊埠一起傳遞。例如，要偵聽所有可用的公共IP（，請使用：
```
$ python manage.py runserver 0:8000
```

開發用伺服器會根據需要自動為每個請求重新加載Python代碼。 您無需重新啟動伺服器即可使代碼更改生效。 但是，某些操作（例如添加文件）不會觸發重新啟動，因此在這種情況下，您必須重新啟動伺服器。

## 創建民意調查應用程式
本教學將在與manage.py文件相同的目錄中創建民意調查應用程式，以便可以將其導入為自己的頂層模組，而不是study_project的子模組。 要創建您的應用，請確保您與manage.py位於同一目錄中。

在外部**study_project**目錄建立應用程式**polls**，輸入此命令：
```
$ python manage.py startapp polls
```

<dl>
  <dt><a href="https://docs.djangoproject.com/en/3.1/ref/django-admin/#startapp">startapp</a></dt>
  <dd>在當前目錄或給定目的地中為給定應用程式名稱創建Django應用程式名目錄結構。
  </dd>
</dl>

Django應用程式目錄結構如下：
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
from django.http import HttpResponse


def index(request):
    return HttpResponse("民意調查首頁")
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

函數[`path()`]有四個參數，兩個必需：`route`和`view`，以及兩個可選：`kwargs`和`name`。
- **route**： 是一個包含URL模式的字符串。處理請求時，Django從`urlpatterns`中的第一項URL模式開始，沿著列表向下移動，將請求的URL與每個模式進行比較，直到找到匹配的模式。
- **view**： 當Django找到匹配的模式時，它調用指定的View函數，其中`HttpRequest`物件作為View函數的第一個參數，來自路由的任何捕獲到的值作為關鍵字參數。
- **kwargs**： 任意關鍵字參數可以傳遞一個`dict`物件到目標View。
- **name**： 命名您的URL可讓您從Django的其他地方明確地引用它，尤其是在模板(Template)中。

下一步是將根URLconf指向**polls.urls** 模組。在**study_project/urls.py**中，導入`django.urls.include`，並在`urlpatterns`列表中插入函數[`include()`]，如以下程式碼：
```py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```

函數[`include()`]能引用其他URLconf。每當Django遇到[`include()`]時，它都會砍掉已匹配到該點的URL的任何部分，並將剩餘的字符串發送到被引用的URLconf中以進行進一步處理。

[`include()`]背後的想法是使URL即插即用變得容易。由於民意調查應用程式在他們自己的URLconf(**polls/urls.py**)中，因此可以將它們放在URL路徑"/polls/”下，或“/fun_polls/”下，或“/content/polls/”下，或任何其他URL根路徑下，該應用程式仍然可以正常工作。

引用其他URL模式時，應始終使用[`include()`]。

您現在已將**index** View牽線到URLconf。讓我們驗證它是否正常工作，運行以下命令：
```
$ python manage.py runserver
```
在瀏覽器中轉到`http://127.0.0.1:8000/polls/`，可以應該看到『民意調查首頁』的文字。
> 到目前為止，訪問`http://127.0.0.1:8000/`會得到Page not found (404)錯誤頁面。

---

前往 [Part 2](PART2.md)

[django-admin]: https://docs.djangoproject.com/en/3.1/ref/django-admin/
[django-admin and manage.py]: https://docs.djangoproject.com/en/3.1/ref/django-admin/
[6.4. Packages]: https://docs.python.org/3/tutorial/modules.html#tut-packages
[Django settings]: https://docs.djangoproject.com/en/3.1/topics/settings/
[URL dispatcher]: https://docs.djangoproject.com/en/3.1/topics/http/urls/
[ASGI]: https://asgi.readthedocs.io/en/latest/
[How to deploy with ASGI]: https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
[WSGI]: https://wsgi.readthedocs.io/en/latest/what.html
[How to deploy with WSGI]: https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
[`path()`]: https://docs.djangoproject.com/en/3.1/ref/urls/#django.urls.path
[`include()`]: https://docs.djangoproject.com/en/3.1/ref/urls/#django.urls.include