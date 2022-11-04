from django.contrib import admin
from craftAdmins.models import Product,Category,Admin,Order



class AdminProduct(admin.ModelAdmin):
    list_display=['name','price','category']

class AdminCategory(admin.ModelAdmin):
    list_display=['name']



class AdminUser(admin.ModelAdmin):
    list_display=['name','email','address']

class AdminOrder(admin.ModelAdmin):
    list_display=['product','customer','date']

class AdminuserOrder(admin.ModelAdmin):
    list_display=['productName','customer','order_date']



# Register your models here.
admin.site.register(Product,AdminProduct)
admin.site.register(Category,AdminCategory)
admin.site.register(Order,AdminOrder)
admin.site.register(Admin,AdminUser)
