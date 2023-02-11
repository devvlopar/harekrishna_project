from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.core.mail import send_mail
from random import randint
from django.conf import settings
from seller.models import *
# Create your views here.

def index(request):
    all_products = Products.objects.all()
    try:
        user_data = Buyer.objects.get(email = request.session['email'])
        return render(request, 'index.html', {'buyer_data': user_data, 'all_products': all_products})
    except:
        return render(request, 'index.html', {'all_products': all_products})


def about(request):
    buyer_obj = Buyer.objects.get(email = request.session['email'])
    return render(request, 'about.html', {'buyer_data': buyer_obj})

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
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        try:
            Buyer.objects.get(email = request.POST['email'])
            return render(request, 'register.html', {'msg':'Email Already Exists!!'})
        except:
            if request.POST['password'] == request.POST['repassword']:
                global user_data
                user_data = [
                    request.POST['first_name'],
                    request.POST['last_name'],
                    request.POST['email'],
                    request.POST['password']
                 ]             
                s = "Registration!!!"
                global c_otp
                c_otp = randint(1000, 9999)
                m = f"Hello User!!\nYour OTP is {c_otp}."
                f = settings.EMAIL_HOST_USER
                r = [request.POST['email']]
                send_mail(s,m,f,r)
                return render(request, 'otp.html', {'msg': 'Check Your MailBox'})
                
            else:
                return render(request, 'register.html', {'msg':'Both Passwords do not Match!!'})


def otp(request): 
    if request.POST['u_otp'] == str(c_otp):
        Buyer.objects.create(
            first_name = user_data[0],
            last_name = user_data[1],
            email = user_data[2],
            password = user_data[3]
        )
        return render(request, 'login.html', {'hj':'account created successfully!!'})
    else:
        return render(request, 'otp.html', {'msg' :'Incorrect OTP!!'})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        try:
            user_obj = Buyer.objects.get(email = request.POST['email'])
            if user_obj.password == request.POST['password']:
                request.session['email'] = request.POST['email'] #login ho gaya/ session chalu ho gaya
                return redirect('index')
            else:
                return render(request, 'login.html', {'hj':'Invalid Password'})
        except:
            return render(request, 'login.html', {'hj':'Email Is Not Registered!!'})


def logout(request):
    del request.session['email']
    return redirect('index')

def faqs(request):
    try:
        buyer_obj = Buyer.objects.get(email = request.session['email'])
        return render(request, 'faqs.html', {'buyer_data': buyer_obj})
    except:
        return render(request, 'faqs.html')

def add_to_cart(request,pk):
    try:
        buyer_obj = Buyer.objects.get(email = request.session['email'])
        Cart.objects.create(
            product = Products.objects.get(id = pk),
            buyer = buyer_obj
        )
        return redirect('index')
    except:
        return redirect('login')
    
def cart(request):
    try:
        buyer_obj = Buyer.objects.get(email = request.session['email'])
        cart_data = Cart.objects.filter(buyer = buyer_obj)
        total_price = 0
        for i in cart_data:
            total_price += i.product.price
        return render(request, 'cart.html', {'buyer_data': buyer_obj, 'cart_data':cart_data, 'p_count': len(cart_data), 'total_amount':total_price})
    except:
        return redirect('login')
    
def delete_cart(request,pk):
    cart_obj = Cart.objects.get(id=pk)
    cart_obj.delete()
    return redirect('cart')