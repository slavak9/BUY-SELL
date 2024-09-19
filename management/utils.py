from category.models import Categories, ItemCategory
from category.forms import CategoriesForm,ItemCategoryForm
import string
import json
from django.conf import settings
import os
from user_personal_area.manage_data import set_category_img
#from django.core.management import call_command

try:
    from products.choices import get_choice_values
    from products.form_files import get_form
    from products.models import get_model

except ImportError:
    print('error: at management/utils, could not import get_form or get_model or get_choice_values')
class DataMixOther:
    def get_additional_context(self,**kwargs):
        context = kwargs
        if 'category_items' in context:
            try:
              context['category_items'] = ItemCategory.objects.all()
            except Exception:
                pass
        return context


def get_slag(n: str):
    list_char = string.punctuation.replace('-','').replace('_','')
    slug = ''
    n = n.replace(' ','_')
    for i in n:
        if i in list_char:
            if slug[-1] != '-':
                slug += '-'
        else:
            slug += i
    return slug.lower().strip('-')


def clear_special_char(st: str):
    for i in string.punctuation.replace('_',''):
        if i in st:
            return False
    return st


def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            return lines
    except FileNotFoundError:
        return False
def write_file(path,lines):
    with open(path, 'w', encoding='utf-8') as file:
        if type(lines) == list:
            file.writelines(lines)
        elif type(lines) == str:
            file.write(lines)


def writer_corection(data):
    data = (data.replace(']},', ']},\n').replace('],', '],\n'))
    data = data.split('\n')
    for i in range(len(data)):
        if len(data[i]) > 110:
            L = len(data[i])
            new_str = ''
            start = 0
            while L > 110:
                index = data[i][start:start + 110].rfind(',')
                L -= index
                new_str += data[i][start:start + index + 1] + '\n'
                start += index + 1
            new_str += data[i][start:]
            data[i] = new_str
    data = '\n'.join(data)
    return data


def set_initial_choice(data):
    path = os.path.join(settings.BASE_DIR, 'products', 'choices', '__init__.py')
    lines = read_file(path)
    if lines:
        lines.append('00')
        for i in range(len(lines)):
            if f"from .{data['category_slug']} import {data['category_slug']}" in lines[i]:
                lines[-1] = '10'
                continue
            elif lines[-1] == '10':
                if f"def get_choice_values(name):\n" == lines[i]:
                    lines[-1] = '11'
                    continue
            elif lines[-1] == '11':
                if get_if_choice(data) == lines[i] or get_if_choice(data).replace('if', 'elif') == lines[i]:
                    lines.pop(-1)
                    break
                elif (lines[-1] == lines[i] and lines[-1] == '11'):
                    lines[-1] = get_if_choice(data).replace('if', 'elif')
                    break

            elif lines[-1] == '00' and lines[i] == '\n' and lines[i + 1] == '\n':
                lines[i] = f"from .{data['category_slug']} import {data['category_slug']}\n\n\n"
                lines[-1] = get_if_choice(data).replace('if', 'elif')
                break
        write_file(path, lines)
    else:
        lines = f"from .{data['category_slug']} import {data['category_slug']}\n\n\n"
        lines = lines + "def get_choice_values(name):\n" + get_if_choice(data)
        write_file(path, lines)

def set_choices_value(data):
    print(data)
    fields = data['fields']
    list_choice = data['fields_sub_choices']
    exist_choice = None
    if 'fields_sub_choices' not in data:
        return data
    set_initial_choice(data)
    try:
        exist_choice = get_choice_values(data['category_slug'])
    except Exception:
        print('ERROOR')
    def delete_empty_data():
        non_field = []
        for key, value in fields.items():
            if not value['fields']:
                non_field.append(key)
                continue
            name = {}
            for i in value['fields']:
                name[i] = {}
            fields[key] = name
        for i in non_field:
            fields.pop(i)
    delete_empty_data()

    def get_combined_value(v1, v2):
        if v2 and data['model'] in v2:
            v2 = v2[data['model']]
            for key, value in v1.items():
                if key in v2 and value:
                    for f_key, f_value in value.items():
                        if f_key not in v2[key]:
                            v2[key][f_key] = f_value
                elif value:
                    v2[key] = value
            return v2
        else:
            return v1

    def transform_sub_values(values):
        for key, value in values.items():
            s = value['field']
            value.pop('field')
            for s_key, s_value in value.items():
                value[s_key] = {s: set(s_value)}
        return values

    fields = get_combined_value(fields, exist_choice)
   # list_choice = transform_sub_values(list_choice)

    def get_united_value():
        for key, value in list_choice.items():
            if key in fields:  # IF BRAND IN FIELDS
                name = None
                for k, v in value.items():  # AUDI , GENER:[]
                    if k in fields[key]:  # IF AUDI IN BRAND OF FIELDS
                        fields[key][k] = v
                        name = list(v.keys())[0]
                for x, g in fields[key].items():
                    if g.keys():
                        fields[key][x][name] = list(g.values())[0]
    get_united_value()

    if exist_choice:
        exist_choice[data['model']] = fields
    else:
        exist_choice = {}
        exist_choice[data['model']] = fields

    path = os.path.join(settings.BASE_DIR, 'products', 'choices', f"{data['category_slug']}.py")
    string_data = writer_corection(f"{data['category_slug']} = " + str(exist_choice))
    with open(path, 'w', encoding='utf-8') as file:
        file.write(string_data)

