from django.contrib import admin
from .models import Profile , Product , Cart , CartItem , Order , OrderItem , UserOTP
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id' , 'user' , 'role']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['vendor' , 'name' , 'description' , 'price' , 'stock_quantity' , 'category' , 'image']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart' , 'product' , 'quantity']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order' , 'product' , 'quantity' , 'price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer' , 'order_date' , 'status' , 'total_amount']

@admin.register(UserOTP)
class OtpAdmin(admin.ModelAdmin):
    list_display = ['user' , 'otp' , 'otp_created_at']

