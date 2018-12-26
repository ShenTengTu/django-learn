from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'), # route , veiw, kwargs, name
]