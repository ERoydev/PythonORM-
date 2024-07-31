from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_fruit/', views.CreateFruitView.as_view(), name='create_fruit'),
    path('<int:pk>/', include([
        path('details_fruit/', views.details_fruit, name='details_fruit'),
        path('edit_fruit/', views.edit_fruit, name='edit_fruit'),
        path('delete_fruit/', views.DeleteFruitView.as_view(), name='delete_fruit')
    ])),
    path('create_category/', views.create_category, name='create_category')
]
