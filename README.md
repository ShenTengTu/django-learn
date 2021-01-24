# first Django app
參考官方文件教學：https://docs.djangoproject.com/en/3.1/

<details>
  <summary>Change Log</summary>
  <dl>
    <dt>2021-01-24</dt>
    <dd>新增『佈署檢查清單』。 使用dotenv來進行配置。</dd>
    <dt>2021-01-21</dt>
    <dd>更新至Django 3.1.x，以3.1版官方文件為參考。更新PART1.md，範例代碼改回PART1進度。 </dd>
  </dl>
</details>
<br>

操作環境：
- ~~Windows 7~~, Ubuntu 18.04
- Python 3.7.x
- Django ~~2.1.7~~ 3.1.x

[DEMO連結](http://shentengtu.pythonanywhere.com/polls/)

## Python虛擬環境
本學習項目使用 Pipenv 套件管理工具來創建虛擬環境。 ([Pipenv 套件管理工具 官網](https://pipenv.readthedocs.io/en/latest/))
```shell
$ pip install --user pipenv # 安裝pipenv
$ cd path/to/your/project # 切換到project目錄
$ pipenv --three --site-packages # Python 3 虛擬環境 並啟用 site-packages
$ pipenv install django # 安裝django 到虛擬環境
$ pipenv install python-dotenv # 安裝dotenv加載模組 到虛擬環境
```

## 目錄
- [Writing your first Django app (version 3.1)](https://docs.djangoproject.com/en/3.1/intro/tutorial01/)
  - [PART1](PART1.md)：瞭解Django專案及Django應用程式 (2021-01-21 Updated)
  - [PART2](PART2.md)：瞭解Django對於資料庫的操作及Django模型類別
  - [PART3](PART3.md)：瞭解Django路由設定、Django視圖及Django模板
  - [PART4](PART4.md)：透過網頁表單瞭解Django伺服端如何處理客戶端要求
  - [PART5]
  - [PART6]
  - [PART7]
- [佈署檢查清單](others/deployment/deployment_checklist.md)

## 佈署
根據[佈署檢查清單](others/deployment/deployment_checklist.md)，**settings.py**的
- `SECRET_KEY`必須保密
- 設置`DEBUG = False`
- 設置`ALLOWED_HOSTS`

DJango專案創建時會自動生成一組密鑰，要重新生成可以執行以下命令將新的密鑰輸出到名為SECRET_KEY的文字檔：
```shell
$ python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())' > SECRET_KEY
```

專案遵循[12要素原則](https://12factor.net/)，採用`.env`檔案進行配置並使用`python-dotenv`模組來添加到環境變量中。

實際佈署的`.env`檔案不要提交到公開的代碼管理服務，請參考Django專案目錄內的`example.env`範例檔案。

在`manage.py`中下方加入以下代碼：
```python
# ...

from pathlib import Path
from dotenv import load_dotenv

def main():
    """Run administrative tasks."""
    # path of Django project directory
    BASE_DIR = Path(__file__).resolve().parent
    # Reads the key-value pair from .env file and adds them to environment variable. 
    load_dotenv(dotenv_path=BASE_DIR / '.env', override=True)

    # ...
```

在`wsgi.py`與`asgi.py`中導入`get_wsgi_application`或`get_wsgi_application`之前加入以下代碼：
```python
from pathlib import Path
from dotenv import load_dotenv

# path of Django project directory
BASE_DIR = Path(__file__).resolve().parent.parent
# Reads the key-value pair from .env file and adds them to environment variable. 
load_dotenv(dotenv_path=BASE_DIR / '.env', override=True)
```

在`setting.py`中修改：
```python
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (os.environ['DEBUG'] == "True")

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    os.environ['ALLOWED_HOST']
    ]
```



