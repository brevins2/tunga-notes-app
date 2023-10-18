from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAllUsers),
    path('<int:pk>/', views.login),
    path('create/', views.register),
    path('delete/<int:user_id>/', views.deleteSingleUser, name='delete-user'),
    path('update/<int:user_id>/', views.updateSingleUser, name='update-single-user')
]
