# models/__init__.py
from .products import Products
from .category import Category
from .user import CustomUserManager, CustomUser, Role, UserRole  # Import the CustomUser model
from .orders import Order
