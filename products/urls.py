from django.urls import path
from .views import Products, DetailProduct, ShowImgGallery

urlpatterns = [
    path('<slug:product_slug>/', Products.as_view(), name='category_item'),
    path('id_name/<slug:single_product_slag>/', DetailProduct.as_view(), name='product'),
    path('img_gallery/<slug:gallery_img>/', ShowImgGallery.as_view(), name='gallery'),
]