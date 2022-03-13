from django.db import models
from django.core.validators import MinValueValidator 

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(
        max_length=50,
        unique=True
    )
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.email


class Category(models.Model):
    CATEGORY_CHOICES = (
        ('Food', 'Food'),
        ('Rent', 'Rent'),
        ('Phone', 'Phone'),
        ('Transportation', 'Transportation'),
        ('Education', 'Education'),
        ('Insurance', 'Insurance'),
        ('Random', 'Random'),
        ('Edit', 'Edit'),
    )

    name = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    def __str__(self):
        return self.name


class Budget(models.Model):
    EVENT_CHOICES = (
        ('Income', 'Income'),
        ('Outcome', 'Outcome')
    )

    event = models.CharField(
        max_length=50,
        choices=EVENT_CHOICES
    )
    amount = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(1)
        ]
    )
    memo = models.TextField(
        null=True,
        blank=True
    )
    date = models.DateField(auto_now_add=True)
    # associations
    user = models.ForeignKey(
        User,
        verbose_name=("user"),
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        verbose_name=("category"),
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return str(self.user) + ' ' + str(self.event) + ' ' + str(self.category)
