import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, FormView, TemplateView, RedirectView
from django.contrib.auth.models import User, Group, Permission
from main_app.utils import DataMixing
from products.forms import AddProductInCart
from products.models import ProductName, ProductImgFileSD
from products.utils import get_cart_object


# Create your views here.

class Products(DataMixing,ListView):
    model = ProductName
    template_name = 'products/main_products.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        data_mixing = self.get_user_context(title=f"{self.kwargs['product_slug']}".replace('_', ' ').capitalize())
        context = dict(list(context.items()) + list(data_mixing.items()))
        if self.request.user.is_authenticated:
            data_mixing = self.get_user_context(items_in_the_cart=self.request.user.user_id)
            context = dict(list(context.items()) + list(data_mixing.items()))
        return context

    def get_queryset(self):
        data = ProductImgFileSD.objects.raw("""
        SELECT category_itemcategory.id, 
        products_productname.title,
        products_productname.slug, 
        products_productname.price, 
        products_productimgfilesd.img_file FROM category_itemcategory
        JOIN products_productname ON category_itemcategory.id = products_productname.products_item_id 
        JOIN products_productimgfilesd ON products_productimgfilesd.img_id_id = products_productname.id
        WHERE products_productimgfilesd.is_main = 1 AND products_productname.is_published = 1 AND category_itemcategory.slug = %s
        """, [self.kwargs['product_slug']])
        return data




class DetailProduct(DataMixing,DetailView):
    model = ProductName
    template_name = 'products/product_item.html'
    context_object_name = 'detail_product'
    slug_url_kwarg = 'single_product_slag'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        data_mixing = self.get_user_context(
            title=f"{kwargs['object']['title']}".capitalize(),
            product_img=self.kwargs['single_product_slag'], id=[kwargs['object']['id'],kwargs['object']['products_item_id']])
        context = dict(list(context.items()) + list(data_mixing.items()))
        if self.request.user.is_authenticated:
            data_mixing = self.get_user_context(items_in_the_cart=self.request.user.user_id)
            context = dict(list(context.items()) + list(data_mixing.items()))
        return context


    def get_queryset(self):
        return ProductName.objects.values('id', 'title', 'slug',
            'price', 'quantity', 'product_id', 'products_item_id').filter(is_published=True)


    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse(json.dumps(get_cart_object(request)))
        else:
            return HttpResponse(json.dumps({'error': 'You must log in for perches this item.'}))


class ShowImgGallery(DataMixing,DetailView):
    model = ProductName
    template_name = 'products/product_gallery_img_page.html'
    context_object_name = 'detail_product'
    slug_url_kwarg = 'gallery_img'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        data_mixing = self.get_user_context(
            title=f"Img Gallery {kwargs['object']['title']}".capitalize(),
            product_img_hd=self.kwargs['gallery_img'])
        context = dict(list(context.items()) + list(data_mixing.items()))
        if self.request.user.is_authenticated:
            data_mixing = self.get_user_context(items_in_the_cart=self.request.user.user_id)
            context = dict(list(context.items()) + list(data_mixing.items()))
        return context


    def get_queryset(self):
        return ProductName.objects.values('title','slug').filter(is_published=True)





# It is possible to combine DetailView and CreateView.
# You use a class for DetailView and another class for CreateView,
# then you create a new class that inherits from View.
# This new class has a get and post method.
# The get method calls the DetailView while the post method calls the CreateView.
# Take note to use reverse_lazy for the success_url in CreateView. So basically your code should look something like this:

# class PostView(DetailView):
    # your code
    # pass ;

# class CommentView(CreateView):
#     def get_success_url(self):
#         return reverse_lazy('post_detail', kwargs={'pk': self.get_object(Post.objects.all().pk})
#
# class PostCommentView(View):
#     def get(self, request, *args, **kwargs):
#          view = PostView.as_view()
#          return view(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs) :
#          view = CommentView.as_view()
#          return view(request, *args, **kwargs)
#