from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData, name="default"),
    path('transaction-register/', views.transaction_register,
         name='transaction_register')
]
