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
from django.views.decorators.cache import cache_control

from requests import request


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

config = {

    "apiKey": "AIzaSyBHarVpnSGSt5UrG_k8KXd9KuBlIYK3vwU",
    "authDomain": "tita-1a2a0.firebaseapp.com",
    "databaseURL": "https://tita-1a2a0-default-rtdb.firebaseio.com",
    "projectId": "tita-1a2a0",
    "storageBucket": "tita-1a2a0.appspot.com",
    "messagingSenderId": "875507388348",
    "appId": "1:875507388348:web:762f3437dceabda94025b9",
    "measurementId": "G-6GTETXK7QR"

}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

db = firestore.client()

# Create your views here.


def signin(request):

    return render(request, 'signin.html')

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
    return redirect(cus_home)

#@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        message = "invalid credentials"
        return render(request, "signin.html", {"messg": message})
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    request.session['local'] = a
    datas = db.collection('user').document(a).get().to_dict()
    request.session['name'] = datas["name"]
    per_data=db.collection('user').document(a).collection('personal').get()
    for per in per_data:
        perd=per.to_dict()
        request.session['url'] = perd["url"]

    print(request.session['name'])
    if datas["role"] == "Evaluator":

        return redirect(evaluator_dash)
    else:
        return redirect(hello)
   # name= database.child('users').child(a).child('details').child('name').get(idtoken).val()


def evaluator_dash(request):
     if request.session.is_empty():
        return redirect(signin)

     a = request.session['local']

     datas = db.collection('user').document(a).get().to_dict()
     list = []
     perlist = []
     data = db.collection('user').where('role', '==', 'user').get()
     for dat in data:
        key = dat.id
        # print(key)
        data_pro = db.collection('user').document(
            key).collection('products').get()

        for pro in data_pro:
            prodict = pro.to_dict()
            prodict["productid"] = pro.id
            prodict['userid'] = key
            list.append(prodict)
        data_per = db.collection('user').document(
            key).collection('personal').get()
        for per in data_per:
            perdict = per.to_dict()
            perdict['personid'] = per.id
            perlist.append(perdict)
        name = datas["name"]
        # print(list)
     return render(request, "evaluator_dash.html", {"nam": name, "prd": list, "per": perlist})

def evaluated_products(request):
    if request.session.is_empty():
        return redirect(signin)

    a = request.session['local']

    datas = db.collection('user').document(a).get().to_dict()
    list = []
    perlist = []
    data = db.collection('user').where('role', '==', 'user').get()
    for dat in data:
        key = dat.id
        # print(key)
        data_pro = db.collection('user').document(
            key).collection('products').get()

        for pro in data_pro:
            prodict = pro.to_dict()
            prodict["productid"] = pro.id
            prodict['userid'] = key
            list.append(prodict)
        data_per = db.collection('user').document(
            key).collection('personal').get()
        for per in data_per:
            perdict = per.to_dict()
            perdict['personid'] = per.id
            perlist.append(perdict)
        name = datas["name"]
        # print(list)

    return render(request,'evaluated_products.html', {"nam": name, "prd": list, "per": perlist})
def Inactive_products(request):
    if request.session.is_empty():
        return redirect(signin)

    a = request.session['local']

    datas = db.collection('user').document(a).get().to_dict()
    list = []
    perlist = []
    data = db.collection('user').where('role', '==', 'user').get()
    for dat in data:
        key = dat.id
        # print(key)
        data_pro = db.collection('user').document(
            key).collection('products').get()

        for pro in data_pro:
            prodict = pro.to_dict()
            prodict["productid"] = pro.id
            prodict['userid'] = key
            list.append(prodict)
        data_per = db.collection('user').document(
            key).collection('personal').get()
        for per in data_per:
            perdict = per.to_dict()
            perdict['personid'] = per.id
            perlist.append(perdict)
        name = datas["name"]
        # print(list)

    return render(request,'Inactive_products.html', {"nam": name, "prd": list, "per": perlist})
def solded_products(request):
    if request.session.is_empty():
        return redirect(signin)

    a = request.session['local']

    datas = db.collection('user').document(a).get().to_dict()
    list = []
    perlist = []
    data = db.collection('user').where('role', '==', 'user').get()
    for dat in data:
        key = dat.id
        # print(key)
        data_pro = db.collection('user').document(
            key).collection('products').get()

        for pro in data_pro:
            prodict = pro.to_dict()
            prodict["productid"] = pro.id
            prodict['userid'] = key
            list.append(prodict)
        data_per = db.collection('user').document(
            key).collection('personal').get()
        for per in data_per:
            perdict = per.to_dict()
            perdict['personid'] = per.id
            perlist.append(perdict)
        name = datas["name"]
        # print(list)

    return render(request,'solded_products.html', {"nam": name, "prd": list, "per": perlist})

def ev_active_products(request):
    if request.session.is_empty():
        return redirect(signin)

    a = request.session['local']

    datas = db.collection('user').document(a).get().to_dict()
    list = []
    perlist = []
    data = db.collection('user').where('role', '==', 'user').get()
    for dat in data:
        key = dat.id
        # print(key)
        data_pro = db.collection('user').document(
            key).collection('products').get()

        for pro in data_pro:
            prodict = pro.to_dict()
            prodict["productid"] = pro.id
            prodict['userid'] = key
            list.append(prodict)
        data_per = db.collection('user').document(
            key).collection('personal').get()
        for per in data_per:
            perdict = per.to_dict()
            perdict['personid'] = per.id
            perlist.append(perdict)
        name = datas["name"]
        # print(list)

    return render(request,'ev_active_products.html', {"nam": name, "prd": list, "per": perlist})
def rejected_products(request):
    if request.session.is_empty():
        return redirect(signin)

    a = request.session['local']

    datas = db.collection('user').document(a).get().to_dict()
    list = []
    perlist = []
    data = db.collection('user').where('role', '==', 'user').get()
    for dat in data:
        key = dat.id
        # print(key)
        data_pro = db.collection('user').document(
            key).collection('products').get()

        for pro in data_pro:
            prodict = pro.to_dict()
            prodict["productid"] = pro.id
            prodict['userid'] = key
            list.append(prodict)
        data_per = db.collection('user').document(
            key).collection('personal').get()
        for per in data_per:
            perdict = per.to_dict()
            perdict['personid'] = per.id
            perlist.append(perdict)
        name = datas["name"]
        # print(list)

    return render(request,'rejected_products.html', {"nam": name, "prd": list, "per": perlist})


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def logout(request):
#     if request.session.is_empty():
#         return redirect(signin)

#     auth.logout(request)
#     request.session.flush()
#     return render(request, 'signin.html')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    if request.session.is_empty():
        return redirect(signin)
    else:
        auth.logout(request)
        request.session.flush()
        return redirect('index')


def signup(request):
    return render(request, "signup.html")


def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    role = 'user'
    try:
        user = authe.create_user_with_email_and_password(email, passw)
        uid = user['localId']
        data = {"name":name,"email": email, "passw": passw, "role": role}

        db.collection('user').document(uid).set(data)

    except:
        message = "Email already exists. Try with Different Email"
        return render(request, "signup.html", {"messg": message})


    # data={"name":name,"status":"1"}
    # database.child("users").child(uid).child("details").set(data)

    subject = 'TiT-TaT SignUP'
    message = f'Hi User,\n Thank you for SignUp\nYour Login Credentials:\nUsername : {email}\nPassword : {passw}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return render(request, "signin.html")


