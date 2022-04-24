from django.urls import path
from . import views

urlpatterns = [
    path('save',views.add_category, name='add_category'),
    path('update/<int:id>/',views.update_category, name='update_category'),
    path('delete/<int:id>/',views.delete_category, name='delete_category'),
    path('<str:type>', views.get_category_all, name='category'),
]

