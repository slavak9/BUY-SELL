import json
from products.models import ProductName
from shopping_cart.models import ItemsToPurchase,UserCart
from shopping_cart.forms import AddItemsToPurchase
from user_personal_area.models import UserShippingAddress, UserCreditCart
from user_personal_area.forms import AddUserShippingAddress
from django.db.models import Q

# save and update purchase items

def get_purchased_item_object_(data):
    try:
        object_data = ItemsToPurchase.objects.get(user_id=data['user_id'])
        object_data.json_data = data['json_data']
        object_data.save()
    except Exception:
        return True

def save_purchase_items(request):
    data = {'user_id': request.user.user_id, 'json_data':  request.POST['data']}
    form = AddItemsToPurchase(data)
    if form.is_valid():
        form.save()
    else:
        if get_object(data):
            return True

def delete_item_from_user_cart(user_id,product_id):
    try:
        user_object = UserCart.objects.get(Q(user_id=user_id) & Q(product_id=product_id))
        user_object.delete()
    except Exception:
        return {'checkout_form_error': 'Delete item error!'}


# //////////////////////////////////////

# controls if purchase items are right

def get_control_object(data):
    data = json.loads(data)
    for item,quan in data.items():
        try:
            ProductName.objects.get(Q(product_id=item) & Q(quantity__gte=quan))
        except Exception:
            return {'checkout_form_error': f'''Product error:no such product ({item}) or quantity of ({quan}). 
                       Please control your items in the shopping cart!'''}


# controls data that arrives from user shopping cart page

def control_data(request):
    if request.POST['data']:
        data = json.loads(request.POST['data'])
        if 'checkout' in data:
            if data['checkout']:
                response = get_control_object(data['checkout'])
                if not response:
                    global user_checkout_cart
                    user_checkout_cart = {request.user.user_id: data['checkout']}
                    return 'is_checked'
                else:
                    return response
        elif 'delete' in data:
            if data['delete']:
                delete_item_from_user_cart(request.user.user_id, data['delete'])
            else:
                return {'checkout_form_error': 'Data error!'}
    else:
        return {'checkout_form_error':'Data error!'}

# /////////////////////////////////////////////////


def get_addresses_objects(user_id, object_id=None, is_chosen=None, to_choose=None, rel_filter=None):
    if user_id and not object_id and not is_chosen and not to_choose and not rel_filter:
        try:
            return UserShippingAddress.objects.filter(user_id=user_id)
        except Exception:
            return False
    elif user_id and object_id and not rel_filter:
        try:
            return UserShippingAddress.objects.get(Q(user_id=user_id) & Q(id=object_id))
        except Exception:
            return False
    elif user_id and is_chosen:
        try:
            return UserShippingAddress.objects.get(Q(user_id=user_id) & Q(is_chosen=is_chosen))
        except Exception:
            return False
    elif user_id and to_choose:
        try:
            return UserShippingAddress.objects.filter(user_id=user_id).first()
        except Exception:
            return False
    elif user_id and object_id and rel_filter:
        try:
            return UserShippingAddress.objects.filter(user_id=user_id, id=object_id)
        except Exception:
            return False

# get data user shipping and payment if exists end return in context

class GetOrderData:
    def get_user_context(self, **kwargs):
        address = self.get_user_shipping_address(kwargs['user_id'])
        context = kwargs
        context['title'] = 'Order Processing'
        if address:
            context['shipping_address'] = address
        return context

    def get_user_credit_cart(self):
        pass

    def get_user_shipping_address(self,user_id):
        return get_addresses_objects(user_id,is_chosen=True)


# /////////////////////////////////////////////////


# control section: controls field value of address form before saving in database
def control_phone_number(number):
    if not number:
        return 'This field is required.'
    if len(number) < 16 and (number[0] == '+' and number[1::].isnumeric()):
        return False
    else:
        return 'The number must be in format "+(country code) followed by numbers "'

def clear_white_space(value):
    return (' '.join([i for i in value.split(' ') if i]).capitalize())

def get_cleaned_items(object_form):
    for key, item in object_form.items():
        object_form[key] = clear_white_space(item)
    return object_form
# ///////////////////////////////////////////////////


def save_address_form(object_form, is_chosen=None):
    if is_chosen:
        object_form['is_chosen'] = 1
    address_form = AddUserShippingAddress(object_form)
    number = control_phone_number(object_form['phone_number'])
    if address_form.is_valid():
        if not number:
            address_form.save()
        else:
            address_form.add_error('phone_number', number)
            return address_form.errors
    else:
        return address_form.errors

