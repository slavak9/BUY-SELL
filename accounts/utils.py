import random
import string
import datetime
from django.contrib.auth import authenticate
from accounts.models import UsersAccounts


def random_user_id():
    classification = 'CL_'
    number_id = random.choices(range(0, 10), k=12)
    return classification + str(number_id).strip('[]').replace(', ', '')

def get_user_id():
    user_id = random_user_id()
    try:
        UsersAccounts.objects.get(user_id=user_id)
        return get_user_id()
    except Exception:
        return user_id


def date_of_birth(date):
    value = {}
    if len(date) > 10:
        value['date_of_birth'] = 'The date is not valid'
        return value
    limit_min_years = 12
    limit_max_years = 150
    birth_date = datetime.datetime.strptime(date, '%Y %m %d')
    current_day = datetime.datetime.now()
    limit_min_date = datetime.datetime(current_day.year-limit_min_years, current_day.month, current_day.day)
    limit_max_date = datetime.datetime(current_day.year-limit_max_years, current_day.month, current_day.day)

    if birth_date > current_day:
        value['date_of_birth'] = "The date of birth, can not be grater then actual date"
        return value
    elif birth_date > limit_min_date:
        value['date_of_birth'] = "You can not register. You are too young"
        return value
    elif birth_date < limit_max_date:
        value['date_of_birth'] = "We don't think that you are more then 150 years old."
        return value
    else:
        return value


def password_control(password):
    list_value = [False, False, False, False]
    for i in password:
        if i in string.digits and not list_value[0]:
            list_value[0] = True
        if i in string.punctuation and not list_value[1]:
            list_value[1] = True
        if i in string.ascii_uppercase and not list_value[2]:
            list_value[2] = True
        if i in string.ascii_lowercase and not list_value[3]:
            list_value[3] = True
    if False in list_value:
        return {'password2': 'Password must contain at least one: Uppercase letter,special character and number'}
    return {}


def registration_form_control(form):
    error = password_control(form.cleaned_data['password1'])
    if error:
        return error
    error = date_of_birth(form.cleaned_data['date_of_birth'].replace('-', ' '))
    if error:
        return error
    commit_form = form.save(commit=False)
    commit_form.user_id = get_user_id()
    commit_form.save()
    error['success'] = True
    return error


def get_query_object(email):
    try:
        return UsersAccounts.objects.get(email=email).username
    except Exception:
        return False

def login_validation(request):
    value = request.POST['email']
    password = request.POST['password']
    if '@' in value:
        username = get_query_object(value)
        if username:
            user = authenticate(request, username=username, password=password)
            return user
        else:
            return False
    else:
        user = authenticate(request, username=value, password=password)
        return user

# things to do
# make time password protection
#
# asing user permision group