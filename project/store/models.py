from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    meant_for_choices = [('Men','Men'),('Women','Women'),('Boys','Boys'),('Girls','Girls')]
    meant_for = models.CharField(max_length=5,choices = meant_for_choices)
    name = models.CharField(max_length = 30)
    
    def __str__(self):
        return f'{self.name} for {self.meant_for}'

class Product(models.Model):
    name = models.CharField(max_length = 200)
    price = models.FloatField()
    category = models.ForeignKey(Category,on_delete = models.CASCADE)
    size_inventory = models.JSONField(default = dict)
    description = models.JSONField(default = dict)

    def __str__(self):
        return f'{self.id}: {self.name}'

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return f'Image: {self.id} for Product: {self.product}'
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - Ordered: {self.ordered}'

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    size = models.CharField(max_length = 4)
    quantity = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    ordered_price = models.IntegerField(default = 0)

class Addresses(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    street_building = models.CharField(max_length = 300)
    area = models.CharField(max_length = 40)
    city = models.CharField(max_length = 20)
    pin = models.IntegerField()
    phone = models.BigIntegerField()
    name = models.CharField(max_length = 30)

class Order(models.Model):
    status_list = [('cancelled','cancelled'), ('processing','processing'),('dispatched','dispatched'),('delivered','delivered')]
    cart = models.OneToOneField(Cart,on_delete = models.CASCADE)
    date = models.DateField(auto_now_add = True)
    status = models.CharField(choices = status_list,max_length = 20)
    address = models.ForeignKey(Addresses, on_delete = models.CASCADE)
    bill_amount = models.IntegerField(default = 0)
    delivery_date = models.DateField(auto_now = True)
