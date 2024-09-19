from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from main_app.utils import DataMixing
from category.models import Categories,ItemCategory


class ShowCategory(DataMixing,ListView):
    model = Categories
    template_name = 'category/main_category.html'
    context_object_name = 'category_data'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        data_mixing = self.get_user_context(title='Category')
        context = dict(list(context.items()) + list(data_mixing.items()))
        if self.request.user.is_authenticated:
            data_mixing = self.get_user_context(items_in_the_cart=self.request.user.user_id)
            context = dict(list(context.items()) + list(data_mixing.items()))
        return context

    def get_queryset(self):
        return Categories.objects.filter(is_published=True)


class ChosenCategory(DataMixing, ListView):
    model = ItemCategory
    template_name = 'category/chosen_category.html'
    context_object_name = 'chosen'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        data_mixing = self.get_user_context(title=f"{self.kwargs['category_slug']}".replace('_', ' ').capitalize())
        context = dict(list(context.items()) + list(data_mixing.items()))
        if self.request.user.is_authenticated:
            data_mixing = self.get_user_context(items_in_the_cart=self.request.user.user_id)
            context = dict(list(context.items()) + list(data_mixing.items()))
        return context

    def get_queryset(self):
        return ItemCategory.objects.filter(category_id__slug=self.kwargs['category_slug'])



