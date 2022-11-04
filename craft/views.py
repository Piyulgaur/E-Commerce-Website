from urllib import request
from .models import Product
from itertools import product
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Category, Product,Customer,Admin
from django.contrib.auth.hashers import make_password,check_password


def homePage(request):
    products = Product.get_all_products()
    print(request.session.get('customer_email'))
    return render(request,'index.html',{'products':products})


def products(request):
    return render(request,"products.html")


def ShowProduct(request):
    if request.method=="GET":
        prod=Product.get_all_products()
        return render(request,'product.html',{'product':prod})


def login(request):
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")


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
        return render(request,'shop.html')

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
        uname=request.POST.get('uname')
        addr=addr+pin
        customer=Customer(name=name,email=email,
                        phone=phone,password=password,
                        address=addr,username=uname)
        customer.password=make_password(customer.password)
        isExist=customer.isExists()
        
        if isExist:
            error="Email algready registered"
            return render(request,'registration.html',{'error':error})
        customer.register()
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
    if request.session['customer_id']:
        email=request.session['customer_email']
        user=Customer.get_user_by_email(email=email)
        print(user)
        return render(request,'profile.html',{"users":user})

    else:
        return render(request,'login.html')


def editAccount(request):
    if request.method=="GET" :
        if request.session['customer_id']:
            email=request.session['customer_email']
            user=Customer.get_user_by_email(email=email)
            print(user)
            return render(request,'edit_account.html',{"users":user})
        else:
            return render(request,'login.html')

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
        c_id=request.session['customer_id']
        customer1=Customer.get_by_id(c_id)
        address=customer1[0].address
        items=Product.get_all_products_by_ids(list_id)
        return render(request,'checkout.html',{'carts':items,'addr':address})
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
            order=UserOrder(customer=Customer(id=c_id),productName=p.name
            ,quantity=cart.get(str(p.id)),price=p.price,)
            order.UserPlaceOrder()

            Aorder=Order(product=p,customer=Customer(id=c_id),quantity=cart.get(str(p.id)),
                     price=p.price,address=addr,phone=ph,paymentMethod=payment_method,manufacturer=p.manufacturer)
            Aorder.saveOrder()

        request.session['cart']={}
        return redirect('cart')
    else:
        return redirect('cart')

def myOrder(request):
    if request.method=="GET":
        allorder=UserOrder.get_all_order()
        return render(request,'order.html',{'order':allorder})


def adminLogin(request):
    if request.method=='GET':
        return render(request,'./admin_area/admin_login.html')
    else:
        email=request.POST.get('email')
        password=request.POST.get('password')
        admin=Admin.get_admin_by_email(email) # return object matching email
        if admin:
            flag=check_password(password,admin.password)
            if flag:
                request.session['admin_id']=admin.id
                request.session['admin_email']=admin.email
                return redirect('adminProduct')
            else:
                error="Invalid email or password !!! "
                return render(request,'./admin_area/admin_login.html',{'error1':error})

        else:
            error="Invalid email or password !!! "
            return render(request,'./admin_area/admin_login.html',{'error1':error})


def adminRegister(request):
    if request.method=='GET':
        return render(request,'./admin_area/admin_register.html')
    else:
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('pass')
        c_pass=request.POST.get('c_pass')
        phone=request.POST.get('phone_number')
        addr=request.POST.get('address')
        pan1=request.POST.get('pan')
        gst=request.POST.get('gst')
        print(pan1)
        admin=Admin(name=name,email=email,
                        phone=phone,password=password,
                        address=addr,gst=gst,pan=pan1)
        admin.password=make_password(admin.password)
        isExist=admin.isExists()
        
        if isExist:
            error="Email algready registered"
            return render(request,'./admin_area/admin_register.html',{'error':error})
        admin.register()
        request.session['admin_id']=admin.id
        request.session['admin_email']=admin.email
        return redirect('adminProduct')

    
def adminProfile(request):
    print(request.session.get('admin_email'))
    if request.session.get('admin_email'):
        email=request.session.get('admin_email')
        user=Admin.get_admin_by_email(email=email)
        print(user)
        return render(request,'./admin_area/admin_profile.html',{"users":user})

    else:
        return redirect('adminLogin')

