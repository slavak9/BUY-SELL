from django.urls import path
from .views import user_area,user_orders, user_mesagges, \
    user_payments,user_sell,UserSalesArea,UserProductEdit, UserProductAdd

urlpatterns = [
    path('', user_area, name='user_personal_area'),
    path('user-orders', user_orders, name='orders'),
    path('user-payments', user_payments, name='payments'),
    path('user-messages',user_mesagges, name='messages'),
    path('user-sales-area', UserSalesArea.as_view(), name='user_sales_area'),
    path('user-sales-area/edit/<slug:edit_product_slag>/', UserProductEdit.as_view(), name='edit_product'),
    path('add_item/',UserProductAdd.as_view(),name='add_item')
]