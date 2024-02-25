from django.shortcuts import render,redirect  ,get_object_or_404     
from .models import store1,Cart                                                                                         
from django.contrib.auth.models import User                                  
from django.contrib.auth import authenticate,login,logout  
from .forms import *
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm  
    

# Create your views here.
def dashboard(request):  
    object_list=store1.objects.all()   
    
    return render(request,'html/home.html',{'object_list':object_list})  

def product_details(request,id):  
    idd=store1.objects.get(id=id)  
    return render(request,"html/product_details.html",{'i':idd})  


#################

from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from . forms import CreateUser
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
import random
from .models import PreRegistration
from .forms import VerifyForm,LoginForm
from django.contrib.auth import login,logout,authenticate
# Create your views here.

def creatingOTP():
    otp = ""
    for i in range(6):
        otp+= f'{random.randint(0,9)}'
    return otp

def sendEmail(email):
    otp = creatingOTP()
    send_mail(
    'Hello This is a My-Shopping-App project created by jagadeeshgouda Y R',
    f'Your OTP pin is {otp}',
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
    )
    return otp


def createUser(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateUser(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                otp = sendEmail(email)
                dt = PreRegistration(first_name=form.cleaned_data['first_name'],last_name=form.cleaned_data['last_name'],username= form.cleaned_data['username'],email=email,otp=otp,password1 = form.cleaned_data['password1'],password2 = form.cleaned_data['password2'])
                dt.save()
                return HttpResponseRedirect('/verify/')
                
                
        else:
            form = CreateUser()
        return render(request,"newuser.html",{'form':form})
    else:
        return HttpResponseRedirect('/success/')

# def login_function(request):
#     if not request.user.is_authenticated:
#         if request.method == 'POST':
#             form = LoginForm(request=request,data=request.POST)
#             if form.is_valid():
#                 username = form.cleaned_data['username']
#                 password = form.cleaned_data['password']
#                 usr = authenticate(username=username,password = password)
#                 if usr is not None:
#                     login(request,usr)
#                     return HttpResponseRedirect('/success/')
#         else:
#             form = LoginForm()
#         return render(request,'login.html',{'form':form})
#     else:
#         return HttpResponseRedirect('/success/')

def verifyUser(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = VerifyForm(request.POST)
            if form.is_valid():
                otp = form.cleaned_data['otp']
                data = PreRegistration.objects.filter(otp = otp)
                if data:
                    username = ''
                    first_name = ''
                    last_name = ''
                    email = ''
                    password1 = ''
                    for i in data:
                        print(i.username)
                        username = i.username
                        first_name = i.first_name
                        last_name = i.last_name
                        email = i.email
                        password1 = i.password1

                    user = User.objects.create_user(username, email, password1)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    data.delete()
                    messages.success(request,'Account is created successfully!')
                    return HttpResponseRedirect('/login')   
                else:
                    messages.success(request,'Entered OTP is wrong')
                    return HttpResponseRedirect('/verify/')
        else:            
            form = VerifyForm()
        return render(request,'verify.html',{'form':form})
    else:
        return HttpResponseRedirect('/success/')

def success(request):
    if request.user.is_authenticated:
        return render(request,'success.html')
    else:
        return HttpResponseRedirect('/')

def logout_function(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required


def login_form(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            usern = form.cleaned_data['username']
            userp = form.cleaned_data['password']
            user = authenticate(username= usern, password=userp)

            if user is not None:
                login(request, user)
                return redirect('/home')

    else:
        form = AuthenticationForm()
    context= {'form':form}
    return render(request, 'login.html', context)



#logout
@login_required(login_url='/')
def logout_form(request):
    logout(request)
    #return redirect('/login')
    return render(request, 'logout.html')

@login_required(login_url='login')
def changepassword(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)

            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('/login')
            else:
                return HttpResponse("password is not matching")
        else:
            form = PasswordChangeForm(user= request.user)
            context = {'form':form}
            return render(request, 'changepassword.html',context)
    else:
        return redirect('/changepassword')

##########33# 

from django.views.generic import ListView    
from django.db.models import Q  

class SearchResultsView(ListView):  
    model=store1     
    template_name="html/search_results.html"   
    def get_queryset(self):
        query=self.request.GET.get('q')  
        object_list=store1.objects.filter(Q(name__icontains=query) |   Q(description__icontains=query))  
        return object_list       
    def get(self,request,*args,**kwargs):  
        query=self.request.GET.get('q')   
        object_list=self.get_queryset()  
        
        if not object_list:   
            return render(request,"html/not_found.html",{'i':query})     
        return super().get(request,*args,**kwargs)   
    
from django.contrib.auth.decorators import login_required    
@login_required      
def add_to_cart(request):  
    if request.method == 'POST':  
        product_id = request.POST.get('product_id')    
        print(product_id)   
        product=get_object_or_404(store1,id=product_id)  
        cart, created=Cart.objects.get_or_create(user=request.user,product_name=product) 
        cart.quantity +=1   
        cart.totalprice=cart.quantity*product.price                                                   
        cart.save()         
    return redirect('/cart')  
def increment_cart(request,cart_id):    
    cart=get_object_or_404(Cart, id=cart_id ,user=request.user)        
    cart.quantity  +=1    
    cart.totalprice=cart.quantity*cart.product_name.price                        
    cart.save()  
    return redirect('/cart')   

def decrement_cart(request,cart_id):  
    cart=get_object_or_404(Cart,id=cart_id,user=request.user)    
    if cart.quantity>1:       
        cart.quantity-=1    
        cart.totalprice=cart.quantity*cart.product_name.price                    
        cart.save()      
    return redirect('/cart')
def cart(request):  
    cart_items=Cart.objects.filter(user=request.user)  
    total_price=sum(item.totalprice for item in cart_items)  
    return render(request,'html/cart.html',{'cart_items':cart_items,'total_price':total_price})  
def remove_from_cart(request,cart_id):  
    cart=get_object_or_404(Cart,id=cart_id,user=request.user)        
    cart.delete()  
    return redirect("/cart")  


from django.urls import reverse   
from django.http import HttpResponse     
from django.views.decorators.csrf import csrf_exempt    

from .forms import ShippingAddressForm           
from .models import Order,Cart                                   

  
from django.urls import reverse   
from django.http import HttpResponse     
from django.views.decorators.csrf import csrf_exempt    
from paypalrestsdk import Payment 
from .forms import ShippingAddressForm           
from .models import *                                  

@csrf_exempt   
def execute_payment(request):  
    payment_id=request.GET.get('paymentId')  
    payer_id=request.GET.get('payerID')  
    payment=Payment.find(payment_id) 
    if payment.execute({"payer_id":payer_id}):   
        return render(request,'order_success.html') 
    else:  
        return HttpResponse('Error in executing payment')  
    
def cancel_payment(request):  
    return render(request,'payment_cancel.html') 

# def checkout(request):  
    if request.method=='POST': 
        shipping_address_form=ShippingAddressForm(request.POST)  
        if shipping_address_form.is_valid():  
            shipping_address=shipping_address_form.save(commit=False)  
            shipping_address.user=request.user    
            shipping_address.save() 
            order=Order(user=request.user,shipping_address=shipping_address)  
            cart_items=Cart.objects.filter(user=request.user,order__isnull=True)          
            order.total_price=sum(cart_item.totalprice for cart_item in cart_items)      
            order.save()   
            for cart_item in cart_items:   
                cart_item.order=order  
                cart_item.save()   
                
            order.total_price=sum(cart_item.totalprice for cart_item in cart_items)                           
            order.save() 
            # payment_data={ 
            #               "intent":"sale",
            #               "payer":{
            #                 "payment_method":"paypal",  
            #               } , 
            #               "redirect_urls":{ 
            #                   "return_url":request.build_absolute_uri(reverse('execute_payment')),
            #                   "cancel_url":request.build_absolute_uri(reverse('cancel_payment')), 
            #                   },  
            #               "transactions":[{
            #                   "item_list":{ 
            #                       "items":[{ 
            #                           "name": item.product_name.name,      
            #                           "sku":"item",    
            #                           "price":str(item.product_name.price), 
            #                           "currency":"USD",     
            #                           "quantity":item.quantity, 
            #                   }for item in cart_items   ],  
            #                   },    
            #                   "amount":{
            #                       "total":str(order.total_price),  
            #                       "currency":"USD",    
            #                   },  
            #                   "description":"Order payment"
            #                 }],  
                          
            # }    
            payment=Payment(payment_data)  
            if payment.create():  
                order.payment_id=payment.id    
                order.save()    
                return_url=[link.href for link in payment.link if link.method== "REDIRECT"][0]                 
                return redirect(return_url)    
            else:    
                return HttpResponse(f'Error in creating payment:{payment.error}')    
            
    else:     
        shipping_address_form=ShippingAddressForm()  
        
    return render(request,'html/checkout.html',{'shipping_address_form':shipping_address_form})     
def checkout(request):  
    if request.method=='POST': 
        shipping_address_form=ShippingAddressForm(request.POST)  
        if shipping_address_form.is_valid():  
            shipping_address=shipping_address_form.save(commit=False)  
            shipping_address.user=request.user    
            shipping_address.save() 
            order=Order(user=request.user,shipping_address=shipping_address)  
            cart_items=Cart.objects.filter(user=request.user,order__isnull=True)          
            order.total_price=sum(cart_item.totalprice for cart_item in cart_items)      
            order.save()   
            for cart_item in cart_items:   
                cart_item.order=order  
                cart_item.save()   
                
            order.total_price=sum(cart_item.totalprice for cart_item in cart_items)                           
            order.save() 
            return redirect("index")
    
        
    return render(request,'html/checkout.html',{'shipping_address_form':shipping_address_form})     


# payment page

from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


import razorpay

razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def homepage(request):
    # Retrieve the latest car rental or adjust your logic based on your requirements
    latest_order = Order.objects.latest('id')  # Assuming you have a 'pickup_date' field in CarRental

    currency = 'INR'
    
    price=latest_order.total_price
    amount = int(price * 100)

    razorpay_order = razorpay_client.order.create(dict(
        amount=amount,
        currency=currency,
        payment_capture='0'
    ))


    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount':amount,
        'currency': currency,
        'callback_url': callback_url
    }

    return render(request, 'index.html', context=context)

# The rest of your payment handling view remains unchanged

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                try:
                    # Get the car rental associated with the Razorpay order
                    amount = Order.objects.get(pk=razorpay_order_id)

                    # Use the get_total property to calculate the expected amount
                    amount = Order.total_price()

                    razorpay_client.payment.capture(payment_id, amount)
                    return render(request, 'paymentsuccess.html')
                except Order.DoesNotExist:
                    return render(request, 'paymentfail.html')
            else:
                return render(request, 'paymentfail.html')
        except Exception as e:
            print(e)
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()
