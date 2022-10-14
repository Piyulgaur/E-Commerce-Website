from urllib import request
from django.http import HttpResponse
from django.shortcuts import render
from .models import Product

def homePage(request):
    return render(request,"index.html")

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


