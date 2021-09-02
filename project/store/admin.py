from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Product)
admin.site.register(models.Category)
admin.site.register(models.Cart)
admin.site.register(models.Addresses)
admin.site.register(models.CartItem)
admin.site.register(models.Order)
admin.site.register(models.ProductImages)