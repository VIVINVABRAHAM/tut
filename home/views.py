from ast import Or
from unicodedata import category
from django.shortcuts import render, redirect
from django.shortcuts import render
import pyrebase
from regex import E
from django.contrib import auth, messages
import firebase_admin
from firebase_admin import credentials, firestore
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime
from account.views import authe,db
from django.views.decorators.cache import cache_control

from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


# Create your views here.
def index(request):
    return render(request,'index.html')
def categories(request):
    return render(request,"categories.html")
def about(request):
    return render(request,"about.html")
def faq(request):
    return render(request,"faq.html")
def contact(request):
    return render(request,"contact.html")
def all_product(request):
    return render(request,"all_product.html")
def popular_products(request):
    return render(request,"all_product.html")
def featured_products(request):
    return render(request,"all_product.html")
def guest_query(request):
    name=request.POST.get('name')
    print(name)
    email=request.POST.get('email')
    subjecte = request.POST.get('subject')
    subject = f'{subjecte}'
    message = request.POST.get('message')
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )
    return redirect(index)
def advertise(request):
    return render(request,'advertise.html')

def signup(request):
    return render(request, "ad_signup.html")


def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    role = 'advertiser'
    try:
        user = authe.create_user_with_email_and_password(email, passw)
        uid = user['localId']
        data = {"name":name,"email": email, "passw": passw, "role": role}

        db.collection('advertiser').document(uid).set(data)

    except:
        message = "Email already exists. Try with Different Email"
        return render(request, "ad_signup.html", {"messg": message})


    # data={"name":name,"status":"1"}
    # database.child("users").child(uid).child("details").set(data)

    subject = 'TiT-TaT SignUP'
    message = f'Hi User,\n Thank you for SignUp\nYour Login Credentials:\nUsername : {email}\nPassword : {passw}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return render(request, "ad_signin.html")

def signin(request):

    return render(request, 'ad_signin.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hello(request):
    if request.session.is_empty():
        return redirect(signin)
    # a=request.session['local']
    # a=authe.get_account_info(idtoken)
    # a=a['users']
    # a=a[0]
    # a=a['localId']
    # data= db.collection('user').document(a).get().to_dict()
    # name=data["name"]
    return redirect(myadver)

#@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        message = "invalid credentials"
        return render(request, "ad_signin.html", {"messg": message})
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    request.session['local'] = a
    datas = db.collection('advertiser').document(a).get().to_dict()
    request.session['name'] = datas["name"]
    per_data=db.collection('advertiser').document(a).collection('personal').get()
    for per in per_data:
        perd=per.to_dict()
        request.session['url'] = perd["url"]

    print(request.session['name'])

    return redirect(myadver)
def myadver(request):


    return render(request, 'ad_myads.html')




client = razorpay.Client(auth=("YOUR_ID", "YOUR_SECRET"))

data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" }
payment = client.order.create(data=data)

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def pay_proceed(request):
    value=request.POST.get('plan')
    print(value)
    print(type(value))
    amount = int(value)
    amount=amount*100
    print(type(amount))
    currency = 'INR'
      # Rs. 200
    print(amount)
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
    return render(request,'pay_proceed.html', context=context)


# authorize razorpay client with API Keys.






# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    print("erf")
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
            if result is None:
                amount = 20000  # Rs. 200
                try:

                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)

                    # render success page on successful caputre of payment
                    print("pappppd")
                    return render(request, 'payment_success.html')
                except:

                    # if there is an error while capturing payment.
                    print("fail1")
                    return render(request, 'payment_fail.html')
            else:

                # if signature verification fails.
                print("faileeddddd")
                return render(request, 'payment_fail.html')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