def get_if_choice(data):
    return f"    if name == '{data['category_slug']}': return {data['category_slug']}\n"


def add_fields(data):
    fields = ''
    data = data['fields']
    for key, value in data.items():
        key = key.lower()
        if value['type'] == 'select' or value['type'] == 'string':
            fields += f"    {key} = models.CharField(max_length=30, default=None, null=True, blank=True, verbose_name='{key.capitalize()}')\n"
        elif value['type'] == 'integer':
            fields += f"    {key} = models.IntegerField(blank=True,default=None, null=True, verbose_name='{key.capitalize()}')\n"
        elif value['type'] == 'decimal':
            fields += f"    {key} = models.DecimalField(max_digits=10, default=None, null=True, decimal_places=2, blank=True, verbose_name='{key.capitalize()}')\n"
        elif value['type'] == 'check':
            fields += f"    {key} = models.BooleanField(default=False, verbose_name='{key.capitalize()}')\n"
    return fields


def create_fields(data):
    return add_fields(data) + f"    product_id = models.ForeignKey('ProductName', on_delete=models.CASCADE)\n"


def get_if_field(data):
    return f"    if model == '{data['model'].lower()}': return {data['model']}Form\n"

def get_if_model(data):
    return f"    if category == '{data['category_slug'].lower()}': return get_form_{data['category_slug']}(model)\n"


def get_if_field_m(data):
    return f"    if model == '{data['model'].lower()}': return {data['model']}\n"

def get_if_model_m(data):
    return f"    if category == '{data['category_slug'].lower()}': return get_model_{data['category_slug']}(model)\n"

def write_initial_form(data):
    path = os.path.join(settings.BASE_DIR, 'products', 'form_files', '__init__.py')
    lines = read_file(path)
    if lines:
        lines.append('00')
        for i in range(len(lines)):
            if f"from .{data['category_slug']} import *" in lines[i]:
                lines[-1] = '10'
                continue
            elif lines[-1] == '00' and lines[i] == '\n' and lines[i+1] == '\n':
                lines[i] = f"from .{data['category_slug']} import *\n\n\n"
                lines[i+1] = f"def get_form_{data['category_slug']}(model):\n" + get_if_field(data) + '\n\n'
                lines[-1] = '21'
                continue
            elif lines[-1] == '10':
                if f"def get_form_{data['category_slug']}(model):\n" == lines[i]:
                    lines[-1] = '11'
                    continue
            elif lines[-1] == '11':
                if get_if_field(data) == lines[i] or get_if_field(data).replace('if', 'elif') == lines[i]:
                    lines[-1] = '21'
                    continue
                elif lines[i] == '\n' and lines[i+1] == '\n':
                    lines[i] = get_if_field(data).replace('if','elif') + '\n'
                    lines[-1] = '21'
                    continue
            elif lines[-1] == '21':
                if "def get_form(category, model):\n" == lines[i]:
                    lines[-1] = '22'
                    continue
            elif lines[-1] == '22':
                if get_if_model(data) == lines[i] or get_if_model(data).replace('if', 'elif') == lines[i]:
                    lines.pop(-1)
                    break
                elif lines[i] == '22' and lines[-1] == '22':
                    lines[i] = get_if_model(data).replace('if', 'elif')

        write_file(path,lines)
    else:
        text = f"from .{data['category_slug']} import *\n\n\n"
        text = text + f"def get_form_{data['category_slug']}(model):\n" + get_if_field(data) \
               + '\n\n' + "def get_form(category, model):\n" + get_if_model(data)
        write_file(path,text)


# create form model for models in from_files
def get_form_class(data):
    return f"""class {data['model']}Form(forms.ModelForm):
    class Meta:  
        model = {data['model']}
        fields = {list(data['fields'].keys())}\n\n\n"""


