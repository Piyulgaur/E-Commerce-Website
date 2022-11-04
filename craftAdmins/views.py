from itertools import product
from django.shortcuts import render,redirect
from .models import Category, Product,Admin,Order
from craft.models import UserOrder
from craft.models import Customer
from django.contrib.auth.hashers import make_password,check_password

# Create your views here.
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
        gst=request.POST.get('gst')
        admin=Admin(name=name,email=email,
                        phone=phone,password=password,
                        address=addr,gst=gst)
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
    if request.session.get('admin_email'):
        email=request.session.get('admin_email')
        user=Admin.get_admin_by_email(email=email)
        print(user)
        return render(request,'./admin_area/admin_profile.html',{"users":user})

    else:
        return redirect('adminLogin')

def editAdminAccount(request):
    if request.method=="GET" :
        if request.session.get('admin_email'):
            email=request.session.get('admin_email')
            user=Admin.get_admin_by_email(email=email)
            print(user)
            return render(request,'./admin_area/edit_admin_profile.html',{"users":user})
        else:
            return redirect('adminLogin')

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
                customer1.update(name=name1,phone=phone1,address=addr,email=mail,gst=gstin)
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
    if request.session.get('admin_email'):
        mail=request.session.get('admin_email')
        print(mail)
        prod=Product.get_all_products_of_admin(mail)
        catg=Category.get_all_category()
        return render(request,'./admin_area/admin_product.html',{"products":prod,"categories":catg})
    else:
        return redirect('adminLogin')

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
        return redirect('adminProduct')

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
        return redirect('adminProduct')

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

def confirmDelivery(request):
    p_id=request.GET.get('p_id')
    prod=Order.get_all_ord_by_ord_id(p_id)
    if prod[0].status !="Delivered":
        UserOrder.deleteorder(p_id)
    prod.update(status="Delivered")
    
    return redirect('adminOrder')




def adminOrder(request):
    mail=request.session.get('admin_email')
    order=Order.get_all_order_of_admin(mail)
    print(order)
    return render(request,'./admin_area/admin_order.html',{'order':order})




