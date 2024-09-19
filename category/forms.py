from django import forms
from category.models import Categories,\
    ItemCategory

class CategoriesForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['name', 'slug', 'img_categories', 'is_published']

class ItemCategoryForm(forms.ModelForm):
    class Meta:
        model = ItemCategory
        fields = ['name', 'slug', 'img_item_category', 'is_published', 'category_id']
