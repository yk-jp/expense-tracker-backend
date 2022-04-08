from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_month_all, name="default"),
    path('register/', views.register,
         name='register')
]
