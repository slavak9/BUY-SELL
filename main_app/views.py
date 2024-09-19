import json

from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView

from products.forms import AddProductInCart
from django.views.generic import TemplateView
from .utils import DataMixing



class Home(DataMixing,TemplateView):
    template_name = 'main_app/home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        data_mixing = self.get_user_context(title='Home')
        context = dict(list(context.items()) + list(data_mixing.items()))
        if self.request.user.is_authenticated:
            data_mixing = self.get_user_context(items_in_the_cart=self.request.user.user_id)
            context = dict(list(context.items()) + list(data_mixing.items()))
        return context




def support(request):
    return HttpResponse('<h1>support</h1>')

def news(request):
    return HttpResponse('<h1>news</h1>')

def about(request,exception):
    if request.method == 'POST':
        data = {}
        form = AddProductInCart(request.POST)
        if form.is_valid():
            data['res_from_serv'] = True
            print(form.cleaned_data,data)
            return HttpResponse(json.dumps(data))
        else:
            data['res_from_serv'] = False
            return HttpResponse(json.dumps(data),content_type='application/json')
    else:
        form = AddProductInCart()
    return render(request,'main_app/about.html',{'form':form,'exception':exception})

def logout_user(request):
    logout(request)
    return redirect(request.GET['next'])





class HandlerError403(DataMixing,TemplateView):
    template_name ='main_app/handler_error403.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        data_mixing = self.get_user_context(title='Handler403')
        context = dict(list(context.items()) + list(data_mixing.items()))
        return context