def editAdminAccount(request):
    if request.method=="GET" :
        if request.session['admin_id']:
            email=request.session.get('admin_email')
            user=Admin.get_admin_by_email(email=email)
            print(user)
            return render(request,'./admin_area/edit_admin_profile.html',{"users":user})
        else:
            return render(request,'login.html')

    else:
        mail=request.POST.get('email')
        password1=request.POST.get('pass')
        c_id=request.session['admin_id']
        customer1=Admin.get_by_id(c_id) # return object matching email
        if customer1:
            flag=check_password(password1,customer1[0].password)
            print(flag)
            if flag==True:
                name1=request.POST.get('name')
                phone1=request.POST.get('phone')
                addr=request.POST.get('address')
                gstin=request.POST.get('gst')
                pann=request.POST.get('pan')
                customer1.update(name=name1,phone=phone1,address=addr,email=mail,gst=gstin,pan=pann)
                if request.session['admin_email']!=mail:
                    request.session['admin_email']=mail

                print(name1,phone1,addr)
                return redirect('Adminprofile')
            
            else:
                c_id=request.session['admin_id']
                user=Admin.get_by_id(c_id)
                print(user)
                error="Something went wrong"
                return render(request,'./admin_area/edit_admin_profile.html',{"users":user,'error':error})

        else:
            return redirect('Adminprofile')


def adminProduct(request):
    mail=request.session.get('admin_email')
    print(mail)
    prod=Product.get_all_products_of_admin(mail)
    catg=Category.get_all_category()
    return render(request,'./admin_area/admin_product.html',{"products":prod,"categories":catg})

def addProduct(request):
    if request.method=="GET":
        allCat=Category.get_all_category()
        return render(request,'./admin_area/add_product.html',{"Allcat":allCat})

    if request.method== "POST":
        man_id=request.session.get('admin_email')
        name=request.POST.get('p_name')
        price=request.POST.get('price')
        instock=request.POST.get('instock')
        cat_id=request.POST.get('category')
        img1=request.FILES.get('image1')
        img2=request.FILES.get('image2')
        img3=request.FILES.get('image3')
        description=request.POST.get('description')
        allCat=Category.get_all_category()
        print(name,cat_id,price,instock,description,img1,img2,img3,man_id,)
        product=Product(name=name,price=price,instock=instock,
                    category=Category(id=cat_id),img1=img1,img2=img2,img3=img3,
                    desc=description,manufacturer=man_id)
        product.save()
        return render(request,'./admin_area/add_product.html',{"Allcat":allCat})

def editProduct(request):
    if request.method=="GET":
        allCat=Category.get_all_category()
        prd_id=request.GET.get('prod_id')
        prod=Product.get_all_products_by_prd_id(prd_id)
        
        return render(request,'./admin_area/edit_product.html',{"Allcat":allCat,"products":prod})
    if request.method=="POST":
        prd_id=request.GET.get('prod_id')
        prod=Product.get_all_products_by_prd_id(prd_id)
        man_id=request.session.get('admin_email')
        name=request.POST.get('p_name')
        price=request.POST.get('price')
        instock=request.POST.get('instock')
        cat_id=request.POST.get('category')
        img1=request.FILES.get('image1')
        img2=request.FILES.get('image2')
        img3=request.FILES.get('image3')
        description=request.POST.get('description')
        allCat=Category.get_all_category()
        print(name,cat_id,price,instock,description,img1,img2,img3,man_id,)
        prod.update(name=name,price=price,instock=instock,
                    category=Category(id=cat_id),img1=img1,img2=img2,img3=img3,
                    desc=description,manufacturer=man_id)
        return redirect('editProduct')

def addCategory(request):
    if request.method=="GET":
        return render(request,"./admin_area/add_category.html")
    if request.method=="POST":
        cname=request.POST.get('c_name')
        newcat=Category(name=cname)
        newcat.save()
        return redirect('adminProduct')    

def editCategory(request):
    if request.method=="GET":
        c_id=request.GET.get('cat_id')
        catg=Category.get_cat_by_id(c_id)
        return render(request,"./admin_area/edit_category.html",{'category':catg})

    if request.method=="POST":
        c_id=request.GET.get('cat_id')
        catg=Category.get_cat_by_id(c_id)
        name1=request.POST.get('c_name')
        catg.update(name=name1)
        return redirect('adminProduct')

   

def deleteProduct(request):
    prd_id=request.GET.get('prod_id')
    Product.delete_by_id(prd_id)
    return redirect('adminProduct')


def deleteCat(request):
    cat_id=request.GET.get('cat_id')
    print(cat_id)
    Category.delete_by_id(cat_id)
    return redirect('adminProduct')


def adminOrder(request):
    mail=request.session.get('admin_email')
    #order=Order.get_all_order_of_admin(mail)
    return render(request,'./admin_area/admin_order.html',{'order':order})


def logout(request):
    request.session.clear()
    return redirect('login')
