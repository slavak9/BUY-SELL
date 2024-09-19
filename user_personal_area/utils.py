from products.models import ProductName, ProductImgFileSD, ProductImgFileHD, ProductVideoFile, ProductDescription, \
    DescriptionText, DescriptionImgFile, DescriptionTable, DescriptionFile
from category.models import Categories, ItemCategory
from django.http import FileResponse
from django.http import HttpResponse
from user_personal_area.manage_data import set_img_initial, set_des_img, video_load_initial
import json
import string
import random
import os
from django.conf import settings


try:
    from products.models import get_model
    from products.form_files import get_form
except ImportError:
    print('error: at user_personal_area/utils, get_form is not exists yet')

main_img_limit = 8  # set quantity of uploading main images
description_img_limit = 8  # set quantity of uploading description images
video_limit = 1  # set quantity of uploading video


def get_category_queryset():
    try:
        queryset_objects = Categories.objects.values('id', 'name', 'slug')
        for object in queryset_objects:
            object['items'] = get_itemcategory_queryset(object['id'])
        return queryset_objects
    except Exception:
        return False


def get_itemcategory_queryset(id):
    try:
        return ItemCategory.objects.filter(category_id=id).values('id', 'name', 'slug', 'category_id')
    except Exception:
        return False


def get_product_imgfile_queryset(id):
    try:
        return ProductImgFileSD.objects.filter(img_id_id=id)
    except Exception:
        return False


def get_product_videofile_queryset(id):
    try:
        return ProductVideoFile.objects.filter(video_id_id=id)
    except Exception:
        return False


def get_product_table_queryset(id):
    try:
        return DescriptionTable.objects.get(table_id=id)
    except Exception:
        return False


def get_product_file_queryset(id):
    try:
        return DescriptionFile.objects.get(file_id=id)
    except Exception:
        return False


def get_product_img_queryset(id):
    try:
        return DescriptionImgFile.objects.filter(img_id_id=id)
    except Exception:
        return False


def get_product_text_queryset(id):
    try:
        text_object = DescriptionText.objects.values('id', 'text_description').filter(text_id=id)
        count = 0
        for text in text_object:
            objects = get_product_img_queryset(text['id'])
            text['image'] = objects
            text['quantity'] = count
            count += len(objects)
        return (text_object, count)
    except Exception:
        return False


def get_product_description_queryset(id):
    try:
        description_object = ProductDescription.objects.values('id', 'title').get(description_id=id)
        objects = get_product_text_queryset(description_object['id'])
        description_object['des_text'] = objects[0]
        description_object['img_count'] = objects[1]
        return description_object
    except Exception:
        return False


# return form fields or names for each sub category on request
def get_fields_category(name, bool=None):
    form = get_form(name['category'], name['slug'])
    if bool and form:
        return form
    elif form:
        form = form().as_ul()
        form = '\n'.join([i.replace(i[0:i.rfind(':<')][i[0:i.rfind(':<')].find('>') + 1:],
                                    i[0:i.rfind(':<')][i[0:i.rfind(':<')].find('>') + 1:].replace('_', ' '))
                          if '</label>' in i else i for i in form.split('\n')])
        return {'fields': form}
    else:
        return {'fields': 'None'}


def get_model_values(name):
    model = get_model(name['category'], name['slug'])
    if model:
        try:
            model = model.objects.get(product_id_id=name['id'])
            model = model.__dict__
            model.pop('_state')
            model.pop('id')
            model.pop('product_id_id')
            return model
        except Exception:
            return


def get_new_model_fields(fields, models):
    new_fields = ''
    for field in fields():
        field = str(field)
        for key, value in models.items():
            if f'name="{key}"' in field and '<select' in field:
                field = field.split('\n')
                for ind in range(len(field)):
                    if f'value="{value}"' in field[ind]:
                        field[ind] = field[ind].replace(f'value="{value}"', f'value="{value}" selected')
                    elif 'selected' in field[ind]:
                        field[ind] = field[ind].replace('selected', '')
                field = f'<label for="id_{key}">{key.replace("_", " ").capitalize()}:</label>' + ''.join(field)
            elif 'type="checkbox"' in field and f'name="{key}"' in field:
                field = f'<label for="id_{key}">{key.replace("_", " ").capitalize()}:</label>' + \
                        field.replace(f'name="{key}"', f'name="{key}" checked')
            elif f'name="{key}"' in field:
                field = f'<label for="id_{key}">{key.replace("_", " ").capitalize()}:</label>' + \
                        field.replace(f'name="{key}"', f'name="{key}" value="{value}"')
        new_fields += f'<li>{field}</li>\n'
    return new_fields


