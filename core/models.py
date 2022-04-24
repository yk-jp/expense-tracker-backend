from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
from django.core.validators import MinValueValidator, validate_email
from django.core.exceptions import ValidationError
from django.utils.timezone import now
import uuid

class CustomUserManager(BaseUserManager):
    VALIDATE_FIELDS = { 
        "email":"email",
        "password":"password"
    }
    
    def update_user(self, user, **fields):
        User.objects.update_validation(user, **fields)
        
        if self.VALIDATE_FIELDS["password"] in fields:
            user.set_password(fields["password"])
            user.save()
        else: User.objects.filter(pk=user.id).update(**fields)
        
    
    def update_validation(self,user, **fields):
        if len(fields) <= 0:
            raise ValueError("There's nothing to be updated.")
        
        if self.VALIDATE_FIELDS["email"] in fields:
            email = fields["email"] 
            
            if validate_email(fields["email"]):
                raise ValidationError("Enter a valid email address")
            
            if User.objects.filter(email=fields["email"]).exclude(pk=user.id).exists(): 
                raise ValidationError(f'This email, \'{email}\' is already registered. Choose another email.')
        
        if self.VALIDATE_FIELDS["password"] in fields:
            if len(fields["password"]) < 8:
                raise ValueError("Password is too short. enter at least 8 characters")
    
    def create_validation(self, email, name, password, **extra_fields):
        if not email:
            raise ValueError("Email is not provided")
        
        if not password:
            raise ValueError("Password is not provided")
        
        if validate_email(email):
            raise ValidationError("Enter a valid email address")
        
        if User.objects.filter(email=email).exists(): 
            raise ValidationError(f'This email, \'{email}\' is already registered. Choose another email.')
        
        if len(password) < 8:
            raise ValueError("Password is too short. enter at least 8 characters")
    
    def create_user(self, email, name, password, **extra_fields):
       
        self.create_validation(email, name, password, **extra_fields)
        
        user = self.model(
            name = name,
            email = self.normalize_email(email),
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(auto_created=True, primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(
        db_index=True,
        max_length=254,
        unique=True
    )
    
    password = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','password']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Category(models.Model):
    CATEGORY_CHOICES_DEFAULT = (
        ('Random', 'Random'),
        ('Food', 'Food'),
        ('Rent', 'Rent'),
        ('Phone', 'Phone'),
        ('Transportation', 'Transportation'),
        ('Education', 'Education'),
        ('Insurance', 'Insurance'),
        ('Add', 'Add')
    )    
    
    CATEGORY_TYPE = (
        ('Expense', 'Expense'),
        ('Income', 'Income')
    )    

    id = models.AutoField(auto_created=True, primary_key=True, unique=True)
    
    user = models.ForeignKey(
        User,
        verbose_name=("user"),
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=50,
        default="Random"
    )
    
    category_type = models.CharField(
       max_length = 50,
       choices= CATEGORY_TYPE
    )

    def __str__(self):
        return f'{self.user} , {self.category_type}, {self.name}'


class Transaction(models.Model):
    EVENT_CHOICES = (
        ('Income', 'Income'),
        ('Expense', 'Expense')
    )

    id = models.AutoField(auto_created=True, primary_key=True, unique=True)

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

    date = models.DateField()
     
    # associations
    user = models.ForeignKey(
        User,
        verbose_name=("user"),
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        verbose_name=("category"),
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f'{self.id} {self.user} {self.event} {self.category} {self.amount}'
