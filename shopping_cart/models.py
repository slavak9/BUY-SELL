from django.db import models

class UserCart(models.Model):
    user_id = models.CharField(max_length=50, verbose_name='User ID')
    product_id = models.CharField(max_length=125, verbose_name='Product ID')
    quantity = models.IntegerField(verbose_name='Quantity')


    def __str__(self):
        return self.product_id

class ItemsToPurchase(models.Model):
    user_id = models.CharField(max_length=50, verbose_name='User Id', unique=True)
    json_data = models.TextField(verbose_name='Json Data')

    def __str__(self):
        return self.user_id