# check if file form exist, if not make it and write fields data for sub category
def create_forms(data):
    #data['fields'] = list(data['fields'].keys())
    path = os.path.join(settings.BASE_DIR, 'products', 'form_files', f"{data['category_slug']}.py")
    lines = read_file(path)
    if lines:
        lines.append('00')
        fields = None
        for index in range(len(lines)-1):
            # checks if model already imported from category,if not, import it and add FORM CLASS
            if f"from products.models.{data['category_slug']} import *" in lines[index]:
                lines[-1] = '10'
                continue
            elif lines[-1] == '00' and lines[index] == '\n' and lines[index+1] == '\n':
                lines[index] = lines[index].strip('\n') + f"from products.models.{data['category_slug']} import *\n\n"
                lines.pop(-1)
                lines.append(get_form_class(data))
                lines.append('10')
                break

            # controls and add fields in field list
            elif lines[-1] == '10' and f"class {data['model']}Form(forms.ModelForm):" in lines[index]:
                lines[-1] = '11'
                continue
            elif lines[-1] == '11':
                fields = list(data['fields'].keys())
                for field in fields:
                    if f"'{field}'" in lines[index]:
                        fields.remove(field)
            if ']' in lines[index] and lines[-1] == '11' and fields:
                fields = ', '.join([f"'{i}'" for i in fields])
                if (len(lines[index]) + len(fields)) > 115:
                    lines[index] = lines[index].replace(']',f',\n       {fields}]')
                else:
                    lines[index] = lines[index].replace(']',f', {fields}]')
                break
        if lines[-1] == '10':
            lines.pop(-1)
            lines.append(get_form_class(data))
        else:
            lines.pop(-1)
        write_file(path,lines)
        write_initial_form(data)
    else:
        text = f"from django import forms\nfrom products.models.{data['category_slug']} import *\n\n\n"
        write_file(path,text + get_form_class(data))
        write_initial_form(data)


# write new model name, if file was imported, else write import new file end model name in init.py
def create_field_init(data):
    path = os.path.join(settings.BASE_DIR, 'products', 'models', "__init__.py")
    lines = read_file(path)
    if lines:
        lines.append('00')
        for i in range(len(lines)):
            if f"from .{data['category_slug']} import *\n" == lines[i]:
                lines[-1] = '10'
                continue
            elif lines[-1] == '00' and lines[i] == '\n' and lines[i + 1] == '\n':
                lines[i] = f"from .{data['category_slug']} import *\n\n\n"
                lines[i + 1] = f"def get_model_{data['category_slug']}(model):\n" + get_if_field_m(data) + '\n\n'
                lines[-1] = '21'
                continue
            elif lines[-1] == '10':
                if f"def get_model_{data['category_slug']}(model):\n" == lines[i]:
                    lines[-1] = '11'
                    continue
            elif lines[-1] == '11':
                if get_if_field_m(data) == lines[i] or get_if_field_m(data).replace('if', 'elif') == lines[i]:
                    lines[-1] = '21'
                    continue
                elif lines[i] == '\n' and lines[i + 1] == '\n':
                    lines[i] = get_if_field_m(data).replace('if', 'elif') + '\n'
                    lines[-1] = '21'
                    continue
            elif lines[-1] == '21':
                if "def get_model(category, model):\n" == lines[i]:
                    lines[-1] = '22'
                    continue
                elif lines[i] == lines[-1]: # should be 21
                    lines[i] = "def get_model(category, model):\n" + get_if_model_m(data)
            elif lines[-1] == '22':
                if get_if_model_m(data) == lines[i] or get_if_model_m(data).replace('if', 'elif') == lines[i]:
                    lines.pop(-1)
                    break
                elif lines[i] == lines[-1]: # should be 22
                    lines[i] = get_if_model_m(data).replace('if', 'elif')
        write_file(path,lines)
    else:
        text = f"from django.db import models\n from .main_models import *\n from .{data['category_slug']} import *\n\n\n"
        text = text + f"def get_model_{data['category_slug']}(model):\n" + get_if_field_m(data).replace('Form', '') \
               + '\n\n' + "def get_model(category, model):\n" + get_if_model_m(data)
        write_file(path, text)


def clear__slash(st:str):
    if '__' in st:
        st = st.replace('__','_')
        return clear__slash(st)
    else:
        return st

