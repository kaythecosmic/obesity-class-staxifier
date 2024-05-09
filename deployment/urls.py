from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('input', views.input, name = 'input'),
    path('predict', views.predict, name = 'predict'),
]