from django.http import HttpResponse
from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_func),
    path('all_users/', views.show_all_users)
]
