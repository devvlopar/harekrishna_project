from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from random import randint

# Create your views here.
def seller_index(request):
    try:
        seller=Seller.objects.get(email=request.session['seller_email'])
        return render(request, 'seller_index.html',{'seller_data':seller})
    except:
        return render(request, 'seller_login.html')
    


def seller_login(request):
    if request.method == "GET":
        return render(request, 'seller_login.html')
    else:
        try:
            seller_data=Seller.objects.get(email = request.POST['email'])
            if seller_data.password == request.POST['password']:
                request.session['seller_email']=request.POST['email']
                return redirect('seller_index')
            else:
                return render(request,'seller_login.html',{'msg':'Password incorrect'})
        except:
            return render(request,'seller_login.html',{'msg':'Email incorrect'})


def seller_logout(request):
    try:
        del request.session['seller_email']
        return redirect('seller_index')
    except:
        return redirect('seller_login')

def seller_edit(request):
    return render(request, 'seller_edit_profile.html')


def add_product(request):
    if request.method == 'GET':
        sellerdata = Seller.objects.get(email = request.session['seller_email'])
        return render(request, 'add_product.html', {'seller_data':sellerdata})
    else:
        seller_obj = Seller.objects.get(email = request.session['seller_email'])
        Products.objects.create(
            product_name = request.POST['product_name'],
            des = request.POST['des'],
            price = request.POST['price'],
            product_stock = request.POST['product_stock'],
            pic = request.FILES['pic'],
            seller = seller_obj
        )
        return render(request, 'add_product.html', {'seller_data':seller_obj, 'msg': 'Successlly Added!!!'})
    
def my_products(request):
    seller_data = Seller.objects.get(email = request.session['seller_email'])
    seller_products = Products.objects.filter(seller = seller_data)
    return render(request, 'my_products.html', {'seller_data': seller_data, 'seller_products': seller_products })


def delete_product(request,pk):
    kaam_tamaam_prod = Products.objects.get(id= pk)
    kaam_tamaam_prod.delete()
    return redirect('my_products')
    
def edit_product(request, pid):
    s_product = Products.objects.get(id = pid)
    if request.method == 'GET':
        seller_data = Seller.objects.get(email = request.session['seller_email'])
        return render(request, 'edit_product.html', {'product_data': s_product,'seller_data': seller_data})
    else:
        s_product.product_name = request.POST['product_name']
        s_product.price = request.POST['price']
        s_product.des = request.POST['des']
        s_product.product_stock = request.POST['product_stock']
        if request.FILES:
            s_product.pic = request.FILES['pic']
        s_product.save()
        return redirect('my_products')
        
def seller_register(request):
    if request.method == 'GET':
        return render(request, 'seller_register.html')
    else:
        s = "Registration!!!"
        global c_otp
        global files, user_dict
        user_dict = {
            'full_name' : request.POST['full_name'],
            'email' : request.POST['email'],
            'password' : request.POST['password'],
            'gst_no' : request.POST['gst_no']
        }
        c_otp = randint(1000, 9999)
        files = request.FILES['pic']
        print(c_otp)        
        return render(request, 'seller_otp.html')
    

def seller_otp(request):
    Seller.objects.create(
        full_name = user_dict['full_name'] ,
        email = user_dict['email'],
        password = user_dict['password'],
        gst_no = user_dict['gst_no'],
        pic = files
    )
    return render(request, 'seller_register.html')


