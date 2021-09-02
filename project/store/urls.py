from django.urls import path,include
from . import views 

app_name='store'

urlpatterns=[
    path('', views.home, name = 'home'),
    path('for/<str:text>/<str:product>/', views.productlist, name = 'productlist'),
    path('for/<str:text>/', views.category, name = 'categories'),
    path('increase/<item_id>/', views.incquantity, name = 'incquantity'),
    path('decrease/<item_id>/', views.decquantity, name = 'decquantity'),
    path('product/<id>/', views.productdetail, name = 'productdetail'),
    path('order/<id>', views.orderdetail, name = 'orderdetail'),
    path('cancelorder/<orderid>/', views.cancelorder, name = 'cancelorder'),
    path('deleteaddress/<addressid>/', views.deleteaddress, name = 'deleteaddress'),
    path('addToCart/<ID>/<size>/', views.addtocart, name = 'addtocart'),
    path('deleteFromCart/<id>/', views.deletefromcart, name = 'deletefromcart'),
    path('yourCart/', views.yourcart, name = 'yourcart'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('addaddress/', views.add_address, name = 'addaddress'),
    path('orders/', views.orderlist, name = 'orderlist'),
    path('addresses/', views.addresslist, name = 'addresslist'),
]