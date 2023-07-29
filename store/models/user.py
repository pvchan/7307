from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .orders import Order


# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, first_name, last_name, email, phone_number, password, **extra_fields)


# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "email", "phone_number"]

    def __str__(self):
        return self.username

    @staticmethod
    def get_user_roles(user_id):
        from .orders import UserRole
        return UserRole.objects.filter(user_id=user_id)
    
    @staticmethod
    def get_user_orders(user_id):
        from .orders import Order
        return Order.objects.filter(user_id=user_id)
    
    orders = models.ManyToManyField('store.Order', through='store.UserRole', related_name='users_as_customer')
    user = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='users_as_staff')

    groups = None  # Disable built-in groups field for the CustomUser model
    user_permissions = None

# Role Model
class Role(models.Model):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    )

    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name  


# User-Role Mapping Model
class UserRole(models.Model):
    user = models.ForeignKey('store.CustomUser', on_delete=models.CASCADE)
    role = models.ForeignKey('store.Role', on_delete=models.CASCADE)
    order = models.ForeignKey('store.Order', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