def get_product_cat_fields(data):
    model = get_model_values(data)
    if not model:
        return get_fields_category(data)
    else:
        fields = get_new_model_fields(get_fields_category(data, True), model)
        return {'fields': fields}


def get_slug_category(category, id):
    for cat in category:
        for item in cat['items']:
            if item['id'] == id:
                return cat['slug']


class ItemDataMixing:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['category_objects'] = get_category_queryset()
        if 'id' in context:
            context['img_object'] = get_product_imgfile_queryset(context['id'])
            context['video_object'] = get_product_videofile_queryset(context['id'])
            context['description_object'] = get_product_description_queryset(context['id'])
            context['file'] = get_product_file_queryset(context['description_object']['id'])
            context['table'] = get_product_table_queryset(context['description_object']['id'])
            context['data_fields'] = get_product_cat_fields({'slug': context['category'].slug,
                                                             'id': context['id'],
                                                             'category': get_slug_category(context['category_objects'],
                                                                                           context['category'].id)})
        context['main_img_quan'] = main_img_limit
        context['des_img_quan'] = description_img_limit
        return context


def check_slag(st):
    try:
        ProductName.objects.get(slug=st)
        return check_slag(st + random_user_id('AD-SL'))
    except Exception:
        return st


def get_slag(n: str):
    list_char = string.punctuation.replace('-', '').replace('_', '')
    slug = ''
    n = n.replace(' ', '_')
    for i in n:
        if i in list_char:
            if slug[-1] != '-':
                slug += '-'
        else:
            slug += i
    return check_slag(slug.lower().strip('-'))


def random_user_id(s):
    number_id = random.choices(range(0, 10), k=9)
    return s + str(number_id).strip('[]').replace(', ', '')


def get_product_id(d):
    product_id = random_user_id('PI_') + d
    try:
        ProductName.objects.get(product_id=product_id)
        return get_product_id(d)
    except Exception:
        return product_id


# ---------------------------------------------------------------------------------------

def SetMainImg(s, f, i):  # return HD and SD path otherwise return error
    all_path = set_img_initial(f, hd_size=1920, sd_size=960)
    if type(all_path) == bool:
        return {'error': 'Make sure that all images are right format. Please try again!'}
    elif all_path['HD'] and all_path['SD']:
        all_path['HD'] = os.path.join(all_path['HD']['path'], all_path['HD']['file_name'])
        all_path['SD'] = os.path.join(all_path['SD']['path'], all_path['SD']['file_name'])
        try:
            ProductImgFileSD.objects.create(is_main=s, img_file=all_path['SD'], img_id_id=i)
        except Exception:
            print('error', 'user_personal_area', 'can not create imgSD object')
            path = os.path.join(settings.MEDIA_ROOT, all_path['SD'])
            try:
                os.remove(path)
            except FileNotFoundError:
                print(f'FileNotFoundError: {path}')
            path = os.path.join(settings.MEDIA_ROOT, all_path['HD'])
            try:
                os.remove(path)
            except FileNotFoundError:
                print(f'FileNotFoundError: {path}')
            return {'error': 'Can not create image object'}

        try:
            ProductImgFileHD.objects.create(img_file=all_path['HD'], img_id_id=i)
        except Exception:
            print('error', 'user_personal_area', 'can not create imgSD object')
            path = os.path.join(settings.MEDIA_ROOT, all_path['SD'])
            try:
                os.remove(path)
            except FileNotFoundError:
                print(f'FileNotFoundError: {path}')
            path = os.path.join(settings.MEDIA_ROOT, all_path['HD'])
            try:
                os.remove(path)
            except FileNotFoundError:
                print(f'FileNotFoundError: {path}')
            return {'error': 'Can not create image object'}
    else:
        return {'error': 'Make sure that all images are right format. Please try again!'}
    return {
        'path': [os.path.join(settings.MEDIA_ROOT, all_path['SD']), os.path.join(settings.MEDIA_ROOT, all_path['HD'])]}


