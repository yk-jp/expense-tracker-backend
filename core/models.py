from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Budget(models.Model):
    event = models.CharField(max_length=50)
    memo = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    # associations
    user = models.ForeignKey(User, verbose_name=("user"), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name=("category"), null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.id + ' ' + self.event + ' ' + self.date


