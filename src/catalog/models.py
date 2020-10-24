from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=255)


class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='subs'
    )

    def __str__(self):
        return '%d: %s' % (self.id, self.name)


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE, related_name='products'
    )

    def __str__(self):
        return '%d: %s' % (self.id, self.name)


"""
    1 user --> has 1 cart
    So why I created cart with direct user link, 
    cause the task had no rules o realize customer and login/logout processes
"""
class Cart(models.Model):
    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='cart'
    )


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quant = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    @property
    def price(self):
        return self.product.price * self.quant
