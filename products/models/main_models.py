from django.db import models
from django.urls import reverse
from category.models import ItemCategory
# Create your models here.

class ProductName(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Slug of Product')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name='Is Published')
    product_id = models.CharField(max_length=50, unique=True, verbose_name='Product ID')
    price = models.DecimalField(verbose_name='Product price', max_digits=10, decimal_places=2)
    quantity = models.IntegerField(blank=True, verbose_name='Product Quantity')
    user_id = models.CharField(max_length=50, verbose_name='UserID')
    products_item = models.ForeignKey(ItemCategory, on_delete=models.PROTECT)


    #def __str__(self):
    #    return self.title

    def get_absolute_url(self):
        return reverse('product',kwargs={'single_product_slag':self.slug})



class ProductVideoFile(models.Model):
    video_file = models.FileField(upload_to='product_video/%Y/%m/%d',verbose_name='Product video file',blank=True)
    video_id = models.ForeignKey('ProductName', on_delete=models.CASCADE)


class ProductImgFileSD(models.Model):
    is_main = models.BooleanField(verbose_name='Main picture',db_index=True, default=False)
    img_file = models.ImageField(upload_to='product_img/%Y/%m/%d',blank=True,verbose_name='Product img file')
    img_id = models.ForeignKey('ProductName', on_delete=models.CASCADE)

class ProductImgFileHD(models.Model):
    img_file = models.ImageField(blank=True, verbose_name='Product img file')
    img_id = models.ForeignKey('ProductName', on_delete=models.CASCADE)

class SearchInfo(models.Model):
    model = models.CharField(max_length=60, blank=True, verbose_name='Model')
    brand = models.CharField(max_length=60, blank=True, verbose_name='Brand')
    year = models.IntegerField(blank=True, verbose_name='Year')
    size = models.CharField(max_length=20, blank=True, verbose_name='Size')
    place = models.CharField(max_length=100, blank=True, verbose_name='Place')
    search_id = models.ForeignKey('ProductName', on_delete=models.CASCADE)


class ProductDescription(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name='Description title')
    description_id = models.ForeignKey('ProductName', on_delete=models.CASCADE)


class DescriptionText(models.Model):
    text_description = models.TextField(blank=True, verbose_name='Product description')
    text_id = models.ForeignKey('ProductDescription', on_delete=models.CASCADE)

class DescriptionImgFile(models.Model):
    img_file = models.ImageField(blank=True, verbose_name='Description Img file')
    img_id = models.ForeignKey('DescriptionText', on_delete=models.CASCADE)

class DescriptionTable(models.Model):
    table = models.TextField(blank=True, verbose_name='HTML Table')
    table_id = models.ForeignKey('ProductDescription', on_delete=models.CASCADE)


class DescriptionFile(models.Model):
    file = models.FileField(blank=True, upload_to='descriptio_media/file/%Y/%m/%d', verbose_name='Descriptio file')
    file_id = models.ForeignKey('ProductDescription', on_delete=models.CASCADE)