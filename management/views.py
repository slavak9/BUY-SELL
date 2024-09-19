from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import ListView
from main_app.utils import DataMixing
from management.utils import DataMixOther,initial_category
from category.models import Categories
import json


class ManageCategory(DataMixing,DataMixOther,ListView):
    model = Categories
    template_name = 'management/manage_category.html'
    context_object_name = 'category_data'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        data_mixing = self.get_user_context(title='Manage Category')
        context = dict(list(context.items()) + list(data_mixing.items()))
        data_mixing = self.get_additional_context(category_items=True)
        context = dict(list(context.items()) + list(data_mixing.items()))
        return context


    # def dispatch(self, request, *args, **kwargs):
    #     if not self.request.user.is_authenticated:
    #         return super().dispatch(request, *args, **kwargs)
    #     else:
    #         return redirect('home')


    def get_queryset(self):
        return Categories.objects.all()


    def post(self, request, *args, **kwargs):
        print(request.POST)
        response = initial_category(request)
        if not response:
            return HttpResponse(json.dumps({'success': 1}))
        elif 'category_fields' in response:
            return HttpResponse(json.dumps({'category': response['category_fields']}))
        else:
            return HttpResponse(json.dumps({'error': response}))
      #  return HttpResponse(json.dumps({'error': 'hdsj'}))