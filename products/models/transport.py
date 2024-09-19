from django.db import models
from products.models import ProductName


class Cars(models.Model):
    brand = models.CharField(max_length=30, default=None, null=True, blank=True, verbose_name='Brand')
    year = models.IntegerField(blank=True,default=None, null=True, verbose_name='Year')
    price = models.DecimalField(max_digits=10, default=None, null=True, decimal_places=2, blank=True, verbose_name='Price')
    brand_choices_to_select = models.CharField(max_length=30, default=None, null=True, blank=True, verbose_name='Brand_choices_to_select')
    product_id = models.ForeignKey('ProductName', on_delete=models.CASCADE)