def get_errors_messages(object_form):
    errors_dict = {'empty_field': 'This field is required.'}
    html_code = {}
    for key, item in object_form.items():
        if key == 'other_information':
            continue
        elif key == 'phone_number':
            number = control_phone_number(item)
            if number:
                html_code[key] = number
        elif not item:
            html_code[key] = errors_dict["empty_field"]
    if html_code:
        return html_code


def set_address_form(request):
    object_form = json.loads(request.POST['address_form'])
    object_form = get_cleaned_items(object_form)
    object_form['user_id'] = request.user.user_id
    object_quantity = get_addresses_objects(request.user.user_id)
    if not object_quantity:
        form = save_address_form(object_form,is_chosen=True)
        if form:
            return {'address_form_error': form}
    elif len(object_quantity) <= 3:
        form = save_address_form(object_form)
        if not form:
            return {'shipping_addresses': get_addresses_objects(request.user.user_id)}
        else:
            return {'address_form_error': form}
    else:
        return {'error_address_modification': 'You can have only 4 addresses!'}


def update_address_from(request):
    object_form = json.loads(request.POST['edit_form'])
    object_form = get_cleaned_items(object_form)
    errors_mess = get_errors_messages(object_form)
    if not errors_mess:
        model_form = get_addresses_objects(user_id=request.user.user_id, object_id=object_form['id'], rel_filter=True)
        object_form.pop('id')
        if model_form:
            model_form.update(**object_form)
            return {'shipping_addresses': get_addresses_objects(request.user.user_id)}
        else:
            return {'error_address_modification': 'Can not find the address!'}
    elif errors_mess:
        return {'address_form_error': errors_mess, 'shipping_addresses': get_addresses_objects(request.user.user_id)}

def control_get_request(request):
    context_response = {}
    if 'manage_addresses' in request.POST:
        if request.POST['manage_addresses']:
            addresses = get_addresses_objects(request.user.user_id)
            if addresses:
                return {'shipping_addresses':addresses}
    elif 'edit_form' in request.POST:
            return update_address_from(request)

    elif 'address_form' in request.POST:
            return set_address_form(request)

    elif 'save_addresses' in request.POST:
        objects_data = json.loads(request.POST['save_addresses'])
        error_mess = {'error_addresses_modification': 'Can not find address!'}
        trigger = False
        if objects_data['delete_address']:
            object_list_to_modify = get_addresses_objects(request.user.user_id)
            for item in objects_data['delete_address'].values():
                for item_object in object_list_to_modify:
                    if str(item_object.id) == item:
                        if item == objects_data['chosen_address']:
                            objects_data['chosen_address'] = ''
                        if item_object.is_chosen:
                            trigger = True
                        item_object.delete()
            if trigger and not objects_data['chosen_address']:
                object_list_to_modify = get_addresses_objects(request.user.user_id, to_choose=True)
                if object_list_to_modify:
                    object_list_to_modify.is_chosen = 1
                    object_list_to_modify.save()
                else:
                    return error_mess
        if objects_data['chosen_address']:
            if not trigger:
                object_list_to_modify = get_addresses_objects(request.user.user_id, is_chosen=True)
                if object_list_to_modify:
                    object_list_to_modify.is_chosen = 0
                    object_list_to_modify.save()
                else:
                    return error_mess
            object_list_to_modify = get_addresses_objects(request.user.user_id, object_id=objects_data['chosen_address'])
            if object_list_to_modify:
                object_list_to_modify.is_chosen = 1
                object_list_to_modify.save()
            else:
                return error_mess
    return context_response






    # 'edit_form_value' = as response if it is manage window

    #     try:
    #         user_item = UserCart.objects.get(user_id=data['user_id'], product_id=data['product_id'])
    #         user_item.quantity += int(data['quantity'])
    #         user_item.save()
    #         message['quantity'] = 'You already have this item in the cart. Quantity was added.'
    #     except Exception:
    #         form.save()
    #         message['saved'] = 'The item was added in the cart.'
    #     if data['trigger']:
    #         message['url'] = request.build_absolute_uri(reverse(url_to_redirect))
    #         return message
    #     else:
    #         return message
    # else:
    #     message['error'] = 'Invalid data. Please try again'
    #     return message

