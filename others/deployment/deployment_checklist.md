# 佈署檢查清單
在部署Django專案之前，應該花一些時間在考慮安全性，性能和操作的情況下檢查設置。

Django包含許多[安全功能]。 有些是內置的，並且始終啟用。 其他選項是可選的，因為它們並不總是合適的，或者因為它們不方便開發。 例如，強制HTTPS可能不適用於所有網站，並且對於本地開發來說是不切實際的。

性能最佳化是另一種權衡取捨的方法。 例如，快取在生產中很有用，而對於本地開發則不那麼有用。 錯誤報告的需求也大不相同。

以下清單包括以下設置：
- 必須正確設置Django以提供預期的安全級別；
- 預計在每種環境下都會有所不同；
- 啟用可選的安全功能；
- 實現性能最佳化；
- 提供錯誤報告。

其中許多設置都是敏感的，應視為機密。如果要發布項目的源代碼，通常的做法是發布適當的設置進行開發，並使用私有設置模組進行生產。

## 運行 `manage.py check --deploy`
可以使用[`check --deploy`]選項自動執行以下所述的某些檢查。請確保按照選項文檔中的說明針對您的生產設置文件運行該文件。

## 關鍵設置

### `SECRET_KEY`
**密鑰必須是較大的隨機值，並且必須保密。**

**確保生產中使用的密鑰沒有在其他任何地方使用，並避免將其提交給源代碼管理**。這減少了攻擊者可以從中獲取密鑰向量的數量。

可以考慮從環境變量中加載密鑰，而不是在設置模組中對密鑰進行硬編碼：
```python
import os
SECRET_KEY = os.environ['SECRET_KEY']
```

或來自文件：
```python
with open('/etc/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()
```

### `DEBUG`
**您絕不能在生產中啟用調試。**

您肯定是在使用`DEBUG = True`來開發項專案，因為這樣可以在瀏覽器中啟用方便的功能，例如完整的追溯。

但是，對於生產環境而言，這是一個非常糟糕的主意，因為它會洩露有關專案的大量訊息：源代碼的摘錄，區域變數，設置，使用的程式庫等。

## 特定於環境的設置

### `ALLOWED_HOSTS`
當`DEBUG = False`時，如果沒有適當的`ALLOWED_HOSTS`值，Django將無法工作。

需要使用此設置來保護您的站點免受某些[CSRF]攻擊。如果使用通配符(`*`)，則必須對`Host` HTTP標頭執行自己的驗證，否則，請確保您不容​​易受到此類攻擊。

您還應該配置位於Django前面的Web伺服器以驗證主機。 它應該以靜態錯誤頁面響應或忽略對不正確主機的請求，而不是將請求轉發給Django。 這樣，您就可以避免Django日誌（如果配置了錯誤報告，則避免發送電子郵件）中的虛假錯誤。 例如，在nginx上，您可以設置默認伺服器以在無法識別的主機上返回“ 444 No Response”：
```nginx
server {
    listen 80 default_server;
    return 444;
}
```

### `CACHES`
如果您使用快取，則連結參數在開發和生產中可能會有所不同。 Django默認對每個進程進行可能不是理想的[本地記憶體快取]。

快取伺服器通常具有弱認證。確保它們僅接受來自您的應用程式伺服器的連結。

### DATABASES`
資料庫連結參數在開發和生產中可能有所不同。

**資料庫密碼非常敏感。您應該像`SECRET_KEY`一樣保護它們。**

為了獲得最大的安全性，請確保資料庫伺服器僅接受來自應用程式伺服器的連結。

如果您尚未為資料庫設置備份，請立即執行！

### `EMAIL_BACKEND` 與相關設置
如果您的站點發送電子郵件，則需要正確設置這些值。

默認情況下，Django從`webmaster @ localhost`和`root @ localhost`發送電子郵件。但是，某些郵件提供商拒絕來自這些地址的電子郵件。要使用其他發件人地址，請修改`DEFAULT_FROM_EMAIL`和`SERVER_EMAIL`設置。

### `STATIC_ROOT` 與 `STATIC_URL`
靜態文件由開發伺服器自動提供。在生產中，必須定義`STATIC_ROOT`目錄，[collectstatic]將在其中複製它們。

有關更多訊息，請參見[管理靜態文件]（例如圖片，JavaScript，CSS）。

### `MEDIA_ROOT`與 `MEDIA_URL`
媒體文件由您的用戶上傳。他們不被信任！確保您的Web伺服器從不嘗試直釋它們。例如，如果用戶上傳.php文件，則Web伺服器不應執行該文件。

