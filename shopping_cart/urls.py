from django.urls import path
from .views import ShoppingCart,OrderInformation

urlpatterns = [
    path('', ShoppingCart.as_view(), name='cart'),
    # path('cart_proses',proses,name='aqusations'),
    path('order_process/',OrderInformation.as_view(), name='order_info')
]
# r'^result/(?P[^\/]*)/$'  (?P<pk>\d+)/$'




