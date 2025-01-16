from django.views import View
from django.shortcuts import render , redirect
from .forms import SignupForm , ProductForm
from .models import Profile , User , Cart , CartItem , Product
from django.contrib.auth import authenticate , login as auth_login , logout


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
                    return redirect('product')
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
                return redirect('redirect_view')
            return render(request, 'product.html', {'form': product_form})
        return redirect('login')


class RedirectView(View):
    def get(self , request):
        if request.user.is_authenticated and request.user.is_superuser:
            return render(request , 'Admin.html')
        elif request.user.is_authenticated and request.user.profile.role == 'Customer':
            return redirect('Customer_dashboard')
        elif request.user.is_authenticated and request.user.profile.role == 'Vendor':
            return render(request , 'Vendor.html')
        else:
            return render(request , 'dashboard.html')


# class Customer_dashboard(View):
#     def get(self , request):
#         if request.user.is_authenticated and request.user.profile.role == 'Customer' :
#             category = request.GET.get('category')

#             if category:
#                 category = category.strip()

#             if category:
#                 products = Product.objects.filter(category__icontains=category)
#             else:
#                 products = Product.objects.all()

#             cart = Cart.objects.filter(user=request.user).first()
#             return render(request, 'Customer.html', {'name': request.user.username , 'cart': cart , 'products': products})
    
#         return redirect('redirect_view')


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





