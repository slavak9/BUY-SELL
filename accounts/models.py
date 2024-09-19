from django.db import models
from django.contrib.auth.models import AbstractUser



class UsersAccounts(AbstractUser):
    email = models.EmailField(max_length=100, verbose_name='email address', unique=True)
    user_id = models.CharField(max_length=50, verbose_name='UserID', blank=True, unique=True)
    date_of_birth = models.CharField(max_length=20, verbose_name='Date of Birth', blank=True)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []



# class CustomUser(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     user_id = models.CharField(max_length=255)









