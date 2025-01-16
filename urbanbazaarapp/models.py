from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICE = (('Vendor' , 'Vendor') , ('Customer' , 'Customer'))

    user = models.OneToOneField(User , on_delete = models.CASCADE)
    role = models.CharField(max_length = 20 , choices = ROLE_CHOICE)

    def __str__(self):
        return f"{self.user.username} {self.role}"


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

    def _str_(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)



