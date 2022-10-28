from django.contrib import admin
from django.urls import path, include
from . import views


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('cache/', views.cache_clear),
#     path('transaction/', include('transaction.urls')),
#     path('stats/', include('stats.urls')),
#     path('auth/', include('authentication.urls')),
#     path('category/', include('category.urls')),
# ]
urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/cache/', views.cache_clear),
    path('api/transaction/', include('transaction.urls')),
    path('api/stats/', include('stats.urls')),
    path('api/auth/', include('authentication.urls')),
    path('api/category/', include('category.urls')),
]
