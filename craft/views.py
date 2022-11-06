from itertools import product
from django.shortcuts import render,redirect
from django.http import HttpResponse
from craftAdmins.models import Category,Product,Admin,Order
from .models import Customer,UserOrder
from django.contrib.auth.hashers import make_password,check_password
# Create your views here.
def index(request):
    products=Product.get_all_products()
    print(request.session.get('customer_email'))

    return render(request,'index.html',{'products':products})

def product_desc(request):
    if request.method=='POST':
        prod_id=request.POST.get('product_id')
        quant=request.POST.get('quantity')
        quant=int(quant)
        cart=request.session.get('cart')
        if cart:
            quantt=cart.get(prod_id)
            if quantt:
                print(cart)
                cart[prod_id]=quantt+1
            else:
                cart[prod_id]=quant

        else:
            cart={}
            cart[prod_id]=quant
        request.session['cart']=cart
        print(cart)
        return redirect('cart')

    else:
        prd_id=request.GET.get('prod_id')
        if prd_id:
            products=Product.get_all_products_by_prd_id(prd_id)
        else:
            pass
        print(prd_id)
        print(products)
        return render(request,'product_description.html',{'products':products[0]})

def registration(request):
    if request.method=='GET':
        return render(request,'registration.html')
    else:
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('pass')
        c_pass=request.POST.get('c_pass')
        phone=request.POST.get('phone_number')
        addr=request.POST.get('address')
        pin=request.POST.get('pin')
        addr=addr+", pin code "+pin
        customer=Customer(name=name,email=email,
                        phone=phone,password=password,
                        address=addr)
        customer.password=make_password(customer.password)
        isExist=customer.isExists()
        
        if isExist:
            error="Email already registered"
            return render(request,'registration.html',{'error':error})
        customer.register()
        request.session['customer_id']=customer.id
        request.session['customer_email']=customer.email
        return redirect('homepage')



def login(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        email=request.POST.get('email')
        password=request.POST.get('password')
        customer=Customer.get_user_by_email(email) # return object matching email
        if customer:
            flag=check_password(password,customer.password)
            if flag:
                if request.session.get('cart'):
                    request.session['customer_id']=customer.id
                    request.session['customer_email']=customer.email
                    return redirect('homepage')
                else:
                    cart={}
                    request.session['cart']=cart
                    request.session['customer_id']=customer.id
                    request.session['customer_email']=customer.email
                    return redirect('homepage')


            else:
                error="Invalid email or password !!! "
                return render(request,'login.html',{'error1':error})

        else:
            error="Invalid email or password !!! "
            return render(request,'login.html',{'error1':error})
    



def shop(request):
    products=Product.get_all_products()
    cat=Category.get_all_category()
    cat_id=request.GET.get('Category')
    if cat_id:
        products=Product.get_all_products_by_cat_id(cat_id)
    else:
        products=Product.get_all_products()
        
    data={}
    data['products']=products
    data['categ']=cat
    
    return render(request,'shop.html',data)


def profile(request):
    if request.session.get('customer_id'):
        email=request.session.get('customer_email')
        user=Customer.get_user_by_email(email=email)
        print(user)
        return render(request,'profile.html',{"users":user})
    else:
        return redirect('login')


def compare(request):
    if request.method=='POST':
        prod_id=request.POST.get('p_id')
        print(prod_id)
        compare=request.session.get('comp')
        if compare:
            quantt=compare.get(prod_id)
            if quantt:
                print(compare)
            else:
                compare[prod_id]=1
                request.session['comp']=compare
            list_id=list(request.session.get('comp'))
            print(list_id)
            items=Product.get_all_products_by_ids(list_id)
            print(items)

        else:
            compare={}
            compare[prod_id]=1
            request.session['comp']=compare
        print(compare)
        list_id=list(request.session.get('comp'))
        print(list_id)
        items=Product.get_all_products_by_ids(list_id)
        print(items)
    return render(request,'compare.html',{'products':items})


def editAccount(request):
    if request.method=="GET" :
        if request.session.get('customer_id'):
            email=request.session.get('customer_email')
            user=Customer.get_user_by_email(email=email)
            print(user)
            return render(request,'edit_account.html',{"users":user})
        else:
            return redirect('login')

    else:
        mail=request.POST.get('email')
        password1=request.POST.get('pass')
        c_id=request.session['customer_id']
        customer1=Customer.get_by_id(c_id) # return object matching email
        if customer1:
            flag=check_password(password1,customer1[0].password)
            print(flag)
            if flag==True:
                name1=request.POST.get('name')
                phone1=request.POST.get('phone')
                addr=request.POST.get('address')
                customer1.update(name=name1,phone=phone1,address=addr,email=mail)
                if request.session['customer_email']!=mail:
                    request.session['customer_email']=mail

                print(name1,phone1,addr)
                return redirect('profile')
            
            else:
                c_id=request.session['customer_id']
                user=Customer.get_by_id(c_id)
                print(user)
                error="Something went wrong"
                return render(request,'edit_account.html',{"users":user,'error':error})

        else:
            return redirect('profile')      

            

def cart(request):
    try:
        if request.session.get('cart'):
            list_id=list(request.session.get('cart'))
            print(list_id)
            items=Product.get_all_products_by_ids(list_id)
            return render(request,'cart.html',{'carts':items})
        else:
            request.session['cart']={}
            return render(request,'cart.html')
    except:
        return render(request,'cart.html')

def deleteCart(request):
    id=request.GET.get('pid')
    cart1=request.session.get('cart')
    del cart1[id]
    print(cart1)
    request.session['cart']=cart1
    return redirect('cart')


def checkout(request):
    if request.session.get('cart'):
        print(request.session.get('cart'))
        list_id=list(request.session.get('cart'))
        #print(list_id)
        if request.session.get('customer_id'):
            c_id=request.session['customer_id']
            customer1=Customer.get_by_id(c_id)
            address=customer1[0].address
            items=Product.get_all_products_by_ids(list_id)
            return render(request,'checkout.html',{'carts':items,'addr':address})
        else:
            return redirect('login')
    else:
        return render(request,'cart.html')

def saveOrder(request):
    if request.session.get('cart') and request.method=="POST":
        
        payment_method=request.POST.get('payment-method')
        print(payment_method)
        cart=request.session.get('cart')
        c_id=request.session['customer_id']
        customer1=Customer.get_by_id(c_id)
        addr=customer1[0].address
        ph=customer1[0].phone
        products=Product.get_all_products_by_ids(list(cart))
        for p in products:
            order=UserOrder(customer=Customer(id=c_id),productName=p.name,
            productimg=p.img1,quantity=cart.get(str(p.id)),price=p.price,)

            order.UserPlaceOrder()

            Aorder=Order(product=p,customer=Customer(id=c_id),quantity=cart.get(str(p.id)),
                     price=p.price,address=addr,phone=ph,paymentMethod=payment_method,manufacturer=p.manufacturer,status="Pending")
            Aorder.saveOrder()

        request.session['cart']={}
        return redirect('order')
    else:
        return redirect('cart')


def myOrder(request):
    if request.method=="GET" and request.session.get('customer_id'):

        allorder=UserOrder.get_all_order()
        return render(request,'order.html',{'order':allorder})
    else:
        return redirect('login')
        
def deleteOrder(request):
    id= request.GET.get('pid')
    UserOrder.deleteorder(id)
    Order.deleteorder(id)
    return redirect('order')
    

def logout(request):
    request.session.clear()
    return redirect('login')