def set_new_product(request):
    if 'get_category_fields' in request.POST:
        if request.POST['get_category_fields']:
            data = json.loads(request.POST['get_category_fields'])
            return get_fields_category(name=data)

    error_dict = {'os_path': []}

    def clear():
        if error_dict['os_path']:
            for i in error_dict['os_path']:
                try:
                    os.remove(i)
                except FileNotFoundError:
                    print(f'FileNotFoundError: {i}')
            error_dict['os_path'].clear()

    error_message = {
        1: '''<strong class="str-1">ERROR: There is not enough data to processes. 
        Please compile at least all necessary fields marked with</strong><strong class="str-2"> *. </strong>''',
        2: 'FILE ERROR: make sure that all files is right format',
        3: "ERROR: couldn't get id"
    }
    if 'name-data' in request.POST and 'description-data' in request.POST and 'selected-img' in request.FILES:
        def load_files(name_id, name):
            # loads main images
            for img_name in request.FILES:
                if 'input-file' in img_name and 'input-file-des' not in img_name:
                    response = SetMainImg(0, request.FILES[img_name], name_id.id)
                    if 'path' in response:
                        error_dict['os_path'] += response['path']
                    elif 'error' in response:
                        return response['error']
                if 'selected-img' == img_name:
                    response = SetMainImg(1, request.FILES[img_name], name_id.id)
                    if 'path' in response:
                        error_dict['os_path'] += response['path']
                    elif 'error' in response:
                        return response['error']
            # load video file
            if 'input-video-file' in request.FILES:
                try:
                    path = video_load_initial(request.FILES['input-video-file'])
                    if type(path) == dict:
                        try:
                            ProductVideoFile.objects.create(video_file=os.path.join(path['path'], path['file_name']),
                                                            video_id_id=name_id.id)
                            error_dict['os_path'].append(
                                os.path.join(settings.MEDIA_ROOT, path['path'], path['file_name']))
                        except Exception:
                            try:
                                os.remove(os.path.join(settings.MEDIA_ROOT, path['path'], path['file_name']))
                            except FileNotFoundError:
                                print(
                                    f"FileNotFoundError: {os.path.join(settings.MEDIA_ROOT, path['path'], path['file_name'])}")
                            return 'Object video error. Please Try Again!'
                    else:
                        return {'Make sure that video is right format and less than 500 Mbyte. Please try again!'}
                except Exception:
                    print('error', 'user_personal_area/utils', 'def load_files',
                          'can not find ProductVideoFile.objects')
                    return 'Object video error. Please Try Again!'

            # loads description information
            if 'description-data' in request.POST:
                description_data = json.loads(request.POST['description-data'])
                if 'des-title' in description_data:
                    try:
                        descr_id = ProductDescription.objects.create(title=description_data['des-title'].strip(' '),
                                                                     description_id_id=name_id.id)
                    except Exception:
                        return error_message[1]

                    # load description img
                    def load_des_img(n, id):
                        for name, file in request.FILES.items():
                            if f'part-{n}:input-file-des' in name:
                                path = set_des_img(file, hd_size=1280)
                                if not path:
                                    return 'Make sure that images is right format. Please try again!'
                                try:
                                    DescriptionImgFile.objects.create(
                                        img_file=os.path.join(path['path'], path['file_name']), img_id_id=id)
                                    error_dict['os_path'].append(
                                        os.path.join(settings.MEDIA_ROOT, path['path'], path['file_name']))
                                except Exception:
                                    try:
                                        os.remove(os.path.join(settings.MEDIA_ROOT, path['path'], path['file_name']))
                                    except FileNotFoundError:
                                        print(
                                            f"FileNotFoundError: {os.path.join(settings.MEDIA_ROOT, path['path'], path['file_name'])}")
                                    return 'Error to Loading Images. Please Try Again!'

                    for key, value in description_data.items():
                        if 'description' in key:
                            try:
                                text_id = DescriptionText.objects.create(text_description=value.strip(' '),
                                                                         text_id_id=descr_id.id)
                            except Exception:
                                return error_message[3]
                            response = load_des_img(key[-1], text_id.id)
                            if response:
                                return response

                    if 'table' in description_data:
                        try:
                            DescriptionTable.objects.create(table=description_data['table'].replace(' ', ''),
                                                            table_id_id=descr_id.id)
                        except Exception:
                            return error_message[3]

                    if 'doc_file' in request.FILES:
                        try:
                            DescriptionFile.objects.create(file=request.FILES['doc_file'], file_id_id=descr_id.id)
                        except Exception:
                            return "Can not load document file. Please try again"
                else:
                    return error_message[1]
            else:
                return error_message[1]

            # set date in model fields for search
            if 'model_fields' in request.POST:
                if request.POST['model_fields']:
                    model_fields = json.loads(request.POST['model_fields'])
                    try:
                        form = get_fields_category(name, True)
                        form = form(model_fields)
                        if form.is_valid():
                            form = form.save(commit=False)
                            form.product_id_id = name_id.id
                            form.save()
                        else:
                            print(
                                f'error: Can not save field object {name["slug"]}!, user_personal_area/utils/set_new_product/load_files')
                    except Exception:
                        print('error: user_personal_area/utils/set_new_product, could not find form')

        # loads main information
        data = json.loads(request.POST['name-data'])
        if 'product_id' in data and 'title' in data and 'price' in data and 'quantity' in data and 'name' in data:
            data['products_item_id'] = int(data['product_id'])
            data['user_id'] = request.user.user_id
            data['slug'] = get_slag(data['title'])
            data['product_id'] = get_product_id(request.user.user_id[-3:])
            name = {'slug': data['name'], 'category': data['category']}
            data.pop('name')
            data.pop('category')
            try:
                obj = ProductName.objects.create(**data)
            except Exception:

                return {'error': error_message[1]}
            error = load_files(obj, name)
            if error:
                try:
                    clear()
                    obj.delete()
                except Exception:
                    return {'error': [error + ' ,Delete error.']}
                return {'error': [error]}
        else:
            return {'error': [error_message[1]]}
    else:
        return {'error': [error_message[1]]}


