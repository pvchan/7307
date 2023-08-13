from django.shortcuts import render , redirect , HttpResponseRedirect
from store.models.products import Products
from store.models.category import Category
from django.views import View
from store.models.user import CustomUser, UserRole  
from django.utils.decorators import method_decorator
from django.middleware.csrf import rotate_token
from django.views.decorators.csrf import csrf_protect  


# Create your views here.
@method_decorator(csrf_protect, name='dispatch')
class Index(View):

    def post(self , request):
        rotate_token(request)
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        # redirect to the current page
        return redirect('homepage')



    def get(self , request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Products.get_all_products_by_categoryid(categoryID)
    else:
        products = Products.get_all_products()

    # Get user roles
    customer_id = request.session.get('customer')
    roles = []
    if customer_id:
        try:
            customer = CustomUser.objects.get(id=customer_id)
            roles = [user_role.role.name for user_role in UserRole.objects.filter(user=customer)]
        except CustomUser.DoesNotExist:
            pass

    data = {
        'products': products,
        'categories': categories,
        'roles': roles,  # Include roles in the context
    }

    print('you are : ', request.session.get('customer'))
    return render(request, 'index.html', data)



