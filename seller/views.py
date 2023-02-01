from django.shortcuts import render, redirect
from .models import Seller

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