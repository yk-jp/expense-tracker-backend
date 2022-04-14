from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_stats,name='stats'),
    path('category/<str:name>/',views.get_category_stats, name='category')
]
