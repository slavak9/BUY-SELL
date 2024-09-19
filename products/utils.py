from django.shortcuts import redirect
from django.urls import reverse
from products.forms import AddProductInCart
from products.models import ProductName
from shopping_cart.models import UserCart
import json

def quantity_in_stock(data):
    try:
        return ProductName.objects.get(product_id=data['product_id']).quantity
    except Exception:
        return False

def save_object(request,data):
    form = AddProductInCart(data)
    url_to_redirect = 'cart'
    message = {}
    if form.is_valid():
        try:
            user_item = UserCart.objects.get(user_id=data['user_id'], product_id=data['product_id'])
            user_item.quantity += int(data['quantity'])
            user_item.save()
            message['quantity'] = 'You already have this item in the cart. Quantity was added.'
        except Exception:
            form.save()
            message['saved'] = 'The item was added in the cart.'
        if data['trigger']:
            message['url'] = request.build_absolute_uri(reverse(url_to_redirect))
            return message
        else:
            return message
    else:
        message['error'] = 'Invalid data. Please try again'
        return message


def get_cart_object(request):
    data = json.loads(request.POST['data'])
    data['user_id'] = request.user.user_id
    message = {}
    user_quantity = data['quantity']
    quantity_in_store = quantity_in_stock(data)
    if not user_quantity or int(user_quantity) <= 0:
        message['error'] = 'Add quantity'
        return message
    elif int(user_quantity) > quantity_in_store:
        message['error'] = f'There is not enough quantity in the store!\nQuantity available {quantity_in_store}'
        return message
    else:
        return save_object(request, data)
