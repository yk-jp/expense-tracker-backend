from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_stats_month, name='stats'),
    path('year/',views.get_stats_recent_one_year, name='stats_year'),
    path('category/<str:name>/',views.get_category_stats, name='category')
]
