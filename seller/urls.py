from django.urls import path
from .views import *

urlpatterns = [
    path('seller_index/', seller_index, name='seller_index'),
    path('seller_login/', seller_login, name='seller_login'),
    path('seller_logout/', seller_logout, name='seller_logout'),
    path('seller_edit/', seller_edit, name='seller_edit'),
    path('add_product/', add_product, name='add_product'),





]