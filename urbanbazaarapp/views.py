from django.views import View
from django.shortcuts import render , redirect
from .forms import SignupForm , ProductForm
from .models import Profile , User , Cart , CartItem , Product , Order , OrderItem
from django.contrib.auth import authenticate , login as auth_login , logout
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404


class Userlogin(View):
    def get(self, request): 
        if request.user.is_authenticated:
            return redirect('redirect_view')
        return render(request, 'login.html')
        
    def post(self , request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
                try:
                    user = User.objects.get(email = email)
                except User.DoesNotExist:
                    return render(request, 'login.html', {'error': 'User with this email does not exist.'})

                user = authenticate(request, username = user.username, password = password)
                if user:
                    auth_login(request, user)
                    return redirect('redirect_view')
                else:
                    return render(request, 'login.html', {'error': 'Invalid email or password.'})
        return render(request, 'login.html', {'error': 'Please enter both email and password.'})


class LogoutView(View):
    def get(self , request):
        logout(request)
        return redirect('login')


class SignupUser(View):  
    def get(self, request): 
        if not request.user.is_authenticated:
            signup_form = SignupForm()
            return render(request, 'signup.html', {'form': signup_form})
        return redirect('login')
        
    def post(self, request):  
        if not request.user.is_authenticated:
            signup_form = SignupForm(data = request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                role = signup_form.cleaned_data['role']
                Profile.objects.create(user = user, role = role)
                user.save()
                return redirect('login')
            return render(request, 'signup.html', {'form': signup_form})
        return redirect('login')


class ProductAdd(View):  
    def get(self, request): 
        if request.user.is_authenticated and request.user.profile.role == 'Vendor':
            product_form = ProductForm()
            return render(request, 'product.html', {'form': product_form})
        return redirect('login')

    def post(self, request):  
        if request.user.is_authenticated and request.user.profile.role == 'Vendor':
            product_form = ProductForm(data = request.POST)
            if product_form.is_valid():
                user = product_form.save( commit = False)
                user.vendor = request.user
                user.save()
                return redirect('Vendor_dashboard')
            return render(request, 'product.html', {'form': product_form})
        return redirect('login')


class RedirectView(View):
    def get(self , request):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect('Admin_dashboard')
        elif request.user.is_authenticated and request.user.profile.role == 'Customer':
            return redirect('Customer_dashboard')
        elif request.user.is_authenticated and request.user.profile.role == 'Vendor':
            return redirect('Vendor_dashboard')
        else:
            return render(request , 'dashboard.html')


class Customer_dashboard(View):
    def get(self, request):
        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=request.user)
                if profile.role == 'Customer':
                    category = request.GET.get('category')

                    if category:
                        category = category.strip()
                        products = Product.objects.filter(category__icontains=category)
                    else:
                        products = Product.objects.all()

                    cart = Cart.objects.filter(user=request.user).first()
                    return render(request, 'Customer.html', {
                        'name': request.user.username,
                        'cart': cart,
                        'products': products
                    })
                else:
                    return redirect('login')

            except Profile.DoesNotExist:
                return redirect('login')

        return redirect('login')


class Vendor_dashboard(View):
    def get(self, request):
        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=request.user)
                if profile.role == 'Vendor':

                    products = Product.objects.filter(vendor = request.user)
                    return render(request, 'Vendor.html', {
                                    'name': request.user.username,
                                    'products': products
                                })
                else:
                    return redirect('login')
                
            except Profile.DoesNotExist:
                return redirect('login')
            
        return redirect('login')


