from products.models import ProductImgFileSD, ProductImgFileHD, ProductVideoFile, ProductDescription,\
            DescriptionText,DescriptionImgFile,DescriptionTable, SearchInfo
from category.models import ItemCategory
from django.db.models import Q
from shopping_cart.models import UserCart

menu_bar = [
    {'title': 'Category', 'url_name': 'category'},
    {'title': 'Support', 'url_name': 'support'},
    {'title': 'News', 'url_name': 'news'},
    {'title': 'About', 'url_name': 'about'},
]
login_link = {'title': 'Login', 'url_name': 'accounts'}
logout_link = {'title': 'Logout', 'url_name': 'logout', 'url_personal_area': 'user_personal_area'}
icon_link = {'home': 'home', 'shopping_cart': 'cart'}
registration = {'title': 'Register', 'url_name': 'register'}
forgot_password = {'title': 'Forgot Password', 'url_name': 'forgot_password'}

user_area_bar = [
    {'title': 'My orders', 'url_name': 'orders'},
    {'title': 'Messages', 'url_name': 'messages'},
    {'title': 'Payments', 'url_name': 'payments'},
    {'title': 'Sales area', 'url_name': 'user_sales_area'},
]
user_area_bar.append(logout_link)

def get_tag_url(x):
    domain = ['http://', 'https://', 'www.']
    x = x.split(' ')
    for i in range(len(x)):
        for k in domain:
            if k in x[i]:
                x[i] = f'{x[i][0:x[i].find(k)]}<a href="{x[i][x[i].find(k):]}">{x[i][x[i].find(k):]}</a>'
                break
    return ' '.join(x)

def get_description_images(id):
    try:
        return DescriptionImgFile.objects.filter(img_id=id)
    except Exception:
        pass


def get_model_fields(data):
    model = ItemCategory.objects.raw(f'''SELECT * FROM products_{data[1]} 
    WHERE products_{data[1]}.product_id_id = {data[0]}''')
    new_model =[]
    model = [i.__dict__ for i in model][0]
    for key in model:
        if key == '_state' or key == 'id' or key == 'product_id_id':
            continue
        else:
            if type(model[key]) == bool and (model[key]):
                new_model.append({'name': str(key).capitalize(), 'value': 'Yes'})
            elif type(model[key]) == bool and not (model[key]):
                new_model.append({'name': str(key).capitalize(), 'value': 'No'})
            else:
                new_model.append({'name': str(key).capitalize(), 'value': str(model[key]).capitalize()})
    return new_model
class DataMixing:

    def get_user_context(self,**kwargs):
        context = kwargs
        if 'product_img' in context:
            try:
                video = ProductVideoFile.objects.filter(video_id__slug=context['product_img'])
                context['product_video'] = video
            except Exception:
                pass

            try:
                description = ProductDescription.objects.get(description_id__slug=context['product_img'])
                context['product_description'] = description

                try:
                    tabel = DescriptionTable.objects.get(table_id=description.id)
                    context['table_description'] = tabel
                except Exception:
                    pass

                try:
                    description = DescriptionText.objects.filter(text_id=description.id)
                    for i in description:
                        i.text_description = get_tag_url(i.text_description)
                        i.images = get_description_images(i.id)
                    context['text_description'] = description
                except Exception:
                    pass
            except Exception:
                pass

            try:
                context['id'][1] = (ItemCategory.objects.values('slug').get(id=context['id'][1]))['slug'].replace('_','').replace(' ','')
                fields = get_model_fields(context['id'])
                context['main_info'] = fields
            except Exception:
                pass

            try:
                img = ProductImgFileSD.objects.filter(img_id__slug=context['product_img']).order_by('-is_main')
                context['product_img'] = img
            except Exception:
                context.pop('product_img')
        if 'product_img_hd' in context:
            try:
                img = ProductImgFileHD.objects.filter(img_id__slug=context['product_img_hd'])
                context['product_img_hd'] = img
            except Exception:
                context.pop('product_img_hd')

        if 'items_in_the_cart' in context:
            try:
                items_in_the_cart = UserCart.objects.values('user_id').filter(user_id=context['items_in_the_cart']).count()
                if items_in_the_cart:
                    context['items_in_the_cart'] = items_in_the_cart
                else:
                    context.pop('items_in_the_cart')
            except Exception:
                context.pop('items_in_the_cart')


        context['menu_bar'] = menu_bar
        context['user_area_bar'] = user_area_bar
        context['login_link'] = login_link
        context['logout_link'] = logout_link
        context['icon_link'] = icon_link
        context['registration'] = registration
        context['forgot_password'] = forgot_password

        return context