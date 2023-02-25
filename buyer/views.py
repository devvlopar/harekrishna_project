from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.core.mail import send_mail
from random import randint
from django.conf import settings
from seller.models import *
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
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

def add_to_cart(request):
    try:
        buyer_obj = Buyer.objects.get(email = request.session['email'])
        p_obj = Products.objects.get(id = request.GET['id'])
        Cart.objects.create(
            buyer = buyer_obj,
            product = p_obj
        )
        return JsonResponse({'msg':'Successfully Added!!'})
    except:
        return JsonResponse({'msg':'login nahi kiya hai'})
   
    # try:
    #     Cart.objects.create(
    #         product = Products.objects.get(id = pk),
    #         buyer = buyer_obj
    #     )
    #     return redirect('index')
    # except:
    #     return redirect('login')
    
razorpay_client = razorpay.Client(
auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def cart(request):
    try:
        buyer_obj = Buyer.objects.get(email = request.session['email'])
        cart_data = Cart.objects.filter(buyer = buyer_obj)
        global total_price
        total_price = 0
        for i in cart_data:
            total_price += i.product.price

        #RazorPay Code

        currency = 'INR'
        if total_price == 0:
            total_price = 10
        amount = total_price * 100  # Rs. 200

        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))

        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = 'paymenthandler/'

        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        context['buyer_data'] = buyer_obj
        context['cart_data'] = cart_data
        context['p_count'] = len(cart_data)
        context['total_amount'] = total_price

        return render(request, 'cart.html', context=context)
 

    except:
        return redirect('login')
    






@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = total_price * 100  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    b_obj = Buyer.objects.get(email = request.session['email'])
                    c_list = Cart.objects.filter(buyer = b_obj)
                    
                    for i in c_list:
                        MyOrders.objects.create(
                            buyer = b_obj,
                            product = i.product,
                            status = 1
                        )
                        
                        i.delete()
                    
                    # render success page on successful caputre of payment
                    return render(request, 'success.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'fail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'fail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
    




def del_cart_item(request):
    b_obj = Buyer.objects.get(email = request.session['email'])
    c_row = Cart.objects.get(id = request.GET['c_item'])
    c_row.delete()
    cart_data = Cart.objects.filter(buyer = b_obj)
    final_list = []
    p_count = len(cart_data)

    for s_cart_item in cart_data:
        final_list.append({'id': s_cart_item.id, 
                           'pname' : s_cart_item.product.product_name,
                           'price' : s_cart_item.product.price,
                           'pic': s_cart_item.product.pic.url})

    
    #NIche  no code payment amount update karva mate chhe
    total_price = 0
    for i in cart_data:
        total_price += i.product.price

    #RazorPay Code

    currency = 'INR'
    if total_price == 0:
        total_price = 10
    amount = total_price * 100  # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                    currency=currency,
                                                    payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['total_amount'] = total_price

    context.update({'msg':'Successfully deleted!!', 'cart_data': final_list, 'p_count':p_count})
        
    return JsonResponse(context)