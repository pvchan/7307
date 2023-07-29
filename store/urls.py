from django.contrib import admin
from django.urls import path
from .views.home import Index , store
from .views.signup import Signup
from .views.login import Login , logout
from .views.cart import Cart
from .views.checkout import CheckOut
from .views.orders import OrderView
from .middlewares.auth import  auth_middleware
from .views.products import ProductView
from .views.admin_dashboard import AdminView
from .views.staff_dashboard import StaffView
from .views.createuser import CreateUser
from .views.viewproducts import ViewProducts, EditProduct, NewProduct
from .views.viewcategories import ViewCategories, EditCategory, NewCategory
from .views.viewusers import ViewUsers, EditUser

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store', store , name='store'),

    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout , name='logout'),
    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('product/<int:product_id>', ProductView.as_view(), name='product'),
    path('admin_dashboard', AdminView.as_view(), name='admin_dashboard'),
    path('staff_dashboard', StaffView.as_view(), name='staff_dashboard'),
    path('create_user', CreateUser.as_view(), name='create_user'),
    path('viewproducts', ViewProducts.as_view(), name='viewproducts'),
    path('editproduct/<int:product_id>', EditProduct.as_view(), name='editproduct'),
    path('viewcategories', ViewCategories.as_view(), name='viewcategories'),
    path('editcategory/<int:category_id>', EditCategory.as_view(), name='editcategory'),
    path('new_category', NewCategory.as_view(), name='new_category'),
    path('new_product', NewProduct.as_view(), name='new_product'),
    path('viewusers', ViewUsers.as_view(), name='viewusers'),
    path('viewusers/edit/<int:user_id>/', EditUser.as_view(), name='edituser'),
]
