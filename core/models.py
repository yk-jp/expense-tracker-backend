from django.db import models
from django.core.validators import MinValueValidator
from django.utils.timezone import now
import uuid


class User(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, unique=True) 
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

    id = models.AutoField(auto_created=True, primary_key=True, unique=True) 

    name = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        unique=True
    )

    def __str__(self):
        return self.name


class Transaction(models.Model):
    EVENT_CHOICES = (
        ('Income', 'Income'),
        ('Outcome', 'Outcome')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    event = models.CharField(
        max_length=50,
        choices=EVENT_CHOICES
    )

    amount = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default = 1,
        validators=[ 
            MinValueValidator(1) 
        ]
    )

    memo = models.TextField(
        null=True,
        blank=True
    )

    t_date = models.DateField()
     
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
        return str(self.amount)