# edit block


# EDIT PRODUCT BLOCK -----------EDIT PRODUCT BLOCK---------------EDIT PRODUCT BLOCK---------------EDIT PRODUCT BLOCK----
def set_edit_product(request):
    if 'get_category_fields' in request.POST:
        if request.POST['get_category_fields']:
            data = json.loads(request.POST['get_category_fields'])
            return get_product_cat_fields(data)

    if 'name-data' in request.POST and 'description-data' in request.POST and 'name_id' in request.POST:
        # add description img files if in request.FILES
        def load_img_files(k, img):
            if request.FILES:
                quan_obj = get_product_img_queryset(img.id).count()
                quan_obj = description_img_limit - quan_obj
                for name, file in request.FILES.items():
                    if not quan_obj:
                        break
                    if f'part-{k[-1]}:input-file-des-' in name:
                        path = set_des_img(file, hd_size=1280)
                        if not path:
                            return {
                                'error': 'Images ERROR: Make sure that all files are right format. Please try again!'}
                        try:
                            DescriptionImgFile.objects.create(
                                img_file=os.path.join(path['path'], path['file_name']), img_id_id=img.id)
                        except Exception:
                            try:
                                os.remove(os.path.join(settings.MEDIA_ROOT, path['path'], path['file_name']))
                            except FileNotFoundError:
                                print(
                                    f"FileNotFoundError: {os.path.join(settings.MEDIA_ROOT, path['path'], path['file_name'])}")
                            print('error', 'user_personal_area/utils.py', 'def load_img_files',
                                  'can not create object')
                            return {'error': 'Server ERROR: can not create object'}
                        quan_obj -= 1

        def load_descriptions_img(k, img):
            # control and delete description img files, if it not in list
            if 'edit-data-des-img' in request.POST:
                try:
                    description_img = json.loads(request.POST['edit-data-des-img'])
                    objects = get_product_img_queryset(img.id)
                    for obj in objects:
                        boolean = False
                        for key, value in description_img.items():
                            if f'part-{k[-1]}:input-file-des-' in key:
                                if value['path'] == obj.img_file and obj.id == int(value['id']):
                                    boolean = True
                                    break
                        if not boolean:
                            path = os.path.join(settings.MEDIA_ROOT, str(obj.img_file))
                            obj.delete()
                            try:
                                os.remove(path)
                            except FileNotFoundError:
                                print(f'FileNotFoundError: {path}')
                except Exception:
                    print('error', 'user_personal_area/utils.py', 'load_descriptions_img',
                          'can not get DescriptionImgFile')
                    return {'error': 'Server ERROR: can not find object'}

        def load_descriptions_title(description):
            description_data = json.loads(request.POST['description-data'])
            if 'des-title' in description_data:
                try:
                    description = ProductDescription.objects.get(description_id_id=description.id)
                    description.title = description_data['des-title'].strip(' ')
                    description.save()
                    description_data.pop('des-title')
                    if 'table' in description_data:
                        table = DescriptionTable.objects.filter(table_id_id=description.id)
                        if len(table):
                            table.update(table=description_data['table'])
                            description_data.pop('table')
                        else:
                            DescriptionTable.objects.create(table=description_data['table'], table_id_id=description.id)
                            description_data.pop('table')
                except Exception:
                    print('error', 'user_personal_area/utils.py', 'def load_descriptions_title',
                          'can not get ProductDescription.objects')
                    return {'error': 'Server ERROR: can not find object'}

                # changing text in description text control end delete

                if len(description_data) <= 3:
                    try:
                        del_des_data = {}
                        text = DescriptionText.objects.filter(text_id_id=description.id)
                        for i in range(len(text)):
                            boolean = False
                            for key, value in description_data.items():
                                if i + 1 == int(key[-1]):
                                    q = text[i]
                                    q.text_description = value.strip(' ')
                                    q.save()
                                    boolean = True
                                    response = load_descriptions_img(key, q)
                                    if response:
                                        return response
                                    response = load_img_files(key, q)
                                    if response:
                                        return response
                                    del_des_data[key] = value
                                    break
                            if not boolean:
                                text[i].delete()

                        for key in del_des_data.keys():
                            description_data.pop(key)

                        if description_data:
                            for k, v in description_data.items():
                                q = DescriptionText.objects.create(text_description=v, text_id_id=description.id)
                                load_img_files(k, q)
                    except Exception:
                        print('error', 'user_personal_area/utils.py', 'def load_descriptions_title',
                              'can not get DescriptionText.objects')
                        return {'error': 'Server ERROR: can not find object!'}
                else:
                    print('error', 'user_personal_area/utils.py', 'def load_descriptions_title',
                          f'quantity exceeded, quantity = {len(description_data)}')
                    return {'error': 'Quantity ERROR: Quantity text exceeded!'}

        # delete main img if img was change
        def load_main_img(img):
            if 'edit-data-main-img' in request.POST:
                try:
                    main_img = json.loads(request.POST['edit-data-main-img'])
                    objectsSD = get_product_imgfile_queryset(img.id)
                    objectsHD = ProductImgFileHD.objects.filter(img_id_id=img.id)
                    for objSD in objectsSD:
                        boolean = False
                        for key, value in main_img.items():
                            if 'input-file' in key:
                                if value['path'] == objSD.img_file and objSD.id == int(value['id']):
                                    if 'selected' in value and value['selected']:
                                        objSD.is_main = 1
                                        objSD.save()
                                    else:
                                        objSD.is_main = 0
                                        objSD.save()
                                    boolean = True
                                    break
                                elif value['path'] == objSD.img_file or objSD.id == int(value['id']):
                                    print('error', 'user_personal_area/utils', 'def load_main_img', 'value error')
                                    return {'error': 'Value ERROR: Loading images. Please Try Again!'}
                        if not boolean:
                            for objHD in objectsHD:
                                if objSD.id == objHD.id and objSD.img_id_id == objHD.img_id_id:
                                    path = os.path.join(settings.MEDIA_ROOT, str(objHD.img_file))
                                    objHD.delete()
                                    try:
                                        os.remove(path)
                                    except FileNotFoundError:
                                        print(f'FileNotFoundError: {path}')
                                    break
                            path = os.path.join(settings.MEDIA_ROOT, str(objSD.img_file))
                            objSD.delete()
                            try:
                                os.remove(path)
                            except FileNotFoundError:
                                print(f'FileNotFoundError: {path}')
                except Exception:
                    print('error', 'user_personal_area/utils', 'def load_main_img', 'can not find Query object',
                          'object error')
                    return {'error': 'Object ERROR: Loading images. Please Try Again!'}

        # load main img if exist in request files
        def load_main_img_file(img):
            if request.FILES:
                quan_obj = get_product_imgfile_queryset(img.id).count()
                quan_obj = main_img_limit - quan_obj
                for name, file in request.FILES.items():
                    if not quan_obj:
                        break
                    if not 'input-file-des' in name and 'input-file' in name:
                        response = SetMainImg(0, file, img.id)
                        if response:
                            return response
                        quan_obj -= 1
                    elif 'selected-img' in name:
                        response = SetMainImg(1, file, img.id)
                        if response:
                            return response
                        quan_obj -= 1

        # delete video if video was change
        def load_video_file(video):
            if 'input-video-file' in request.FILES:
                try:
                    objects = get_product_videofile_queryset(video.id).count()
                    if objects >= video_limit:
                        print('error: trying to load many videos')
                        return 'error: can not save video file'
                    else:
                        path = video_load_initial(request.FILES['input-video-file'])
                        if type(path) == dict:
                            try:
                                ProductVideoFile.objects.create(
                                    video_file=os.path.join(path['path'], path['file_name']), video_id_id=video.id)
                            except Exception:
                                try:
                                    os.remove(os.path.join(settings.MEDIA_ROOT, path['path'], path['file_name']))
                                except FileNotFoundError:
                                    print(
                                        f"FileNotFoundError: {os.path.join(settings.MEDIA_ROOT, path['path'], path['file_name'])}")
                                return {
                                    'error': 'Server ERROR: Can not find object. Please try again!'}
                        else:
                            return {'error': 'Video ERROR: Make sure that video is right format. Please try again!'}
                except Exception:
                    print('error', 'user_personal_area/utils', 'def load_video_file',
                          'can not find ProductVideoFile.objects')
                    return {'error': 'Object ERROR: Loading Video. Please Try Again!'}

        # load video if video exist in request files
        def load_video(vid):
            if 'input-video-file' in request.FILES:
                file = request.FILES['input-video-file']
                try:
                    path = file.temporary_file_path()
                    if os.path.getsize(path) > 500000000:
                        file.close()
                        return {
                            'error': 'Video ERROR: Make sure that video is right format and less than 500Mbyte. Please try again!'}
                except Exception:
                    return {
                        'error': 'Video ERROR: Make sure that video is right format and less than 500Mbyte. Please try again!'}
            if 'edit-data-video' in request.POST:
                try:
                    video = json.loads(request.POST['edit-data-video'])
                    objects = get_product_videofile_queryset(vid.id)
                    if int(video['input-video-file']['id']) == objects[0].id and video['input-video-file'][
                        'path'] == 'delete':
                        path = os.path.join(settings.MEDIA_ROOT, str(objects[0].video_file))
                        objects[0].delete()
                        try:
                            os.remove(path)
                        except FileNotFoundError:
                            print(f'FileNotFoundError: {path}')
                    elif int(video['input-video-file']['id']) != objects[0].id or video['input-video-file']['path'] != \
                            objects[0].video_file:
                        print('error', 'user_personal_area/utils', 'def load_video', 'matching error')
                        return {'error': 'Data ERROR: Data was compromised!'}
                except Exception:
                    print('error', 'user_personal_area/utils', 'def load_video',
                          'can not find ProductVideoFile.objects')
                    return {'error': 'Object ERROR: Loading Video. Please Try Again!'}



        def set_fields(name, fields):
            fields = json.loads(fields)
            if fields:
                model = get_model(name['category'], name['slug'])
                form = get_form(name['category'], name['slug'])
                if model and form:
                    try:
                        model = model.objects.get(product_id_id=name['id'])
                        form = form(fields, instance=model)
                    except Exception:
                        form = form(fields)
                        # return {'error': 'Object ERROR: Changing searching data. Please Try Again!'}
                    if form.is_valid():
                        form = form.save(commit=False)
                        form.product_id_id = name['id']
                        form.save()
                    else:
                        return form.errors

        data = json.loads(request.POST['name-data'])
        if 'product_id' in data and 'title' in data and 'price' in data and 'quantity' in data:
            data['products_item_id'] = int(data['product_id'])
            data.pop('product_id')
            slug = {'slug': data['name'], 'id': request.POST['name_id'], 'category': data['category']}
            if 'preview' in data:
                slug['preview'] = data['preview']
                data.pop('preview')
            data.pop('name')
            data.pop('category')
            # try:
            name = ProductName.objects.filter(user_id=request.user.user_id, id=request.POST['name_id'])
            if data['products_item_id'] != name[0].products_item_id:
                try:
                    model = get_model(slug['preview']['category'], slug['preview']['slug'])
                    model = model.objects.get(product_id_id=slug['id'])
                    model.delete()
                except Exception:
                    pass
            name.update(**data)
            # except Exception:
            #    print('error user_personal_area/utils name-data')
            #    return {'error': '<strong class="str-1">Server Error:can not load object </strong>'}

            response = load_main_img(name[0])
            if response and 'error' in response:
                return {'error': f"<strong class='str-1'>{response['error']}</strong>"}
            response = load_main_img_file(name[0])
            if response and 'error' in response:
                return {'error': f"<strong class='str-1'>{response['error']}</strong>"}
            response = load_descriptions_title(name[0])
            if response and 'error' in response:
                return {'error': f"<strong class='str-1'>{response['error']}</strong>"}
            response = load_video(name[0])
            if response and 'error' in response:
                return {'error': f"<strong class='str-1'>{response['error']}</strong>"}
            response = load_video_file(name[0])
            if response and 'error' in response:
                return {'error': f"<strong class='str-1'>{response['error']}</strong>"}
            if 'model_fields' in request.POST:
                response = set_fields(slug, request.POST['model_fields'])
                if response:
                    pass
        else:
            return {'error': '''<strong class="str-1">ERROR: There is not enough data to processes. 
        Please compile at least all necessary fields marked with</strong><strong class="str-2"> *. </strong>'''}
    else:
        return {'error': ''''<strong class="str-1">ERROR: There is not enough data to processes. 
        Please compile at least all necessary fields marked with</strong><strong class="str-2"> *. </strong>'''}


