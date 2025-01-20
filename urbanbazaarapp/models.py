from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Profile(models.Model):
    ROLE_CHOICE = (('Vendor' , 'Vendor') , ('Customer' , 'Customer'))

    user = models.OneToOneField(User , on_delete = models.CASCADE)
    role = models.CharField(max_length = 20 , choices = ROLE_CHOICE)
    # is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class UserOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name= "otp_info",blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    def is_otp_valid(self):
        if self.otp_created_at:
            return (now() - self.otp_created_at).total_seconds() <= 600  
        return False

class Product(models.Model):

    CATEGORY_CHOICES = [
        ('ELECTRONICS', 'Electronics'),
        ('CLOTHING', 'Clothing'),
        ('FURNITURE', 'Furniture'),
        ('ACCESSORIES', 'Accessories'),
        ('MOBILE', 'Mobile'),
        ('LAPTOP', 'Laptop'),
    ]
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default= 'ELECTRONICS')
    image = models.ImageField(default='dd.png')

    def __str__(self):
        return f"{self.name} by {self.vendor.username} ({self.category})"


class Cart(models.Model):
    user = models.OneToOneField(User , on_delete = models.CASCADE)
    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart , on_delete = models.CASCADE)
    product = models.ForeignKey(Product , on_delete = models.CASCADE)
    quantity = models.PositiveBigIntegerField(default = 1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"


class Order(models.Model):
    ORDER_STATUS = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=ORDER_STATUS, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order by {self.customer.username} on {self.order_date.strftime('%Y-%m-%d')}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in order {self.order.id}"




