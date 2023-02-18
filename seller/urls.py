from django.urls import path
from .views import *

urlpatterns = [
    path('', seller_index, name='seller_index'),
    path('seller_login/', seller_login, name='seller_login'),
    path('seller_register/', seller_register, name='seller_register'),
    path('seller_logout/', seller_logout, name='seller_logout'),
    path('seller_edit/', seller_edit, name='seller_edit'),
    path('add_product/', add_product, name='add_product'),
    path('my_products/', my_products, name='my_products'),
    path('delete_product/<int:pk>', delete_product, name='delete_product'),
    path('edit_product/<int:pid>', edit_product, name='edit_product'),
    path('dispatched/<int:pk>', dispatched, name='dispatched')








]