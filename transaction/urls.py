from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_month_all, name='transaction'),
    path('save', views.add_new_event,
         name='add_new_event'),
    path('delete_event/<int:id>', views.delete_event, name='delete_event'),
    path('update_event/<int:id>', views.update_event, name='update_event'),
    path('day', views.get_day_event, name='get_day_event')
]
