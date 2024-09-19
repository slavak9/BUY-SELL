from django.db import models
from django.urls import reverse


# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=50,unique=True,db_index=True,verbose_name='Name of Category')
    slug = models.SlugField(max_length=50,unique=True,db_index=True,verbose_name='Slug')
    img_categories = models.ImageField(blank=True,verbose_name='Category Image')
    is_published = models.BooleanField(default=False,verbose_name='Is Published')
    time_create = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('chosen_category',kwargs={'category_slug':self.slug})



class ItemCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name='Title')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Slug of Sub Category')
    img_item_category = models.ImageField(blank=True, verbose_name='Sub Category Image')
    time_create = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False, verbose_name='Is Published')
    category_id = models.ForeignKey(Categories, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_item',kwargs={'product_slug':self.slug})