def cus_home(request):
    if request.session.is_empty():
        return redirect(signin)
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    data = db.collection('user').document(a).get().to_dict()
    name = data["name"]

    datas = db.collection('user').document(a).get().to_dict()
    list = []
    perlist = []
    datalist=[]
    data = db.collection('user').where('role', '==', 'user').get()
    for dat in data:
        key = dat.id
        #print(key)
        data_per = db.collection('user').document(
            key).collection('personal').get()
        for per in data_per:
            perdict = per.to_dict()
            perdict['personid'] = per.id
            p = perdict['date']
            da = {'dal': p.date()}
            ab = p.date()
            perdict.update(da)
            #print(perdict)

            data_pro = db.collection('user').document(
                key).collection('products').where('status','==', 2).limit(12).get()

            for pro in data_pro:
                prodict = pro.to_dict()
                prodict["productid"] = pro.id
                prodict['userid'] = key
                res = perdict | prodict
                list.append(res)

            datalistcreation = db.collection('user').document(
                key).collection('products').where('status','==', 2).get()
            for pro in datalistcreation:
                prodict = pro.to_dict()
                datalist.append(prodict["title"])

    #     print(prodict)
    #print(list)
    #print(len(list))
            # list.append(prodict)
    print(datalist)
    return render(request, "cus_home.html", {"prd": list,'datalist':datalist})


