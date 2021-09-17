from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('dataset/', views.dataset, name='dataset'),
    path('dataattr/', views.dataattr, name='dataattr'),
    path('models/', views.models, name='models'),
    path('mark/', views.mark, name='mark'),
    path('feedback/', views.feedback, name='feedback'),
    path('quit/', views.quit, name='quit'),
]
