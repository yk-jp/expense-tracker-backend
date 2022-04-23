from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('transaction/', include('transaction.urls')),
    path('stats/', include('stats.urls')),
    path('auth/', include('authentication.urls'))
]