# check for special characters allow only _ and (). if characters exist, delete field with character and return error
def check_special_char(data: dict):
    charset = string.punctuation.replace('_','')
    errors = []
    fields_copy = data['fields'].copy()
    for key in fields_copy.keys():
        new_key = key.strip(' ').replace(' ', '_')
        new_key = clear__slash(new_key)
        for char in charset:
            if not new_key.replace('_','') or char in new_key:
                data['fields'].pop(key)
                errors.append(key)
                break
        if new_key not in data['fields'] and key in data['fields']:
            data['fields'][new_key] = data['fields'][key]
            data['fields'].pop(key)
    if errors:
        if 'model_fields_error' in data:
            if data['model_fields_error'] == list:
                errors += data['model_fields_error']
                data['model_fields_error'] = {
                    'server': [f'Could not create fields: {",".join(errors)}! Allowed only letters with numbers']}
            else:
                data['model_fields_error'] = {
                    'server': [f'Could not create fields: {",".join(errors)}! Allowed only letters with numbers',
                               data['model_fields_error']]}
    return data
# create new model file if not exist and write data for sub category

def check_sub_special_char(data):
    if 'fields_sub_choices' not in data:
        return data
    charset = string.punctuation.replace('_', '')
    errors = []
    fields = data['fields_sub_choices']
    try:
        for key, value in fields.items():
            s = clear__slash(value['field'].strip(' ').replace(' ', '_'))
            for char in charset:
                if not s.replace('_', '') or char in s:
                    errors.append(value['field'])
                    fields[key] = {}
                    break
            if fields[key]:
                data['fields'][key+'_choices_to_select'] = {'type': 'string', 'fields': []}
                s = value['field']
                value.pop('field')
                for s_key, s_value in value.items():
                    value[s_key] = {s: set(s_value)}
        if errors:
            data['model_fields_error'] = errors
    except Exception:
        data['model_fields_error'] = 'Could not create fields for sub category'
    return data


def create_model(data):
    model = ''.join([i.capitalize() for i in data['slug'].split('_')])
    data['model'] = model
    path = os.path.join(settings.BASE_DIR, 'products', 'models', f"{data['category_slug']}.py")
    data = check_sub_special_char(data)
    data = check_special_char(data)
   # data = set_choices_fields(data, path)
    lines = read_file(path)
    if lines:
        lines = read_file(path)
        lines.append('false')
        for index in range(len(lines)-1):
            if f"class {data['model']}(models.Model):" in lines[index]:
                lines[-1] = ('true')
                continue
            elif lines[-1] == 'true':
                keys = list(data['fields'].keys())
                for i in keys:
                    g = i.lower() + ' ='
                    if g in lines[index] and (lines[index].strip(' '))[0:len(g)] == g:
                        data['fields'].pop(i)
                if lines[index] == '\n' and lines[index+1] == '\n':
                    lines[index] = lines[index].strip('\n') + add_fields(data) +'\n'
                    break
        if lines[-1] == 'false':
            lines.pop(-1)
            model = f"class {model}(models.Model):\n" + create_fields(data) + '\n\n'
            lines.append(model)
            lines.append('false')

        lines.pop(-1)
        write_file(path,lines)
    else:
        model = f"class {model}(models.Model):\n" + create_fields(data) + '\n\n'
        initial = "from django.db import models\nfrom products.models import ProductName\n\n\n"
        write_file(path, initial + model)

    create_forms(data)
    set_choices_value(data)
    model = create_field_init(data)
    if 'model_fields_error' in data:
        return data['model_fields_error']
    else:
        return model
    

# create new category block
def create_categories(request):
        try:
            data = json.loads(request.POST['create_category'])
            data['slug'] = get_slag(data['name'])
            form = CategoriesForm(data)
            if form.is_valid() and request.FILES['file']:
                path = set_category_img(request.FILES['file'], True, sd_size=960)
                if not path:
                    form.add_error('img_categories', 'Image error: Make sure that file is Image!')
                    return form.errors
                form = form.save(commit=False)
                form.img_categories = os.path.join(path['path'], path['file_name'])
                form.save()
            else:
                if not request.FILES['file']:
                    form.add_error('img_categories', 'Image error: Make sure that Image is uploaded!')
                return form.errors
        except Exception:
            print('ERROR DATA:could not manage data source: management.utils.create_categories')
            return {'server':['Could not create category!']}


# edit existing category block
def edit_category(request):
    try:
        data = json.loads(request.POST['edit_category'])
        data['slug'] = get_slag(data['name'])
        obj = Categories.objects.get(id=data['id'])
        form = CategoriesForm(data,instance=obj)
        data = None
        if request.FILES:
            data = set_category_img(request.FILES['file'], True, sd_size=960)
        if form.is_valid():
            form = form.save(commit=False)
            if data:
                os.remove(os.path.join(settings.MEDIA_ROOT,str(obj.img_categories)))
                form.img_categories = os.path.join(data['path'], data['file_name'])
            form.save()
        else:
            return form.errors
    except Exception:
        print('ERROR DATA:could not manage data, source: management.utils.edit_category')
        return {'server': ['Could not edit category!']}