class Admin_dashboard(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
                products = Product.objects.all()
                vendors = Profile.objects.filter(role = 'Vendor')
                customers = Profile.objects.filter(role = 'Customer')
                orders = Order.objects.all()
                order_items = OrderItem.objects.filter(order__in=orders)

                order_paginator = Paginator(orders, 7) 
                order_page_number = request.GET.get('order_page')
                orders_page = order_paginator.get_page(order_page_number)

                product_paginator = Paginator(products, 7) 
                product_page_number = request.GET.get('product_page')
                products_page = product_paginator.get_page(product_page_number)


                vendor_paginator = Paginator(vendors, 7)
                vendor_page_number = request.GET.get('vendor_page')
                vendors_page = vendor_paginator.get_page(vendor_page_number)

                customer_paginator = Paginator(customers, 7)
                customer_page_number = request.GET.get('customer_page')
                customers_page = customer_paginator.get_page(customer_page_number)

                context = {
                    'name': request.user.username,
                    'products': products_page,
                    'vendors': vendors_page,
                    'customers': customers_page,
                    'orders': orders_page,
                    'order_items': order_items,
                }

                return render(request, 'Admin.html', context)
        else:
            return redirect('login')


class Add_to_cart(View):
    def post(self , request , *args, **kwargs):
        if request.user.is_authenticated and request.user.profile.role == 'Customer':
            product_id = self.kwargs.get('id')
            product = Product.objects.get(id = product_id)
            cart , cart_created = Cart.objects.get_or_create(user = request.user)
            # cart = Cart.objects.get(user = request.user)
            cart_item , item_created = CartItem.objects.get_or_create(cart = cart , product = product , defaults={'quantity' : 1})

            if not item_created:
                        if cart_item.quantity < product.stock_quantity:
                            cart_item.quantity += 1
                            cart_item.total_price = cart_item.product.price * cart_item.quantity 
                            cart_item.save()
                        else:
                            if cart_item.quantity >= product.stock_quantity:
                                messages.error(request, f"Only {product.stock_quantity} units available in stock.")
                            else:
                                pass
                            
                        cart_item.save()

                        return redirect('Customer_dashboard')
            else:
                return redirect('login')
            
        return redirect('login')


class View_cart(View):
    def get(self , request):
        if request.user.is_authenticated and request.user.profile.role == 'Customer':

            cart = Cart.objects.filter(user = request.user).first()
            cart_items = CartItem.objects.filter(cart = cart)
            cart_items = [
                {
                    "id": item.id,
                    "product": item.product,
                    "quantity": item.quantity,
                    "price": item.product.price,
                    "total_price": item.quantity * item.product.price,
                }
                for item in cart_items
            ]

            return render (request , 'view_cart.html' , {'cart_items':cart_items , 'cart':cart})
        
        return redirect('login')


class Checkout(View):
    def get(self , request , *args, **kwargs):
        if request.user.is_authenticated and request.user.profile.role == 'Customer':
            cart = Cart.objects.filter(user=request.user).first()
            cart_items = CartItem.objects.filter(cart=cart)

            total_amount = sum(item.product.price * item.quantity for item in cart_items)

            for item in cart_items:
                item.total_price = item.product.price * item.quantity
            
            return render(request, 'checkout.html', {'cart_items': cart_items, 'total_amount': total_amount})
        else:
            return redirect('login')
        
    def post(self , request , *args , **kwargs):
        if request.user.is_authenticated and request.user.profile.role == 'Customer':
                cart = Cart.objects.filter(user=request.user).first()
                cart_items = CartItem.objects.filter(cart=cart)

                total_amount = sum(item.product.price * item.quantity for item in cart_items)

                for item in cart_items:
                    item.total_price = item.product.price * item.quantity

                for item in cart_items:
                    order = Order.objects.create(customer=request.user,order_date=datetime.now(),status="Pending",total_amount=item.total_price)
                
                    OrderItem.objects.create(order=order,product=item.product,quantity=item.quantity,price=item.product.price*item.quantity)
                    item.product.stock_quantity -= item.quantity
                    item.product.save()
                    cart_items.delete()
                    return redirect('Customer_dashboard')

                
                return render(request, 'checkout.html', {'cart_items': cart_items, 'total_amount': total_amount})
        else:
            return redirect('login')


class Update_Order_Status(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            order_id = self.kwargs.get('id')
            order = get_object_or_404(Order, id = order_id)
            return render(request, 'Update_Order_Status.html', {'order': order})
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            order_id = self.kwargs.get('id')
            order = get_object_or_404(Order, id = order_id)
            
            new_status = request.POST.get('status')
            order.status = new_status
            order.save()
            return redirect('Admin_dashboard')

        return render(request, 'Update_Order_Status.html', {'order': order})


class Cart_quantity_manage(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.profile.role == 'Customer':
            product_id = self.kwargs.get('id')
            del_cart = CartItem.objects.get(id = product_id)
            if del_cart.quantity >1:
                del_cart.quantity -= 1
                del_cart.total_price = del_cart.product.price * del_cart.quantity
                del_cart.save()
            else:
                del_cart.delete()
            return redirect('View_cart')
        
        return redirect('login')