def postadd(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    data = db.collection('user').document(a).get().to_dict()
    name = data["name"]

    if(db.collection('user').document(a).collection('personal').get()):
        return render(request, "categories_f.html", {"nam": name})
    else:
        data = db.collection('user').document(a).get().to_dict()
        name = data["name"]
        return render(request, "postadd.html", {"nam": name})


def categories_f(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    data = db.collection('user').document(a).get().to_dict()
    name = data["name"]

    return render(request, 'categories_f.html', {'nam': name, })

    # HG=request.POST.get('HG')
    # PA=request.POST.get('PA')
    # CA=request.POST.get('CA')
    # Electronics=request.POST.get('Electronics')
    # Vehicles=request.POST.get('Vehicles')
    # SG=request.POST.get('SG')
    # Rare=request.POST.get('Rare')
    # if(JA!={}):
    #     return render(request,"addpost_jewel.html",{"J":JA})
    # if(HG!={}):
    #     return render(request,"addpostfirst.html",{"H":HG})
    # if(PA!={}):
    #     return render(request,"addpostfirst.html",{"P":PA})
    # if(CA!={}):
    #     return render(request,"addpostfirst.html",{"C":CA})
    # if(Electronics!={}):
    #     render(request,"addpostfirst.html",{"EL":Electronics})
    # if(Vehicles!={}):
    #     render(request,"addpostfirst.html",{"Vl":Vehicles})
    # if(SG!={}):
    #     render(request,"addpostfirst.html",{"S":SG})
    # if(Rare!={}):
    #    render(request,"addpostfirst.html",{"Re":Rare})


# def addpost_jewel(request,jw):
#     a=request.session['local']
#     personal=db.collection('user').document(a).collection('personal').get()
#     person=personal[0].id
#     personals=db.collection('user').document(a).collection('personal').document(person).get().to_dict()
#     data= db.collection('user').document(a).get().to_dict()
#     name=data["name"]

#     return render(request,'addpost_jewel.html',{'per':personals,'nam':name,"j":jw})
def addpost(request, fr):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    personal = db.collection('user').document(a).collection('personal').get()
    person = personal[0].id
    personals = db.collection('user').document(a).collection(
        'personal').document(person).get().to_dict()
    data = db.collection('user').document(a).get().to_dict()
    name = data["name"]

    return render(request, 'addpost.html', {'per': personals, "nam": name, "f": fr})


def addpostfirst(request):
        a = request.session['local']
        personal = db.collection('user').document(
            a).collection('personal').get()
        person = personal[0].id
        personals = db.collection('user').document(a).collection(
            'personal').document(person).get().to_dict()
        data = db.collection('user').document(a).get().to_dict()
        name = data["name"]

        return render(request, 'addpost.html', {'per': personals, 'nam': name})


def postdetail(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    first = request.POST.get('first')
    last = request.POST.get('last')
    phone = request.POST.get('phone')
    ad1 = request.POST.get('ad1')
    ad2 = request.POST.get('ad2')

    state = request.POST.get('state')
    district = request.POST.get('district')
    taluk = request.POST.get('taluk')
    url = request.POST.get('url')
    today = datetime.now()

   # print(taluk)
    # print(url)
    try:
        a = request.session['local']
       # print(a)
        # print("info",str(a))
        data = {
            "first": first,
            "last": last,
            "phone": phone,
            "ad1": ad1,
            "ad2": ad2,

            "state": state,
            "district": district,
            "taluk": taluk,
            "url": url,
            "date": today


        }


        db.collection('user').document(a).collection('personal').add(data)

        # print("a",personal)

        # print(person)

        # name= database.child('users').child(a).child('details').child('name').get(idtoken).val()
        # # return render(request,'addpost.html',{'nam':name})
        # first=database.child('users').child(a).child('personal').child('first').get().val()
        # last=database.child('users').child(a).child('personal').child('last').get().val()
        # phone=database.child('users').child(a).child('personal').child('phone').get().val()
        # ad1=database.child('users').child(a).child('personal').child('ad1').get().val()
        # ad2=database.child('users').child(a).child('personal').child('ad2').get().val()
        # state=database.child('users').child(a).child('personal').child('state').get().val()
        # district=database.child('users').child(a).child('personal').child('district').get().val()
        # taluk=database.child('users').child(a).child('personal').child('taluk').get().val()
        # img_url=database.child('users').child(a).child('personal').child('url').get().val()
        # name= database.child('users').child(a).child('details').child('name').get(idtoken).val()

     # print(timestamps)
        return redirect(categories_f)

    except KeyError:
        message = "Oops! User logged out please sign in again"
        return render(request, "signin.html", {"mess": message})

# def addpost(request,id):
#     print(id)
#     import datetime
#     idtoken=request.session['uid']
#     a=authe.get_account_info(idtoken)
#     a=a['users']
#     a=a[0]
#     a=a['localId']

#     # timestamps=database.child('users').child(a).child('personal').child(id).shallow().get().val()
#     # lis_time=[]
#     # for i in timestamps:
#     #     lis_time.append(i)
#     # lis_time.sort(reverse=True)
#     # print(lis_time)


def myads(request):
    if request.session.is_empty():
        return redirect(signin)

    # idtoken=request.session['uid']
    # a=authe.get_account_info(idtoken)
    # a=a['users']
    # a=a[0]
    # a=a['localId']
    a = request.session['local']

    names = db.collection('user').document(a).get().to_dict()
    name = names['name']

    # dic =  db.collection('user').document(a).collection('products').get()

    # plist=[]
    # for i in productdata:
    #     plist.append(i.val())
    # print(plist)
    # dic = dict(zip(lis_time, plist)
    # print(dic)
    productlist = []
    pro = db.collection('user').document(a).collection('products').where('status','<=',5).get()
    for p in pro:
     prodict = p.to_dict()
     prodict["productid"] = p.id
     productlist.append(prodict)
    print(len(productlist))
    return render(request, 'myads.html', {"prd": productlist, "nam": name})

    # title=database.child('users').child(a).child('product').child(i).child('title').get().val()

    # name= database.child('users').child(a).child('details').child('name').get(idtoken).val()
    # return render(request,'myads.html',{'nam':name,'tit':title})


def post_pro(request):
    if request.session.is_empty():
        return redirect(signin)

    a = request.session['local']

    title = request.POST.get('title')
    brand = request.POST.get('brand')
    material = request.POST.get('material')
    category = request.POST.get('category')
    scratch = request.POST.get('scratch')
    weight = request.POST.get('weight')
    condition = request.POST.get('condition')
    type = request.POST.get('type')
    color = request.POST.get('color')
    stones = request.POST.get('stones')
    buy_price = request.POST.get('buy_price')
    Design_works = request.POST.get('Design_works')
    model = request.POST.get('model')
    yom = request.POST.get('yom')
    cu_price = request.POST.get('cu_price')
    adpost = request.POST.get('adpost')

    url = request.POST.get('url')
    url1 = request.POST.get('url1')
    url2 = request.POST.get('url2')
    url3 = request.POST.get('url3')
    demtitle = request.POST.get('demtitle')
    dembrand = request.POST.get('dembrand')
    demcategory = request.POST.get('demcategory')
    demcolor = request.POST.get('demcolor')
    demyom = request.POST.get('demyom')
    today = datetime.now()
    tok = today

    try:
        a = request.session['local']

        data = {
            "title": title,
            "brand": brand,
            "material": material,
            "category": category,
            "scratch": scratch,
            "weight": weight,
            "condition": condition,
            "type": type,
            "color": color,
            "stones": stones,
            "Design_works": Design_works,
            "model": model,
            "buy_price": buy_price,
            "yom": yom,
            "cu_price": cu_price,
            "adpost": adpost,
            "url": url,
            "url1": url1,
            "url2": url2,
            "url3": url3,
            "demtitle": demtitle,
            "dembrand": dembrand,
            "demcategory": demcategory,
            "demcolor": demcolor,
            "demyom": demyom,
            "status": 0,
            "date": today,
            "toda": tok


        }
        product = db.collection('user').document(
            a).collection('products').add(data)
        return redirect(addpost_pic,product[1].id,category)

    except KeyError:
        message = "Oops! User logged out please sign in again"
        return render(request, "signin.html", {"mess": message})
    return redirect(myads)


#         database.child('users').child(a).child('product').child(millis).set(data,idtoken)
#         plist=[]
#         productdata =  database.child('users').child(a).child('product').get(idtoken)

#         for i in productdata:

#             plist.append(i.val())
#         print(plist)

#         name= database.child('users').child(a).child('details').child('name').get(idtoken).val()
#         title=database.child('users').child(a).child('product').child(millis).child('title').get(idtoken).val()
#         category=database.child('users').child(a).child('product').child(millis).child('category').get(idtoken).val()
#         mili=database.child('users').child(a).child('product').child(millis).get(idtoken).key()
#         milil=database.child('users').child(a).child('product').child(millis).get(idtoken).key()
#         year=database.child('users').child(a).child('product').child(millis).child('yom').get(idtoken).val()
#         clr=database.child('users').child(a).child('product').child(millis).child('color').get(idtoken).val()
#         img_url=database.child('users').child(a).child('product').child(millis).child('url').get(idtoken).val()
#         pri=database.child('users').child(a).child('product').child(millis).child('cu_price').get(idtoken).val()
#         productdata =  database.child('users').child(a).child('product').get(idtoken).val()

#         return redirect(myads)
#

# def test(request):
#     idtoken=request.session['uid']
#     a=authe.get_account_info(idtoken)
#     a=a['users']
#     a=a[0]
#     a=a['localId']
#     plist=[]
#     productdata =  database.child('users').child(a).child('product').get(idtoken)

#     for i in productdata:
#         plist.append(i.val())
#     print(plist)

def addpost_pic(request,pr,fr):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    personal = db.collection('user').document(a).collection('personal').get()
    person = personal[0].id
    personals = db.collection('user').document(a).collection(
        'personal').document(person).get().to_dict()
    data = db.collection('user').document(a).get().to_dict()
    name = data["name"]
    print(pr)
    tit=db.collection('user').document(a).collection('products').document(pr).get().to_dict()
    print("fvkjd")
    return render(request,'addpost_pic.html', {'per': personals, "nam": name, "f": fr,"p":pr,"t":tit})
def pics_add(request):
    a = request.session['local']
    if request.method=="POST":
        url = request.POST.get('url')
        url1 = request.POST.get('url1')
        url2 = request.POST.get('url2')
        url3 = request.POST.get('url3')
        p=request.POST.get('p')
        data={ "url": url,
            "url1": url1,
            "url2": url2,
            "url3": url3,
            }
        db.collection('user').document(a).collection('products').document(p).update(data)
        return redirect(pro_com,p)

    #return render(request,'dem_pro.html', {'per': personals, "nam": name, "f": fr})
def pro_com(request,p):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    personal = db.collection('user').document(a).collection('personal').get()
    person = personal[0].id
    personals = db.collection('user').document(a).collection(
        'personal').document(person).get().to_dict()
    data = db.collection('user').document(a).get().to_dict()
    name = data["name"]

    return render(request,'dem_pro.html', {'per': personals, "nam": name,'p':p})

def dem_pro(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    if request.method=="POST":
        demtitle = request.POST.get('demtitle')
        dembrand = request.POST.get('dembrand')
        demcategory = request.POST.get('demcategory')
        demcolor = request.POST.get('demcolor')
        demyom = request.POST.get('demyom')
        p=request.POST.get('p')
        data={
             "demtitle": demtitle,
            "dembrand": dembrand,
            "demcategory": demcategory,
            "demcolor": demcolor,
            "demyom": demyom,}
        db.collection('user').document(a).collection('products').document(p).update(data)
        return redirect(cus_home)


def profilesettings(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    names = db.collection('user').document(a).get().to_dict()
    name = names['name']
    email=names['email']
    pers=[]
    personal = db.collection('user').document(a).collection('personal').get()
    for pp in personal:
        person=pp.to_dict()
        person['personid']=pp.id
        pers.append(person)
    print(pers)
    personals = db.collection('user').document(a).collection('personal').document(pp.id).get().to_dict()
    context={"nam": name,"per":personals,"mail":email}

    return render(request, 'profile-settings.html', context)

def updateprofile(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    names = db.collection('user').document(a).get().to_dict()
    name = names['name']
    email=names['email']
    pers=[]
    personal = db.collection('user').document(a).collection('personal').get()
    for pp in personal:
        person=pp.to_dict()
        person['personid']=pp.id
        pers.append(person)
    print(pers)
    personals = db.collection('user').document(a).collection('personal').document(pp.id).get().to_dict()
    personals['personid']=pp.id


    context={"nam": name,"per":personals,"mail":email}


    return render(request,'updateprofile.html',context)


def dataup(request):
    if request.session.is_empty():
        return redirect(signin)
    a=request.session['local']
    perid=request.POST.get('perid')
    print(perid)
    first = request.POST.get('first')
    last = request.POST.get('last')
    phone = request.POST.get('phone')
    ad1 = request.POST.get('ad1')
    ad2 = request.POST.get('ad2')

    state = request.POST.get('state')
    district = request.POST.get('district')
    taluk = request.POST.get('taluk')
    url = request.POST.get('url')
    today = datetime.now()
    data = {
            "first": first,
            "last": last,
            "phone": phone,
            "ad1": ad1,
            "ad2": ad2,


            "district": district,
            "taluk": taluk,

            "date": today


        }


    dss=db.collection('user').document(a).collection('personal').document(perid)

    dss.update(data)


    return redirect(cus_home)



def productdetails(request, key):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    plist = []
    print(a)
    productdata = db.collection('user').document(
        a).collection('products').document(key).get().to_dict()
    names = db.collection('user').document(a).get().to_dict()
    name = names['name']
    return render(request, 'product-details.html', {"k": productdata, "nam": name})


def eval_pro_details(request, pid, uid):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']

    data = db.collection('user').document(uid).collection('products').document(pid).get().to_dict()
    persons = db.collection('user').document(uid).collection('personal').get()
    names = db.collection('user').document(a).get().to_dict()
    name = names['name']
    pdict = {}
    for pp in persons:
        pdict = pp.to_dict()
        pdict["productid"] = pid
        pdict["userid"] = uid

    return render(request, 'eval_pro_details.html', {'k': data, "per": pdict, 'nam': name})


def evaluation(request, pid, uid):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    data = db.collection('user').document(uid).collection(
        'products').document(pid).get().to_dict()
    persons = db.collection('user').document(uid).collection('personal').get()
    pdict = {}
    names = db.collection('user').document(a).get().to_dict()
    name = names['name']
    for pp in persons:
        pdict = pp.to_dict()
        pdict["productid"] = pid
        pdict["userid"] = uid
    names = db.collection('user').document(uid).get().to_dict()
    return render(request, 'evaluation.html', {'k': data, 'per': pdict, 'nam': name, 'userid': uid})


def evaluating(request):
    if request.session.is_empty():
        return redirect(signin)

    a = request.session['local']
    userid = request.POST.get('userid')
    pid = request.POST.get('pid')
    Category = request.POST.get('Category')
    Product = request.POST.get('Product')
    Processor = request.POST.get('Processor Used')
    Scratch = request.POST.get('Scratch and Dents if any')
    Weight = request.POST.get('Net Weight in grams')
    Condition = request.POST.get('Current Condition')
    Stones = request.POST.get('Stones')
    Material = request.POST.get('Material Used')
    Design = request.POST.get('Design Verified')
    Brand= request.POST.get('Brand')
    Model= request.POST.get('Model')
    Type = request.POST.get('User Type')
    Color = request.POST.get('Color')
    Year = request.POST.get('Year of Manufacture')

    buy_price = request.POST.get('Buy time price')
    Demanded  = request.POST.get('Demanded price')
    details = request.POST.get('details')
    #details = request.POST.get('details')
    list = []
    list.append(Category)
    list.append(Product)
    list.append(Processor)
    list.append(Scratch)
    list.append(Weight)
    list.append(Condition)
    list.append(Stones)
    list.append(Material)
    list.append(Design)

    list.append(Brand)
    list.append(Model)
    list.append(Type)
    list.append(Color)
    list.append(Year)
    list.append(buy_price)
    list.append(Demanded)
    print(list)
    em_data = db.collection('user').document(userid).get().to_dict()
    email = em_data['email']
    # print(email)
    name = em_data['name']
    if 'No' in list:
        # print("not verified")
        subject = 'TiT-TaT Update Product'
        message = f'Hi {name}, kindly please update the product based on the rules.\nTiT-TaT Rules\n Per year deprecision - 2% \nPer popular to non popular brand deprecision- 2% to 16%\nPer dents small to large deprecision - 1% to 5%\nPer scratch small to large deprecision - 1% to 5%\nPer second user to fifth user deprecision - 2% to 10%\nPer working mild to poor condition deprecision - 10% to 30%\n Please update the details based on below instruction\n ,{details}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)
        db.collection('user').document(userid).collection(
            'products').document(pid).update({'status': 4})
        return redirect(evaluator_dash)
    else:
        subject = 'TiT-TaT Product Verified'
        message = f'Hi {name}, {details}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)
        db.collection('user').document(userid).collection(
            'products').document(pid).update({'status': 1})
        return redirect(evaluator_dash)


def forgotpage(request):

    return render(request, 'forgot.html')


def forgot(request):

    emails = request.POST.get('email')
    print(emails)
    list = []
    password = ""
    name = ""

    forg = db.collection('user').where('email', '==', emails).get()
    for fo in forg:
        usedict = fo.to_dict()
        usedict['userid'] = fo.id
        password = usedict['passw']
        name = usedict['name']
        print(password)
    subject = 'TiT-TaT Account Recover Password'
    message = f'Hi {name}, Your Account password is {password}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [emails]
    send_mail(subject, message, email_from, recipient_list)

        # dataas=db.collection('user').document(fo.id).get().to_dict()
        # mail=dataas['email']
        # print(mail)
        # if mail == emails:
        #     print("sucess")
        #     mail=dataas['email']
        #     name=dataas['name']
        #     passw=dataas['passw']
        #     print(mail)
        #     print(name)
        #     print(passw)

        # else:
        #     print("not")

    return redirect(signin)


def product_history(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    names = db.collection('user').document(a).get().to_dict()
    name = names['name']
    return render(request, 'product-history.html', {"nam": name})


def date_show(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    names = db.collection('user').document(a).get().to_dict()
    name = names['name']

    print(name)

    date = request.POST.get('date')
    print(type(date))
    date = datetime.strptime(date, '%Y-%m-%d').date()
    list = []
    print(date)
    datas = db.collection('user').document(a).collection('products').get()
    for da in datas:
        data = da.to_dict()
        dat = data['date']
        data["productid"] = da.id
        only_date = dat.date()
        print(only_date)
        if only_date >= date:
            list.append(data)
    print(list)
    return render(request, 'product-history.html', {"prd": list, "dat": date, "nam": name})


def product_history_bn(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    names = db.collection('user').document(a).get().to_dict()
    name = names['name']
    return render(request, 'product-history_bn.html', {"nam": name})


def date_shows(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    names = db.collection('user').document(a).get().to_dict()
    name = names['name']
    print(name)
    print(name)

    date = request.POST.get('date')
    print(type(date))
    date = datetime.strptime(date, '%Y-%m-%d').date()
    list = []
    print(date)

    dates = request.POST.get('dates')
    print(type(dates))
    dates = datetime.strptime(dates, '%Y-%m-%d').date()
    lists = []
    print(dates)

    datas = db.collection('user').document(a).collection('products').get()
    for da in datas:
        data = da.to_dict()
        dat = data['date']
        data["productid"] = da.id
        only_date = dat.date()
        print(only_date)
        if date <= only_date <= dates:
            lists.append(data)
    print(lists)

    return render(request, 'product-history_bn.html', {"prd": lists, "dat": date, "dat_to": dates, "nam": name})


def eval_history(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    names = db.collection('user').document(a).get().to_dict()
    name = names['name']
    return render(request, 'eval_history.html', {"nam": name})


def date_show_eval(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    datas = db.collection('user').document(a).get().to_dict()
    list = []
    perlist = []
    date = request.POST.get('date')
    print(type(date))
    date = datetime.strptime(date, '%Y-%m-%d').date()
    list = []
    print(date)
    data = db.collection('user').where('role', '==', 'user').get()
    for dat in data:
        key = dat.id
        # print(key)
        data_pro = db.collection('user').document(
            key).collection('products').get()
        for pro in data_pro:
            prodict = pro.to_dict()
            dat = prodict['date']
            prodict["productid"] = pro.id
            prodict['userid'] = key
            only_date = dat.date()
            print(dat)
            print(prodict)
            if only_date >= date:

                list.append(prodict)

        data_per = db.collection('user').document(
            key).collection('personal').get()
        for per in data_per:
            perdict = per.to_dict()
            perdict['personid'] = per.id
            perlist.append(perdict)
        name = datas["name"]

    return render(request, "eval_history.html", {"nam": name, "prd": list, "per": perlist, "dat": date})


def eval_history_bn(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    names = db.collection('user').document(a).get().to_dict()
    name = names['name']
    return render(request, 'eval_history_bn.html', {"nam": name})


def date_show_eval_bn(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    datas = db.collection('user').document(a).get().to_dict()
    list = []
    perlist = []
    date = request.POST.get('date')
    print(type(date))
    date = datetime.strptime(date, '%Y-%m-%d').date()

    dates = request.POST.get('dates')
    print(type(dates))
    dates = datetime.strptime(dates, '%Y-%m-%d').date()
    print(dates)
    print(date)

    data = db.collection('user').where('role', '==', 'user').get()
    for dat in data:
        key = dat.id
        # print(key)
        data_pro = db.collection('user').document(
            key).collection('products').get()
        for pro in data_pro:
            prodict = pro.to_dict()
            dat = prodict['date']
            prodict["productid"] = pro.id
            prodict['userid'] = key
            only_date = dat.date()
            print(dat)
            print(prodict)
            if date <= only_date <= dates:
                list.append(prodict)

        data_per = db.collection('user').document(
            key).collection('personal').get()
        for per in data_per:
            perdict = per.to_dict()
            perdict['personid'] = per.id
            perlist.append(perdict)
        name = datas["name"]

    return render(request, "eval_history_bn.html", {"nam": name, "prd": list, "per": perlist, "dat": date})


def categories(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    names = db.collection('user').document(a).get().to_dict()
    name = names['name']
    return render(request, "categories.html", {"nam": name})

#@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def about(request):

    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    names = db.collection('user').document(a).get().to_dict()
    name = names['name']
    return render(request, 'about.html', {'nam': name})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def all_product(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    names = db.collection('user').document(a).get().to_dict()
    name = names['name']


    if request.session.is_empty():
        return redirect(signin)
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    data = db.collection('user').document(a).get().to_dict()
    name = data["name"]

    datas = db.collection('user').document(a).get().to_dict()
    list = []
    perlist = []
    data = db.collection('user').where('role', '==', 'user').get()
    for dat in data:
        key = dat.id
        #print(key)
        data_per = db.collection('user').document(
            key).collection('personal').get()
        for per in data_per:
            perdict = per.to_dict()
            perdict['personid'] = per.id
            p = perdict['date']
            da = {'dal': p.date()}
            ab = p.date()
            perdict.update(da)
            #print(perdict)

            data_pro = db.collection('user').document(
                key).collection('products').where('status','!=', 5).limit(12).get()

            for pro in data_pro:
                prodict = pro.to_dict()
                prodict["productid"] = pro.id
                prodict['userid'] = key
                res = perdict | prodict
                list.append(res)
    #     print(prodict)
    #print(list)
    #print(len(list))
            # list.append(prodict)

    return render(request, 'all_product.html', {'nam': name,"prd": list})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def all_products(request,category):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    names = db.collection('user').document(a).get().to_dict()
    name = names['name']
    print(category)

    if request.session.is_empty():
        return redirect(signin)
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    data = db.collection('user').document(a).get().to_dict()
    name = data["name"]

    datas = db.collection('user').document(a).get().to_dict()
    list = []
    perlist = []
    data = db.collection('user').where('role', '==', 'user').get()
    for dat in data:
        key = dat.id
        #print(key)
        data_per = db.collection('user').document(
            key).collection('personal').get()
        for per in data_per:
            perdict = per.to_dict()
            perdict['personid'] = per.id
            p = perdict['date']
            da = {'dal': p.date()}
            ab = p.date()
            perdict.update(da)
            #print(perdict)
            print(category)
            data_pro = db.collection('user').document(
                key).collection('products').where('status','==', 2).where('category','==',category).limit(12).get()

            for pro in data_pro:
                prodict = pro.to_dict()
                prodict["productid"] = pro.id
                prodict['userid'] = key
                res = perdict | prodict
                list.append(res)
    #     print(prodict)
    #print(list)
    #print(len(list))
            # list.append(prodict)

    return render(request, 'all_products.html', {'nam': name,"prd": list,"category":category})


def faq(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    names = db.collection('user').document(a).get().to_dict()
    name = names['name']
    return render(request, 'faq.html', {'nam': name})


def popular_products(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    names = db.collection('user').document(a).get().to_dict()
    name = names['name']
    return render(request, 'all_product.html', {'nam': name})


def featured_products(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    names = db.collection('user').document(a).get().to_dict()
    name = names['name']
    return render(request, 'all_product.html', {'nam': name})


def contact(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    names = db.collection('user').document(a).get().to_dict()
    name = names['name']
    return render(request, 'contact.html', {'nam': name})


# def cus_pro_details(request):
# 	a = request.session['local']
#     cus_data=db.collection('user').document(a).get().to_dict()

def cus_pro_details(request,pid, uid):
    if request.session.is_empty():
        return redirect(signin)
    a=request.session['local']
    cus_da=db.collection('user').document(uid).collection('products').document(pid).get().to_dict()
    per=db.collection('user').document(uid).collection('personal').get()
    perdicts={}
    #print('hello')
    #print(cus_da)
    for pe in per:
        perdict=pe.to_dict()
        perdict['productid']=pid
        perdict['userid']=uid
    set = 0
    #print(perdict)
    user_ref = db.document('user/'+a)
    own_ref = db.document('user/'+uid)
    own_prd = db.document('user/'+uid+'/products/'+pid)
    checks = db.collection('Check').where('user_ref','==',user_ref).where('product_owner','==',own_ref).where('owner_products','==',own_prd).get()
    if checks != None:
        for check in checks:
            checkd = check.to_dict()
            if checkd["rstatus"]=='requested':
                set = 1

    return render(request,'cus_pro_details.html',{'k':cus_da,'kl':perdict,'set':set})
def coins_check(request,pid, uid):
    if request.session.is_empty():
        return redirect(signin)
    a=request.session['local']

    uref = db.document('user/'+a)
    aref = db.document('user/'+uid)
    apref = db.document('user/'+uid+'/products/'+pid)

    aa = db.collection('Check').where('user_ref','==',uref).where('product_owner','==',aref).where('owner_products','==',apref).get()
    if aa == []:
        db.collection('Check').add({
            'user_ref':uref,
            'product_owner':aref,
            'owner_products':apref,
            'rstatus':'checked'
        })
    coins = 0
    rstid = 0
    coincount=db.collection('Check').where('user_ref','==',uref).where('product_owner','==',aref).where('owner_products','==',apref).get()
    for cv in coincount:
        rstid=cv.id
        co=db.collection('Check').document(cv.id).collection('user_process').get()
        if co not in  []:
            for c in co:
                cd = c.to_dict()
                coins=coins + int(cd["cu_price"])
    print(coins)
    product=[]
    pro = db.collection('user').document(a).collection('products').where('status','==',2).get()
    for p in pro:
        prodict = p.to_dict()
        prodict["productid"] = p.id
        prodict["userid"]=a
        product.append(prodict)
        statuscheck = db.collection('Check').where('user_ref','==',uref).get()

        for status in statuscheck:
            checker = db.collection('Check').document(status.id).collection('user_process').document(p.id).get().to_dict()
            if checker==None:
                pass
            elif  checker["status"]==2:
                product.remove(prodict)
            else:
                pass





    print('welcime')
    print(product)
    avl_pro=db.collection('user').document(uid).collection('products').document(pid).get().to_dict()
    avl_pro['productid']=pid
    avl_pro['userid']=uid
    per=db.collection('user').document(uid).collection('personal').get()
    perdicts=[]
   # print(avl_pro)
    #print(pid)
    for pe in per:
        perdict=pe.to_dict()
        perdict['personid']=pid
        perdict['userid']=uid
        perdicts.append(perdict)
   # print(perdicts)


    return render(request,'coins_check.html',{'prd':product,'k':avl_pro,'kd':perdicts,'c':coins,'rstid':rstid})

def requests(request,rid):
    if request.session.is_empty():
        return redirect(signin)
    a=request.session['local']

    db.collection('Check').document(rid).update({'rstatus':'requested'})
    statuschange = db.collection('Check').document(rid).collection('user_process').get()
    for sc in statuschange:
        db.collection('Check').document(rid).collection('user_process').document(sc.id).update({'status':2})




    # uref = db.document('user/'+a)
    # aref = db.document('user/'+uid)
    # apref = db.document('user/'+uid+'/products/'+pid)
    # product=[]
    # pro = db.collection('user').document(a).collection('products').get()
    # for p in pro:
    #     prodict = p.to_dict()
    #     prodict["productid"] = p.id
    #     prodict["userid"]=a
    #     product.append(prodict)
    #     statuscheck = db.collection('Check').where('user_ref','==',uref).get()

    #     for status in statuscheck:
    #         checker = db.collection('Check').document(status.id).collection('user_process').document(p.id).get().to_dict()
    #         print("checker")
    #         print(checker)
    #         if checker==None:
    #             pass
    #         elif  checker["status"]==1:
    #             product.remove(prodict)
    #         else:
    #             pass

    # uid = request.POST.get('uid')
    # pid = request.POST.get('pid')
    # iuid = request.POST.get('iuid')
    # ipid = request.POST.get('ipid')
    # print('hjjj')
    # print(uid)
    # print(pid)
    # print(iuid)
    # print(ipid)
    # data={
    #     "sale":0
    # }
    # db.collection('user').document(uid).collection('products').document(pid).update(data)

    return redirect(cus_home)
def addcoin(request,upid,apid,auid):
    if request.session.is_empty():
        return redirect(signin)
    uid = request.session['local']
    #upid
    userproduct = db.document('user/'+uid+'/products/'+upid)
    user_ref = db.document('user/'+uid)
    own_ref = db.document('user/'+auid)
    own_prd = db.document('user/'+auid+'/products/'+apid)
    cd = userproduct.get().to_dict()
    coin = cd["cu_price"]
    print(coin)

    checks = db.collection('Check').where('user_ref','==',user_ref).where('product_owner','==',own_ref).where('owner_products','==',own_prd).get()
    for check in checks:
        aa = db.collection('Check').document(check.id).collection('user_process').where('userproduct','==',userproduct).get()
        print(aa)
        if aa == []:
             db.collection('Check').document(check.id).collection('user_process').document(upid).set({'userproduct':userproduct,'status':1,'cu_price':coin})
    return redirect(coins_check,pid=apid,uid=auid)
    #return render(request,'coins_check.html',{'c':coin}, pid=apid,uid=auid)
def removecoin(request,upid,apid,auid):
    if request.session.is_empty():
        return redirect(signin)
    uid = request.session['local']
    #upid
    userproduct = db.document('user/'+uid+'/products/'+upid)
    user_ref = db.document('user/'+uid)
    own_ref = db.document('user/'+auid)
    own_prd = db.document('user/'+auid+'/products/'+apid)
    cd = userproduct.get().to_dict()
    coin = cd["cu_price"]
    print(coin)

    checks = db.collection('Check').where('user_ref','==',user_ref).where('product_owner','==',own_ref).where('owner_products','==',own_prd).get()
    for check in checks:
        aa = db.collection('Check').document(check.id).collection('user_process').where('userproduct','==',userproduct).get()
        print(aa)
        if aa != []:
             db.collection('Check').document(check.id).collection('user_process').document(upid).delete()
    return redirect(coins_check,pid=apid,uid=auid)
def requested_products(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    user_r=db.document('user/'+a)

    av_prod=db.collection('Check').where('user_ref','==',user_r).where('rstatus','==','requested').get()
    av_prodd=[]
    user_pro=[]
    print("jjjjjfjfjfjfjjf")
    for av in av_prod:
        av_pro=av.to_dict()
        av_pro["userid"]=av.id
        prod=av_pro["owner_products"].get()
        produ = prod.to_dict()
        produ["productid"]=prod.id
        own=av_pro["product_owner"].get().to_dict()
        res = av_pro | produ | own

        av_prodd.append(res)

        # pic=res['url']
        # title=res['title']
        # yom=res['yom']
        # material=res['material']
        # brand=res['brand']
        # coins=res['cu_price']
        userproducts = db.collection('Check').document(av.id).collection('user_process').get()
        for up in userproducts:
           udict = up.to_dict()
           uproductdetails = udict["userproduct"].get()
           uproductdict = uproductdetails.to_dict()
           uproductdict["productid"] = uproductdetails.id
           res2 = udict | uproductdict
           res2["userid"] = av.id
           user_pro.append(res2)

    # print(av_prodd)
    print("dfsdfdvdvdvD")
    # my_ii=[]
    # mr_ii=[]
    # mk_ii=[]
    # mypro=db.collection('Check').get()
    # for i in mypro:
    #     my_i=i.to_dict()
    #     #my_i['checkid']=i.id
    #     my_ii.append(my_i)
    #     myprod=db.collection('Check').document(i.id).collection('user_process').get()
    #     myprodds=[]
    #     for ii in myprod:
    #         my_r=ii.to_dict()
    #         mr_ii.append(my_r)
    #         myprods=db.collection('Check').document(i.id).collection('user_process').document(ii.id).get().to_dict()
    #         us_prod=myprods["userproduct"].get().to_dict()
    #         us_prod["userproductid"]=ii.id
    #         myprodds.append(us_prod)


    #         print(myprods)
    #         print(us_prod)
    #         upic=us_prod['url']
    #         utitle=us_prod['title']
    #         uyom=us_prod['yom']
    #         umaterial=us_prod['material']
    #         ubrand=us_prod['brand']
    #         id=us_prod['userproductid']
    print(user_pro)
    context = {'av_prodd':av_prodd,'user_pro':user_pro}

    # for i in av_prodd:
    #     print(["category"])
    return render(request,'requested_products.html',context)
    #return render(request,'requested_products.html',{'pic':pic,'title':title,'yom':yom,'material':material,'brand':brand,'coins':coins,'upic':upic,'utitle':utitle,'uyom':uyom,'umaterial':umaterial,'ubrand':ubrand,'id':id})


def approval(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    owner_r=db.document('user/'+a)
    print(a)
    av_prod=db.collection('Check').where('product_owner','==',owner_r).where('rstatus','==','requested').get()
    av_prodd=[]
    user_pro=[]
    print("jjjjjfjfjfjfjjf")
    for av in av_prod:
        av_pro=av.to_dict()
        av_pro["checkid"]=av.id
        prod=av_pro["owner_products"].get()
        produ = prod.to_dict()
        produ["productid"]=prod.id
        usr=av_pro["user_ref"].get().to_dict()
        res = av_pro | produ | usr

        av_prodd.append(res)

        # pic=res['url']
        # title=res['title']
        # yom=res['yom']
        # material=res['material']
        # brand=res['brand']
        # coins=res['cu_price']
        userproducts = db.collection('Check').document(av.id).collection('user_process').get()
        for up in userproducts:
           udict = up.to_dict()
           uproductdetails = udict["userproduct"].get()
           uproductdict = uproductdetails.to_dict()
           uproductdict["productid"] = uproductdetails.id
           res2 = udict | uproductdict
           res2["checkid"] = av.id
           user_pro.append(res2)

    print(av_prodd)
    print("dfsdfdvdvdvD")
    # my_ii=[]
    # mr_ii=[]
    # mk_ii=[]
    # mypro=db.collection('Check').get()
    # for i in mypro:
    #     my_i=i.to_dict()
    #     #my_i['checkid']=i.id
    #     my_ii.append(my_i)
    #     myprod=db.collection('Check').document(i.id).collection('user_process').get()
    #     myprodds=[]
    #     for ii in myprod:
    #         my_r=ii.to_dict()
    #         mr_ii.append(my_r)
    #         myprods=db.collection('Check').document(i.id).collection('user_process').document(ii.id).get().to_dict()
    #         us_prod=myprods["userproduct"].get().to_dict()
    #         us_prod["userproductid"]=ii.id
    #         myprodds.append(us_prod)


    #         print(myprods)
    #         print(us_prod)
    #         upic=us_prod['url']
    #         utitle=us_prod['title']
    #         uyom=us_prod['yom']
    #         umaterial=us_prod['material']
    #         ubrand=us_prod['brand']
    #         id=us_prod['userproductid']
    #print(user_pro)
    context = {'av_prodd':av_prodd,'user_pro':user_pro}

    # for i in av_prodd:
    #     print(["category"])
    return render(request,'waiting_for_approval.html',context)

def sold_recieved(request):
    a = request.session['local']
    owner_r=db.document('user/'+a)

    av_prod=db.collection('Order').where('product_owner','==',owner_r).where('rstatus','==','accepted').get()
    av_prodd=[]
    user_pro=[]
    print("jjjjjfjfjfjfjjf")
    for av in av_prod:
        av_pro=av.to_dict()
        av_pro["orderid"]=av.id
        prod=av_pro["owner_products"].get()
        produ = prod.to_dict()
        produ["productid"]=prod.id
        usr=av_pro["user_ref"].get().to_dict()
        res = av_pro | produ | usr

        av_prodd.append(res)


        userproducts = db.collection('Order').document(av.id).collection('user_process').get()
        for up in userproducts:
           udict = up.to_dict()
           uproductdetails = udict["userproduct"].get()
           uproductdict = uproductdetails.to_dict()
           uproductdict["productid"] = uproductdetails.id
           res2 = udict | uproductdict
           res2["orderid"] = av.id
           user_pro.append(res2)

    print(av_prodd)
    print("dfsdfdvdvdvD")


    context = {'av_prodd':av_prodd,'user_pro':user_pro}
    return render(request,'sold_recieved.html',context)
def recieved_sold(request):
    a = request.session['local']
    user_ref=db.document('user/'+a)

    av_prod=db.collection('Order').where('user_ref','==',user_ref).where('rstatus','==','accepted').get()
    av_prodd=[]
    user_pro=[]
    print("jjjjjfjfjfjfjjf")
    for av in av_prod:
        av_pro=av.to_dict()
        av_pro["orderid"]=av.id
        prod=av_pro["owner_products"].get()
        produ = prod.to_dict()
        produ["productid"]=prod.id
        usr=av_pro["user_ref"].get().to_dict()
        res = av_pro | produ | usr

        av_prodd.append(res)


        userproducts = db.collection('Order').document(av.id).collection('user_process').get()
        for up in userproducts:
           udict = up.to_dict()
           uproductdetails = udict["userproduct"].get()
           uproductdict = uproductdetails.to_dict()
           uproductdict["productid"] = uproductdetails.id
           res2 = udict | uproductdict
           res2["orderid"] = av.id
           user_pro.append(res2)

    print(av_prodd)
    print("dfsdfdvdvdvD")


    context = {'av_prodd':av_prodd,'user_pro':user_pro}
    return render(request,'recieved_sold.html',context)

def satisfy_click(request,chid):
    id = request.session['local']
    data = db.collection('Order').document(chid).get().to_dict()
    if data["satisfystatus"]==1:
        db.collection('Order').document(chid).update({'satisfystatus':2})
    elif data["satisfystatus"]==0:
        db.collection('Order').document(chid).update({'satisfystatus':1})
    datas= db.collection('Order').document(chid).get().to_dict()
    if datas["satisfystatus"]==2:
        satisfied = db.collection('Order').document(chid).update({'rstatus':'satisfied'})



    return redirect(myads)
def nonsatisfy_click(request,chid):
    # id = request.session['local']
    data = db.collection('Order').document(chid).get().to_dict()
    cancel = db.collection('Order').document(chid).update({'rstatus':'cancel'})
    # cancels = db.collection('Order').document(chid).update({'status':2})


    data["owner_products"].update({'status':2})
    checked_products = db.collection('Order').document(chid).collection('user_process').get()
    for cp in checked_products:
        cp.id
        cd=cp.to_dict()
        cd['userproduct'].update({'status':2})


    #disabling ids




    return redirect(myads)



def approve_click(request,chid):
    today=datetime.now()
    checked = db.collection('Check').document(chid).get().to_dict()
    data = {
           'user_ref':checked["user_ref"],
           'product_owner':checked["product_owner"],
           'owner_products':checked["owner_products"],
           'rstatus':'accepted',
           'date':today,
           'satisfystatus':0
    }
    checked["owner_products"].update({'status':5})

    db.collection('Order').document(chid).set(data)

    checked_products = db.collection('Check').document(chid).collection('user_process').get()

    for cp in checked_products:
        cp.id
        cd=cp.to_dict()

        datas={
            'cu_price':cd['cu_price'],
            'status':3,
            'userproduct':cd['userproduct']

        }
        cd['userproduct'].update({'status':5})
        db.collection('Order').document(chid).collection('user_process').document(cp.id).set(datas)

    #disabling ids
    checkduplicate=db.collection('Check').where('product_owner','==',checked["product_owner"]).where('owner_products','==',checked["owner_products"]).get()
    if checkduplicate:
        for cd in checkduplicate:
            db.collection('Check').document(cd.id).delete()

    db.collection('Check').document(chid).delete()

    return redirect(myads)

def reject_click(request,chid):
    data = db.collection('Check').document(chid).delete()
    #reject = db.collection('Order').document(chid).update({'rstatus':'reject'})
    # cancels = db.collection('Order').document(chid).update({'status':2})


    #data["owner_products"].update({'status':2})
    # checked_products = db.collection('Order').document(chid).collection('user_process').get()
    # for cp in checked_products:
    #     cp.id
    #     cd=cp.to_dict()
    #     cd['userproduct'].update({'status':2})


    return redirect(myads)

def satisfied_recieved(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    owner_r=db.document('user/'+a)



    av_prod=db.collection('Order').where('product_owner','==',owner_r).where('rstatus','==','satisfied').get()



    av_prodd=[]
    user_pro=[]
    print("jjjjjfjfjfjfjjf")
    for av in av_prod:
        av_pro=av.to_dict()
        av_pro["orderid"]=av.id
        prod=av_pro["owner_products"].get()
        produ = prod.to_dict()
        produ["productid"]=prod.id
        usr=av_pro["user_ref"].get().to_dict()
        own=av_pro["product_owner"].get().to_dict()

        res = av_pro | produ | usr
        res["ownername"]=own["name"]
        av_prodd.append(res)


        userproducts = db.collection('Order').document(av.id).collection('user_process').get()
        for up in userproducts:
           udict = up.to_dict()
           uproductdetails = udict["userproduct"].get()
           uproductdict = uproductdetails.to_dict()
           uproductdict["productid"] = uproductdetails.id
           res2 = udict | uproductdict
           usernamefetch = db.collection('Order').document(av.id).get().to_dict()
           usernamefetchd = usernamefetch['user_ref'].get().to_dict()
           res2['name']=usernamefetchd["name"]
           res2["orderid"] = av.id
           user_pro.append(res2)

    print(av_prodd)
    print("dfsdfdvdvdvD")


    context = {'av_prodd':av_prodd,'user_pro':user_pro}
    return render(request,'satisfied_recieved.html',context)

def satisfied_given(request):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    user_r=db.document('user/'+a)




    av_prod=db.collection('Order').where('user_ref','==',user_r).where('rstatus','==','satisfied').get()

    av_prodd=[]
    user_pro=[]
    print("jjjjjfjfjfjfjjf")
    for av in av_prod:
        av_pro=av.to_dict()
        av_pro["orderid"]=av.id
        prod=av_pro["owner_products"].get()
        produ = prod.to_dict()
        produ["productid"]=prod.id
        usr=av_pro["user_ref"].get().to_dict()
        own=av_pro["product_owner"].get().to_dict()

        res = av_pro | produ | usr
        res["ownername"]=own["name"]
        av_prodd.append(res)

        userproducts = db.collection('Order').document(av.id).collection('user_process').get()
        for up in userproducts:
           udict = up.to_dict()
           uproductdetails = udict["userproduct"].get()
           uproductdict = uproductdetails.to_dict()
           uproductdict["productid"] = uproductdetails.id
           res2 = udict | uproductdict
           usernamefetch = db.collection('Order').document(av.id).get().to_dict()
           usernamefetchd = usernamefetch['user_ref'].get().to_dict()
           res2['name']=usernamefetchd["name"]
           res2["orderid"] = av.id
           user_pro.append(res2)


    print(av_prodd)
    print("dfsdfdvdvdvD")


    context = {'av_prodd':av_prodd,'user_pro':user_pro}

    return render(request,'satisfied_given.html',context)


def update_post(request,up):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    product = db.collection('user').document(a).collection('products').document(up).get().to_dict()
    print(product)
    cat = product['category']
    print(cat)
    personal = db.collection('user').document(
            a).collection('personal').get()
    person = personal[0].id
    personals = db.collection('user').document(a).collection(
        'personal').document(person).get().to_dict()
    data = db.collection('user').document(a).get().to_dict()
    name = data["name"]
    return render(request, 'update_post.html', {'pro':  product, "fr": up,"f":cat,'per': personals, "nam": name,"up":up})

def update_pro(request):
    if request.session.is_empty():
        return redirect(signin)

    a = request.session['local']
    upda=request.POST.get('update')
    title = request.POST.get('title')
    brand = request.POST.get('brand')
    material = request.POST.get('material')
    category = request.POST.get('category')
    scratch = request.POST.get('scratch')
    weight = request.POST.get('weight')
    condition = request.POST.get('condition')
    type = request.POST.get('type')
    color = request.POST.get('color')
    stones = request.POST.get('stones')
    buy_price = request.POST.get('buy_price')
    Design_works = request.POST.get('Design_works')
    model = request.POST.get('model')
    yom = request.POST.get('yom')
    cu_price = request.POST.get('cu_price')
    adpost = request.POST.get('adpost')

    url = request.POST.get('url')
    url1 = request.POST.get('url1')
    url2 = request.POST.get('url2')
    url3 = request.POST.get('url3')
    demtitle = request.POST.get('demtitle')
    dembrand = request.POST.get('dembrand')
    demcategory = request.POST.get('demcategory')
    demcolor = request.POST.get('demcolor')
    demyom = request.POST.get('demyom')
    today = datetime.now()
    tok = today

    try:
        a = request.session['local']

        data = {
            "title": title,
            "brand": brand,
            "material": material,
            "category": category,
            "scratch": scratch,
            "weight": weight,
            "condition": condition,
            "type": type,
            "color": color,
            "stones": stones,
            "Design_works": Design_works,
            "model": model,
            "buy_price": buy_price,
            "yom": yom,
            "cu_price": cu_price,
            "adpost": adpost,
            "url": url,
            "url1": url1,
            "url2": url2,
            "url3": url3,
            "demtitle": demtitle,
            "dembrand": dembrand,
            "demcategory": demcategory,
            "demcolor": demcolor,
            "demyom": demyom,
            "status": 0,
            "date": today,
            "toda": tok


        }
        product = db.collection('user').document(a).collection('products').document(upda).update(data)
        return redirect(update_pic,upda,category)
        return redirect(myads)
    except KeyError:
        message = "Oops! User logged out please sign in again"
        return render(request, "signin.html", {"mess": message})
    return redirect(myads)
def update_pic(request,pr,fr):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']
    personal = db.collection('user').document(a).collection('personal').get()
    person = personal[0].id
    personals = db.collection('user').document(a).collection(
        'personal').document(person).get().to_dict()
    data = db.collection('user').document(a).get().to_dict()
    name = data["name"]
    print(pr)
    tit=db.collection('user').document(a).collection('products').document(pr).get().to_dict()
    print("fvkjd")
    return render(request,'update_pic.html', {'per': personals, "nam": name, "f": fr,"p":pr,"t":tit})


def delete_pro(request,dl):
    if request.session.is_empty():
        return redirect(signin)
    a = request.session['local']

    product = db.collection('user').document(a).collection('products').document(dl).get().to_dict()
    data={"status":6}
    db.collection('user').document(a).collection('products').document(dl).update(data)

    return redirect(myads)

def evaluator_profile(request):

    return render(request,'evaluator_profile.html')

def search(request):
    a=request.session['local']
    district=request.POST.get('district')
    category=request.POST.get('category')
    prolist=[]
    if district != 'none' and category != 'none' :
        user=db.collection('user').get()
        for u in user:
            personal=db.collection('user').document(u.id).collection('personal').where('district','==',district).get()
            for person in personal:
                parent=person.reference.parent.parent.id
                if parent != a:
                    persondict = person.to_dict()
                    print("gefdf")
                    print(persondict)
                    prod=db.collection('user').document(parent).collection('products').where('category','==',category).get()
                    for pp in prod:
                        product=pp.to_dict()
                        product["userid"]=parent
                        product["productid"]=pp.id
                        product["district"]=persondict["district"]
                        product["state"]=persondict["state"]
                        res = product
                        prolist.append(res)
    print(prolist)
    return render(request,'all_products.html', {"prd": prolist,"district":district,"category":category})





