def check_fields(request,form):
    if 'fields' in request.POST:
        data = json.loads(request.POST['fields'])
        if data:
            data = {'fields': data, 'slug':form.slug}
            if 'fields_sub_choices' in request.POST:
                data['fields_sub_choices'] = json.loads(request.POST['fields_sub_choices'])
            try:
                data['category_slug'] = Categories.objects.values('slug').get(id=form.category_id_id)['slug']
            except Exception:
                print('Object error:category can not find object file, source: management.utils.check_fields')
                return {'server': ['Could not find category!']}
            return create_model(data)


# create sub category block
def create_item_category(request):
   # try:
        data = json.loads(request.POST['create_item_category'])
        data['slug'] = get_slag(data['name'])
        form = ItemCategoryForm(data)
        if form.is_valid() and request.FILES['file']:
            path = set_category_img(request.FILES['file'], False, sd_size=960)
            if not path:
                form.add_error('img_item_category', 'Image error: Make sure that file is Image!')
                return form.errors
            form = form.save(commit=False)
            form.img_item_category = os.path.join(path['path'], path['file_name'])
            form.save()
            return check_fields(request,form)
        else:
            if not request.FILES['file']:
                form.add_error('img_item_category', 'Image error: Make sure that Image is uploaded!')
            return form.errors
  #  except Exception:
   #     print('ERROR DATA:could not manage data, source: management.utils.create_item_category')
   #     return {'server': ['Could not create sub category!']}


# edit sub category block
def edit_item_category(request):
    try:
        data = json.loads(request.POST['edit_item_category'])
        obj = ItemCategory.objects.get(id=data['id'])
        data['category_id'] = obj.category_id_id
        data['slug'] = obj.slug
        form = ItemCategoryForm(data, instance=obj)
        data = None
        if request.FILES:
            data = set_category_img(request.FILES['file'], False, sd_size=960)
        if form.is_valid():
            form = form.save(commit=False)
            if data:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(obj.img_item_category)))
                form.img_item_category = os.path.join(data['path'], data['file_name'])
            form.save()
        else:
            return form.errors
        return check_fields(request,form)
    except Exception:
        print('ERROR DATA:could not manage data, source: management.utils.edit_item_category')
        return {'server': ['Could not edit sub category!']}


def get_model_form(name):
    def name_type(html):
        return [s for s in html.split(' ') if 'name=' in s or 'type=' in s]
    name = json.loads(name)
    model = {}
    try:
        obj = Categories.objects.get(id=name['id']).slug
        name['id'] = obj
        form = get_form(obj, name['slug'])
        choices = get_choice_values(name['id'])[name['slug'].capitalize()]
        print(choices)
        for html in form():
            html = str(html).replace('\n\n', '\n')
            print(html)
            n_st = name_type(html)
            n_st[1] = (n_st[1].replace('"', '').replace('name=', ''))
            if n_st[1] in choices:
                list_options = []
                for key, value in choices[n_st[1]].items():
                    list_options.append(f'<option value="{key}">{key.capitalize()}</option>')






       #     if '<select' in html and '</select>' in html:
       #        n_st = name_type(html)
       #         n_st = n_st[0][n_st[0].find('"') + 1:n_st[0].rfind('"')]
       #         model[n_st.capitalize()] = html
       #     else:
       #         n_st = name_type(html)
       #         model[n_st[1][n_st[1].find('"') + 1:n_st[1].rfind('"')]] = n_st[0][
       #                                                                    n_st[0].find('"') + 1:n_st[0].rfind('"')]
       # model = {'category_fields': model}
       # print(model)
       # return model
    except ImportError:
        print('error: at user_personal_area/utils, get_form is not exists yet')
        return {'category_fields': 'None'}

def initial_category(request):
    if 'request_model_fields' in request.POST:
        if request.POST['request_model_fields']:
            return get_model_form(request.POST['request_model_fields'])
    elif 'create_category' in request.POST and request.FILES:
        return create_categories(request)
    elif 'edit_category' in request.POST:
        return edit_category(request)
    elif 'create_item_category' in request.POST and request.FILES:
        return create_item_category(request)
    elif 'edit_item_category' in request.POST:
        return edit_item_category(request)