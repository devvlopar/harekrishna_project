from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('checkout/', checkout, name="checkout"),
    path('add_row/', add_row, name='name_row'),
    path('delete_row/', delete_row, name="delte_row"),
    path('register/', register, name="register"),
    path('otp/', otp, name="otp"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('faqs/', faqs, name="faqs"),
    path('cart/', cart, name="cart"),
    path('add_to_cart/', add_to_cart, name="add_to_cart"),
    path('cart/paymenthandler/', paymenthandler, name='paymenthandler'),
    path('del_cart_item/', del_cart_item, name="del_cart_item")







]