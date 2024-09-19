import json
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView, TemplateView
from accounts.forms import RegisterForm
from accounts.models import UsersAccounts
from accounts.utils import get_user_id, registration_form_control, login_validation
from main_app.utils import DataMixing
from django.contrib.auth import login, logout

class Login(DataMixing,TemplateView):
    template_name = 'accounts/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        data_mixing = self.get_user_context(title='Login')
        context = dict(list(context.items()) + list(data_mixing.items()))
        return context

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('home')

    def get_success_url(self):
        if not self.request.GET:
            self.success_url = 'home'
        # elif self.request.GET['next'] == '/accounts/registration/':
        #     self.success_url = 'home'
        else:
            self.success_url = self.request.GET['next']
        return self.success_url

    def post(self, request, *args, **kwargs):
        user = login_validation(request)
        if user:
            login(request, user)
            return redirect(self.get_success_url())
        else:
            context = self.get_context_data(**kwargs)
            context['form_error'] = \
                'Please enter a correct username and password. Note that both fields may be case-sensitive.'
            return self.render_to_response(context)


class Register(DataMixing, FormView):
    form_class = RegisterForm
    template_name = 'accounts/registration.html'

    def get_success_url(self):
        self.success_url = ''
        return self.success_url

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        data_mixing = self.get_user_context(title='Sign up')
        context = dict(list(context.items()) + list(data_mixing.items()))
        return context

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('home')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        is_data_valid = registration_form_control(form)
        return HttpResponse(json.dumps(is_data_valid), content_type='application/json')


    def form_invalid(self, form):
        return HttpResponse(json.dumps(form.errors), content_type='application/json')


def forgotpassword(request):
    pass