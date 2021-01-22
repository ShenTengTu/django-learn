# first Django app
參考官方文件教學：[Writing your first Django app (version 3.1)](https://docs.djangoproject.com/en/3.1/intro/tutorial01/)

<details>
  <summary>Change Log</summary>
  <dl>
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
> pip install --user pipenv # 安裝pipenv
> cd path/to/your/project # 切換到project目錄
> pipenv --three --site-packages # Python 3 虛擬環境 並啟用 site-packages
> pipenv install django # 安裝django 到虛擬環境
```

## 目錄
- [PART1](PART1.md)：瞭解Django專案及Django應用程式 (2021-01-21 Updated)
- [PART2](PART2.md)：瞭解Django對於資料庫的操作及Django模型類別
- [PART3](PART3.md)：瞭解Django路由設定、Django視圖及Django模板
- [PART4](PART4.md)：透過網頁表單瞭解Django伺服端如何處理客戶端要求
- [PART5]
- [PART6]
- [PART7]
