from django.db import models
import datetime

# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=50)
    phone=models.CharField(max_length=15)
    email=models.EmailField()
    username=models.CharField(max_length=50,blank=True)
    password=models.CharField(max_length=500)
    address=models.CharField(max_length=500)
    
    def register(self):
        self.save()

    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True
        else:
            return False


    @staticmethod
    def get_user_by_email(email):
        try:
            return Customer.objects.get(email=email) # return one object only
        except:
            return False

    
    @staticmethod
    def get_by_id(c_id):
            return Customer.objects.filter(id=c_id) # return one object only

class UserOrder(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    productName=models.CharField(max_length=100,blank=True)
    productimg=models.ImageField(null=True,blank=True)
    quantity=models.IntegerField(default=1)
    price=models.IntegerField()
    order_date=models.DateField(default=datetime.datetime.today)
   
    def UserPlaceOrder(self):
        self.save()

    def getidOrder(id):
        return UserOrder.objects.filter(customer=id)

    def get_all_order():
        return UserOrder.objects.all()
    
    def deleteorder(id):
        record = UserOrder.objects.get(id = id)
        record.delete()
