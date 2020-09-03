from django.urls import path
from . import views

app_name = 'scrapy'

urlpatterns = [
    path('', views.show_results, name="results"),
]
