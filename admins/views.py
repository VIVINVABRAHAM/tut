from unicodedata import category
from django.shortcuts import render,redirect
from django.shortcuts import render
from pyparsing import Or
import pyrebase
from regex import E
from django.contrib import auth,messages
import firebase_admin
from firebase_admin import credentials,firestore
from account.views import authe,db
from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    if request.session.is_empty():
        return redirect(admin_sign)
    auth.logout(request)
    request.session.flush()
    return render(request,'admin_sign.html')
def admin_sign(request):
    return render(request,'admin_sign.html')
def postadminsg(request):
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    try:
        user=authe.sign_in_with_email_and_password(email,passw)
    except:
        message="invalid credentials"
        return render(request,"admin_sign.html",{"messg":message})
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    idtoken=request.session['uid']
    a=authe.get_account_info(idtoken)

    a=a['users']

    a=a[0]

    a=a['localId']

    request.session['local']=a
    datas= db.collection('user').document(a).get().to_dict()
    if datas["role"] == "admin":
        return redirect(admin_home)
    else:
        messages.error(request,'Invalid Credentials')
        return redirect(admin_sign)



def admin_home(request):
    if request.session.is_empty():
        return redirect(admin_sign)
    a=request.session['local']
    return render(request,'admin_home.html')
def admin_deactive(request):
    if request.session.is_empty():
        return redirect(admin_sign)
    a=request.session['local']
    datas= db.collection('user').where('role','==','user').get()
    list=[]
    perlist = []
    for dat in datas:
        key = dat.id
        Udet=dat.to_dict()
        name=Udet['name']
        data=db.collection('user').document(key).collection('products').where('status','==',0 ).get()
        for da in data:
            datdic=da.to_dict()
            datdic['productid']=da.id
            datdic['userid']=key
            datdic['name']=name
            list.append(datdic)
    #print(list)
    return render(request,'admin_deactive.html',{'det':list})
def admin_processing(request):
    if request.session.is_empty():
        return redirect(admin_sign)
    a=request.session['local']
    datas= db.collection('user').where('role','==','user').get()
    list=[]
    perlist = []
    for dat in datas:
        key = dat.id
        Udet=dat.to_dict()
        name=Udet['name']

        data=db.collection('user').document(key).collection('products').where('status','==',1 ).get()
        for da in data:
            datdic=da.to_dict()
            datdic['productid']=da.id
            datdic['userid']=key
            datdic['name']=name
            list.append(datdic)


    #print(list)
    return render(request,'admin_processing.html',{'pro':list})
def admin_user(request):
    if request.session.is_empty():
        return redirect(admin_sign)

    a=request.session['local']
    datas= db.collection('user').where('role','==','user').get()
    list=[]
    perlist = []
    for dat in datas:
        key = dat.id
        data=db.collection('user').document(key).collection('personal').get()
        for da in data:
            datdic=da.to_dict()
            datdic['userid']=key
            list.append(datdic)
    #print(list)
    # data_per=db.collection('user').document(key).collection('personal').get()
    # for per in data_per:
    #     perdict=per.to_dict()
    #     perdict['personid']=per.id
    #     perlist.append(perdict)
    # print(perlist)

    return render(request,'admin_user.html',{'dd':list})
def admin_evaluator(request):
    if request.session.is_empty():
        return redirect(admin_sign)
    a=request.session['local']
    datas= db.collection('user').where('role','==','Evaluator').get()
    list=[]
    perlist = []
    for dat in datas:
        key = dat.id
        data=db.collection('user').document(key).collection('personal').get()
        for da in data:
            datdic=da.to_dict()
            datdic['userid']=key
            list.append(datdic)
    #print(list)
    return render(request,'admin_evaluator.html',{'ev':list})
def admin_demand(request):
    if request.session.is_empty():
        return redirect(admin_sign)
    a=request.session['local']
    datas= db.collection('user').where('role','==','user').get()
    list=[]
    perlist = []
    for dat in datas:
        key = dat.id
        Udet=dat.to_dict()
        name=Udet['name']

        data=db.collection('user').document(key).collection('products').get()
        for da in data:
            datdic=da.to_dict()
            datdic['productid']=da.id
            datdic['userid']=key
            datdic['name']=name
            list.append(datdic)
    #print(list)

    return render(request,'admin_demand.html',{'dem':list})

def admin_approved(request):
    if request.session.is_empty():
        return redirect(admin_sign)
    a=request.session['local']
    datas= db.collection('user').where('role','==','user').get()
    list=[]
    perlist = []
    for dat in datas:
        key = dat.id
        Udet=dat.to_dict()
        name=Udet['name']
        data=db.collection('user').document(key).collection('products').where('status','==',2 ).get()
        for da in data:
            datdic=da.to_dict()
            datdic['productid']=da.id
            datdic['userid']=key
            datdic['name']=name
            list.append(datdic)


    #print(list)
    return render(request,'admin_approved.html',{'apr':list})


def admin_pro_details(request,pid,uid):
    if request.session.is_empty():
        return redirect(admin_sign)
    a=request.session['local']

    data=db.collection('user').document(uid).collection('products').document(pid).get().to_dict()
    persons= db.collection('user').document(uid).collection('personal').get()
    names= db.collection('user').document(a).get().to_dict()

    pdict={}
    for pp in persons:
        pdict=pp.to_dict()
        pdict["productid"]=pid
        pdict["userid"]=uid

    return render(request,'admin_pro_details.html',{'k':data,"per":pdict})

def way_approve(request,pid,uid):
    db.collection('user').document(uid).collection('products').document(pid).update({'status':2})


    return redirect(admin_processing)

def admin_products(request):
    if request.session.is_empty():
        return redirect(admin_sign)
    a=request.session['local']
    datas= db.collection('user').where('role','==','user').get()
    list=[]
    perlist = []
    for dat in datas:
        key = dat.id
        Udet=dat.to_dict()
        name=Udet['name']

        data=db.collection('user').document(key).collection('products').get()
        for da in data:
            datdic=da.to_dict()
            datdic['productid']=da.id
            datdic['userid']=key
            datdic['name']=name
            list.append(datdic)


    #print(list)
    return render(request,'admin_products.html',{'prod':list})


def user_delete(request,uid):
    if request.session.is_empty():
        return redirect(admin_sign)
    a=request.session['local']
    list=[]
    uref = db.document('user/'+uid)


    user1=db.collection('Check').where('user_ref','==',uref).where('rstatus','==','requested').get()
    user2=db.collection('Check').where('product_owner','==',uref).where('rstatus','==','requested').get()
    user3=db.collection('Order').where('user_ref','==',uref).where('rstatus','==','accepted').get()
    user4=db.collection('Order').where('product_owner','==',uref).where('rstatus','==','accepted').get()
    print("hee")
    print(user1)
    print("hee")
    print(user2)
    print("hee")
    print(user3)
    print("hee")
    print(user4)
    if(user1 == user2 == user3 == user4 == []):
        print("You can delete")
        user_data=db.collection('user').document(uid).collection('personal').get()
        for us in user_data:
            user_datas=us.to_dict()
            user=us.id
            db.collection('user').document(uid).set({"status":1})

            print(user_datas)
        messages.success(request,"User deleted sucessfully")
        return redirect(admin_home)
    else:
        messages.success(request,"User is active in another transaction Cannot delete")
        return redirect(admin_user)

