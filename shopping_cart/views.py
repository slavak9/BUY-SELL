from django.shortcuts import render, redirect
from django.http import Http404,HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView,TemplateView
from main_app.utils import DataMixing
from products.models import ProductName, ProductImgFileSD
from shopping_cart.utils import control_get_request, get_control_object, \
    GetOrderData, delete_item_from_user_cart
import json
user_checkout_cart = {}


# Create your views here.

def proses(request):
    return HttpResponse('<h1>proses</h1>')


class ShoppingCart(DataMixing, ListView):
    template_name = 'shopping_cart/user_cart.html'
    model = ProductName
    context_object_name = 'list_of_products'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        data_mixing = self.get_user_context(title=f'{self.request.user.username} Shopping cart')
        context = dict(list(context.items()) + list(data_mixing.items()))
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(f"{reverse('accounts')}?next={self.request.path}")

    def post(self, request, *args, **kwargs):
        print(request.POST)
        global user_checkout_cart
        self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)
        if 'delete' in request.POST:
            user_checkout_cart = {}
            if request.POST['delete']:
                response = delete_item_from_user_cart(request.user.user_id, request.POST['delete'])
                if response:
                    return HttpResponse(json.dumps(response))
        elif 'checkout' in request.POST:
            if request.POST['checkout']:
                response = get_control_object(request.POST['checkout'])
                if response:
                    context = dict(list((self.get_context_data(**kwargs)).items()) + list(response.items()))
                else:
                    user_checkout_cart ={request.user.user_id:request.POST['checkout']}
                    return redirect('order_info')
        user_checkout_cart = {}
        # beter way render_to_response(template.html,{'message':'value'})
        return self.render_to_response(context)

    def get_queryset(self):

        data = ProductImgFileSD.objects.raw("""
        SELECT products_productname.id,
        shopping_cart_usercart.user_id,
        products_productname.title,
        products_productname.slug,
        products_productname.product_id,
        products_productname.price,
        IIF(shopping_cart_usercart.quantity > products_productname.quantity
        ,products_productname.quantity,shopping_cart_usercart.quantity ) user_quantity,
        products_productname.quantity as 'available_quantity',
        ROUND((products_productname.price * (IIF(shopping_cart_usercart.quantity > products_productname.quantity
        ,products_productname.quantity,shopping_cart_usercart.quantity))),2) as 'total_price',
        products_productimgfilesd.img_file FROM products_productname
        JOIN shopping_cart_usercart on products_productname.product_id = shopping_cart_usercart.product_id
        JOIN products_productimgfilesd on products_productimgfilesd.img_id_id = products_productname.id
        WHERE products_productimgfilesd.is_main AND shopping_cart_usercart.user_id = %s
        """, [self.request.user.user_id])
        return data


class OrderInformation(GetOrderData,TemplateView):
    template_name = 'shopping_cart/order_information.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        data_mixing = self.get_user_context(user_id=self.request.user.user_id)
        context = dict(list(context.items()) + list(data_mixing.items()))
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and request.user.user_id in user_checkout_cart:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('home')


    def post(self, request, *args, **kwargs):
        response = control_get_request(request)
        context = dict(list((self.get_context_data(**kwargs)).items()) + list(response.items()))
        return self.render_to_response(context)



