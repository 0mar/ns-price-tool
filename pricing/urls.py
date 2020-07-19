from django.urls import path
from pricing import views

urlpatterns = [
    path('', views.index, name='index')
]