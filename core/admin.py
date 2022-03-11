from django.contrib import admin


from .models import User, Budget, Category

admin.site.register(
    [
        User,
        Budget,
        Category
    ]
)
