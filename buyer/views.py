from django.shortcuts import render
from django.http import HttpResponse
from .models import Buyer
# Create your views here.

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def checkout(request):
    return render(request, 'checkout.html')

def add_row(request):
    Buyer.objects.create( 
        first_name = 'Ankit',
        last_name = 'Rana',
        email = 'a1121@gmail.com',
        password = 'ankit@123',
        address = '1, society, road, ecity'
    )
    return HttpResponse('row create ho gaya')

def delete_row(request):
    user_obj = Buyer.objects.get(email = 'a1@gmail.com')
    user_obj.delete()
    return HttpResponse('Delete ho gya')


def register(request):
    return render(request, 'register.html')



# CRUD = Create read Update Delete