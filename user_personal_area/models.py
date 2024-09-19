from django.db import models

# Create your models here.

class UserShippingAddress(models.Model):
    user_id = models.CharField(max_length=50,verbose_name='User ID')
    country = models.CharField(max_length=40, verbose_name='Country')
    region = models.CharField(max_length=40, verbose_name='Region')
    locality_or_city = models.CharField(max_length=40, verbose_name='Locality or City')
    street = models.CharField(max_length=40, verbose_name='Street')
    home_apartment = models.CharField(max_length=20, verbose_name='Home/Apartment Number')
    postal_zip_code = models.CharField(max_length=50, verbose_name='Postal Zip Code')
    other_information = models.TextField(blank=True, verbose_name='Other Information')
    phone_number = models.CharField(max_length=20, verbose_name='Phone Number')
    is_chosen = models.BooleanField(default=0, verbose_name='Selected')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Update Time')

class UserCreditCart(models.Model):
    pass

class UserOrders(models.Model):
    order_id = models.CharField(max_length=50, verbose_name='Order ID')
    user_id = models.CharField(max_length=50, verbose_name='User ID')
    products = models.TextField(verbose_name='Product List')
    order_time = models.DateTimeField(auto_now_add=True, verbose_name='Order Time')








