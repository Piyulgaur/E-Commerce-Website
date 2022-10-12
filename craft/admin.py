from django.contrib import admin
from .models import Product, Category, Customer, Order
# Register your models here.

class AdminProduct(admin.ModelAdmin):
    list_display=['name','price','category']

class AdminCategory(admin.ModelAdmin):
    list_display=['name']

class AdminCustomer(admin.ModelAdmin):
    list_display=['name','email','address']

class AdminOrder(admin.ModelAdmin):
    list_display=['product','customer','date']



# Register your models here.
admin.site.register(Product,AdminProduct)
admin.site.register(Category,AdminCategory)
admin.site.register(Customer,AdminCustomer)
admin.site.register(Order,AdminOrder)