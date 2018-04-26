from django.urls import path, re_path

from . import views

urlpatterns = [
    path('<int:category_id>/', views.detail, name='detail'),
    path('', views.index),
]