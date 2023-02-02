from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse

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
        return HttpResponse('Ho gya create')
    
