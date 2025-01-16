from django.contrib import admin
from .models import Profile , Product
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user' , 'role']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['vendor' , 'name' , 'description' , 'price' , 'stock_quantity' , 'category' , 'image']