現在是檢查這些文件的備份策略的好時機。

## HTTPS
任何允許用戶登錄的網站都應實施站點範圍的HTTPS，以避免明文傳輸存取令牌。在Django中，存取令牌包括登錄名稱/密碼，會話cookie和密碼重置令牌。 （如果您通過電子郵件發送密碼重置令牌，則無法做很多事情來保護它們。）

保護敏感區域（例如用戶帳戶或管理員）是不夠的，因為HTTP和HTTPS使用相同的會話Cookie。您的Web伺服器必須將所有HTTP通信重定向到HTTPS，並且只能將HTTPS請求傳輸到Django。

設置HTTPS後，請啟用以下設置。

### `CSRF_COOKIE_SECURE`
將此設置為`True`可以避免通過HTTP意外傳輸CSRF cookie。

### `SESSION_COOKIE_SECURE`
將此設置為`True`可以避免通過HTTP意外傳輸會話cookie。

## 性能最佳化
設置`DEBUG = False`將禁用僅在開發中有用的一些功能。另外，您可以調整以下設置。

### Sessions
考慮使用[已快取的會話]來提高性能。 

如果使用資料庫支持的會話，請定期[清除舊會話]，以避免存儲不必要的數據。

### `CONN_MAX_AGE`
當連接到資料庫帳戶佔請求處理時間的很大一部分時，啟用[持久性資料庫連結]可以大大提高速度。

這對於網絡性能有限的虛擬主機有很大幫助。

### `TEMPLATES`
啟用已快取的模板加載器通常會大大提高性能，因為它避免了每次需要渲染每個模板時都對它們進行編譯。有關更多信息，請參見[模板加載器文檔]。

## 錯誤報告
當您將代碼推向生產環境時，它有望變得健壯，但不能排除意外錯誤。值得慶幸的是，Django可以捕獲錯誤並相應地通知您。

### `LOGGING`
在將網站投入生產之前，請檢查日誌記錄配置，並在收到一些流量後立即檢查它是否按預期工作。

有關詳細信息，請參見[日誌記錄]。

### `ADMINS`  與 `MANAGERS`
`ADMINS`將通過電子郵件收到`500`錯誤的通知。

將向`MANAGERS`通知`404`錯誤。` IGNORABLE_404_URLS`可以幫助過濾掉虛假報告。

有關通過電子郵件報告錯誤的詳細信息，請參見[錯誤報告]。

> **通過電子郵件報告的錯誤無法很好地擴展**
> 在收件箱被報告淹沒之前，請考慮使用諸如[Sentry]之類的錯誤監視系統。Sentry也可以匯總日誌。

### 自定義默認錯誤View
Django包含一些HTTP錯誤代碼的默認View和模板。 您可能需要通過在根模板目錄中創建以下模板來覆蓋默認模板：**404.html**，**500.html**，**403.html**和**400.html**。 使用這些模板的[默認錯誤View]足以滿足99％的Web應用程式的要求，但是您也可以對其[進行自定義]。

[安全功能]: https://docs.djangoproject.com/en/3.1/topics/security/
[`check --deploy`]: https://docs.djangoproject.com/en/3.1/ref/django-admin/#cmdoption-check-deploy
[CSRF]: https://en.wikipedia.org/wiki/Cross-site_request_forgery
[本地記憶體快取]: https://docs.djangoproject.com/en/3.1/topics/cache/#local-memory-caching
[collectstatic]: https://docs.djangoproject.com/en/3.1/ref/contrib/staticfiles/#django-admin-collectstatic
[管理靜態文件]: https://docs.djangoproject.com/en/3.1/howto/static-files/
[已快取的會話]: https://docs.djangoproject.com/en/3.1/topics/http/sessions/#cached-sessions-backend
[清除舊會話]: https://docs.djangoproject.com/en/3.1/topics/http/sessions/#clearing-the-session-store
[持久性資料庫連結]: https://docs.djangoproject.com/en/3.1/ref/databases/#persistent-database-connections
[模板加載器文檔]: https://docs.djangoproject.com/en/3.1/ref/templates/api/#template-loaders
[日誌記錄]: https://docs.djangoproject.com/en/3.1/topics/logging/
[錯誤報告]: https://docs.djangoproject.com/en/3.1/howto/error-reporting/
[Sentry]: https://docs.sentry.io/
[默認錯誤View]: https://docs.djangoproject.com/en/3.1/ref/views/#error-views
[進行自定義]: https://docs.djangoproject.com/en/3.1/topics/http/views/#customizing-error-views