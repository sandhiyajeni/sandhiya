from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from appyuvan.models import Order, Products,Cart
from django.db.models import Q
import random
import razorpay
def index(request):
    a={}
    p=Products.objects.filter(is_active=True)
    a['products']=p
    return render(request,'index.html',a)
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')

def register(request):
    a={}
    if request.method=='GET':
        return render(request,'register.html')
    else:
        user=request.POST['uname']
        psd=request.POST['upass']
        cpsd=request.POST['ucpass']
        print(user,psd,cpsd)
        if user=='' or psd=='' or cpsd=='':
            a['err']='fill all the field'
            return render(request,"register.html",a)
        elif psd != cpsd:
            a['err']='password didnot match'
            return render(request,"register.html",a)
        else:
            u= User.objects.create(username=user,email=user,password=psd)
            u.set_password(psd)
            u.save()
            a['success']="successfully register!please login"
            return render(request,"register.html",a)
def user_login(request):
    a={}
    if request.method=='GET':
        return render(request,'login.html')
    else:
        u1=request.POST['uname']
        p1=request.POST['upass']
        if u1=='' or p1=='':
            a['err']='field cannot be blank...please fill the field'
            return render(request,'login.html',a)
        else:
            u=authenticate(username=u1,password=p1)
            print(u)
            if u is not None:
                login(request,u)
                return redirect('/')
            else:
                a['err']='username and password are invalid'
                return render(request,'login.html',a)
def user_logout(request):
    logout(request)
    return redirect('/')
def catfilter(request,a):
    q1=Q(is_active=True)
    q2=Q(cat=a)
    p=Products.objects.filter(q1 & q2)
    b={}
    b['products']=p
    return render(request,'index.html',b)
def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    p=Products.objects.filter(q1 & q2)
    a={}
    a['products']=p
    return render(request,"index.html",a)

def sort(request,a):
    if a=='0':
        col="price"
    else:
        col="-price"
    p=Products.objects.filter(is_active=True).order_by(col)
    b={}
    b['products']=p
    return render(request,"index.html",b)
def product_details(request,pid):
    a={}
    p=Products.objects.filter(id=pid)
    a['products']=p
    return render(request,'product_details.html',a)
def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        q1=Q(uid=userid)
        q2=Q(pid=pid)
        c=Cart.objects.filter(q1 & q2)
        p=Products.objects.filter(id=pid)
        a={}
        a['products']=p 
        if c:
            a['msg']='product already exist'
            return render(request,'product_details.html',a)
        else:
            u=User.objects.filter(id=userid)
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            a['success']='product added successfully'
            return render(request,'product_details.html',a)
    else:
        return redirect('/login')
def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/cart')
def cartqty(request,a,pid):
    userid=request.user.id
    q1=Q(uid=userid)
    q2=Q(pid=pid)
    c=Cart.objects.filter(q1 & q2)
    #print(c)
    qty=c[0].qty
    # print(c[0])
    # print(qty)
    if a=='0':
        if qty>1:
            qty=qty-1
            c.update(qty=qty)
    else:
        qty=qty+1
        c.update(qty=qty)
    return redirect('/cart')
def cart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    sum=0
    for x in c:
        sum=sum+(x.qty*x.pid.price)
    print("total",sum)
    a={}
    a['products']=c
    a['items']=len(c)
    a['total']=sum

    return render(request,'cart.html',a)
def placeorder(request):
    if request.user.is_authenticated:
        a={}
        userid=request.user.id
        c=Cart.objects.filter(uid=userid)
        oid=random.randrange(1000,9999)
        for x in c:
            o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
            o.save()
            x.delete()
        j=Order.objects.filter(uid=userid)
        sum=0
        for y in j:
            sum=sum+(y.qty*y.pid.price)
        a['products']=c
        a['items']=len(c)
        a['total']=sum
        return render(request,'placeorder.html',a)
    else:
        return redirect('/login')
def makepayment(request):
    userid=request.user.id
    client = razorpay.Client(auth=("rzp_test_KLuc8q5Pngg5XZ", "ftAymVb196pQvWtafzWAM5GE"))
    o=Order.objects.filter(uid=userid)
    sum=0
    for x in o:
        sum=sum+(x.qty*x.pid.price)
    
    sum=sum*100  #conversion of Rs into Paise
    data = { "amount":sum, "currency": "INR", "receipt":str(o[0].id) }
    payment = client.order.create(data=data)
    print(payment)
    content={}
    content['payment']=payment
    
    return render(request,'pay.html',content)


        