def file_delete(obj, value):
    if obj and value == 'img':
        for item in obj:
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(item.img_file)))
            except FileNotFoundError:
                print(f'FileNotFoundError: {os.path.join(settings.MEDIA_ROOT, str(item.img_file))}')
    elif obj and value == 'video':
        for item in obj:
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(item.video_file)))
            except FileNotFoundError:
                print(f'FileNotFoundError: {os.path.join(settings.MEDIA_ROOT, str(item.video_file))}')


def delete_and_view(request):
    if 'set_publish' in request.POST and request.POST['set_publish']:
        data = json.loads(request.POST['set_publish'])
        try:
            obj = ProductName.objects.get(user_id=request.user.user_id, id=data['value'])
            obj.is_published = data['bool']
            obj.save()
        except Exception:
            print('error user_personal_area/utils delete_and_view set_publish')
            return {'error': 'Server Error:can not find object'}
        return {'success': 'item set as published'} if data['bool'] else {'success': 'item set as not published'}
    elif 'item_to_delete' in request.POST and request.POST['item_to_delete']:
        try:
            name = ProductName.objects.get(user_id=request.user.user_id, id=request.POST['item_to_delete'])
            file_delete(get_product_imgfile_queryset(name.id), 'img')
            file_delete(ProductImgFileHD.objects.filter(img_id_id=name.id), 'img')
            file_delete(get_product_videofile_queryset(name.id), 'video')
            obj = ProductDescription.objects.get(description_id_id=name.id)
            obj = DescriptionText.objects.filter(text_id_id=obj.id)
            for i in obj:
                file_delete(get_product_img_queryset(i.id), 'img')
            name.delete()
            # DescriptionFile
        except Exception:
            print('error user_personal_area/utils delete_and_view item_to_delete')
            return {'error': 'Server Error:can not find object'}
        return {'success': 'item was deleted successfully'}
