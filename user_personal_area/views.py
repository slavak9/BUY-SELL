from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView,DetailView,TemplateView
from main_app.utils import DataMixing
from category.forms import CategoriesForm, ItemCategoryForm
from products.forms import ProductNameForm
from products.models import ProductName, ProductImgFileSD
from category.models import Categories, ItemCategory
from user_personal_area.utils import ItemDataMixing, set_new_product, set_edit_product,delete_and_view
# Create your views here.
import json
# class UserSellsArea(DataMixing, ListView):
#     template_name = 'user_personal_area/user_area.html'
#     model = ProductName
#     context_object_name = 'products'
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         data_mixing = self.get_user_context(title=f'{self.request.user.username} Area')
#         context = dict(list(context.items()) + list(data_mixing.items()))
#         return context
#
#     def dispatch(self, request, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             return super().dispatch(request, *args, **kwargs)
#         else:
#             return redirect(f"{reverse('accounts')}?next={self.request.path}")
#
#     def get_queryset(self):
#         data = ProductImgFile.objects.raw("""
#         SELECT category_itemcategory.id,
#         products_productname.title,
#         products_productname.slug,
#         products_productname.price,
#         products_productimgfile.img_file FROM category_itemcategory
#         JOIN products_productname ON category_itemcategory.id = products_productname.products_item_id
#         JOIN products_productimgfile ON products_productimgfile.img_id_id = products_productname.id
#         WHERE products_productimgfile.is_main = 1 AND category_itemcategory.slug = %s
#         """, [self.kwargs['product_slug']])
#         return data



def user_area(request):
    category = CategoriesForm
    item_category = ItemCategoryForm
    if request.method == 'POST':
        print(request.POST)
    return render(request,'user_personal_area/user_area_1.html',{'category':category,'item_category':item_category})

def user_orders(request):
    return HttpResponse('this is user orders')
def user_mesagges(request):
    return HttpResponse('this is user orders')
def user_payments(request):
    return HttpResponse('this is user payment')
def user_sell(request):
    return HttpResponse('this is user payment')

class UserSalesArea(DataMixing, ListView):
    template_name = 'user_personal_area/user_sales_area.html'
    model = ProductName
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        data_mixing = self.get_user_context(title=f"{self.request.user.username.capitalize()}'s Area")
        context = dict(list(context.items()) + list(data_mixing.items()))
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(f"{reverse('accounts')}?next={self.request.path}")

    def get_queryset(self):
        data = ProductImgFileSD.objects.raw("""
        SELECT products_productname.id,
        products_productname.title,
        products_productname.slug,
        products_productname.is_published,
        products_productimgfilesd.img_file FROM category_itemcategory
        JOIN products_productname ON category_itemcategory.id = products_productname.products_item_id 
        JOIN products_productimgfilesd ON products_productimgfilesd.img_id_id = products_productname.id
        WHERE products_productimgfilesd.is_main = 1  AND products_productname.user_id = %s
        ORDER BY products_productname.time_create DESC
            """,[self.request.user.user_id])
        return data

    def post(self, request, *args, **kwargs):
        response = delete_and_view(request)
        return HttpResponse(json.dumps(response))




class UserProductEdit(ItemDataMixing,DetailView):
    template_name = 'user_personal_area/user_edit_product.html'
    context_object_name = 'detail_product'
    slug_url_kwarg = 'edit_product_slag'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        data_mixing = self.get_user_context(id=kwargs['object'].id,title='Product Modification',
                                            category=kwargs['object'].products_item)
        context = dict(list(context.items()) + list(data_mixing.items()))
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(f"{reverse('accounts')}?next={self.request.path}")

    def get_queryset(self):
        queryset = ProductName.objects.filter(slug=self.kwargs[self.slug_url_kwarg])
        return queryset

    def post(self, request, *args, **kwargs):
        response = set_edit_product(request)
        #response = {'error':'error'}
        if not response:
            url = request.build_absolute_uri(reverse('user_sales_area'))
            return HttpResponse(json.dumps({'url': url}))
        elif 'fields' in response:
            return HttpResponse(json.dumps({'fields': response['fields']}))
        else:
            return HttpResponse(json.dumps({'error': response['error']}))


class UserProductAdd(ItemDataMixing,TemplateView):
    template_name = 'user_personal_area/user_new_product.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        data_mixing = self.get_user_context(title='Add Item')
        context = dict(list(context.items()) + list(data_mixing.items()))
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(f"{reverse('accounts')}?next={self.request.path}")

    def post(self, request, *args, **kwargs):
        response = set_new_product(request)
        if not response:
            url = request.build_absolute_uri(reverse('user_sales_area'))
            return HttpResponse(json.dumps({'url': url}))
        elif 'fields' in response:
            return HttpResponse(json.dumps({'fields': response['fields']}))
        else:
            return HttpResponse(json.dumps({'error': response['error']}))

