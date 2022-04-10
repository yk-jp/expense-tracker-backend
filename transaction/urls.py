from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_month_all, name='default'),
    path('save', views.add_new_event,
         name='add_new_event'),
]
