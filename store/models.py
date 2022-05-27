from __future__ import division
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
import datetime
import os
import django.utils.timezone



from pytz import timezone
def get_file_path(request,filename):
    originalFilename=filename
    nowTime=datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename="%s%s" % (nowTime,originalFilename)
    return os.path.join('images/',filename)


class Brand(models.Model):
    brand = models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.brand
class Category(models.Model):
    brand=models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True,blank=True)
    category=models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.category
class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
    serial = models.CharField(max_length=200,null=True)
    status=models.BooleanField(default=True,null=True,blank=False)
    image = models.ImageField(null=True, blank=True,upload_to='images')
    
    def __str__(self):
        return f'{self.brand}-{self.category}-{self.serial}'
    
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url
    class Meta:
        ordering=('-id',)
    
class Receiver(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    staffid=models.CharField(max_length=10,null=True)
    name=models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.name
class Issuer(models.Model):
    #user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Order(models.Model):
    
    receiver=models.ForeignKey(Receiver,on_delete=models.SET_NULL,null=True,blank=True)
    #receiver=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    dateOrdered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False)


  
    transactionID=models.CharField(max_length=200,null=True)
    """
    receiver=models.ForeignKey(Receiver,on_delete=models.SET_NULL,null=True,blank=True)
    complete=models.BooleanField(default=False,null=True,blank=False)

    dateOrdered=models.DateTimeField(auto_now_add=True)
    #iName=models.CharField(max_length=200,null=True)
    transactionID=models.CharField(max_length=200,null=True)
    #iEmail=models.CharField(max_length=200,null=True)
    
    #rName=models.CharField(max_length=200,null=True)
    #rDivision=models.CharField(max_length=200,null=True)
    #rDepart=models.CharField(max_length=200,null=True)
    ##rLocation=models.CharField(max_length=200,null=True)
    #rPurpose=models.CharField(max_length=200,null=True)
    
    
    """
  

    def __str__(self):
        return str(self.id)
        
    @property
    def shipping(self):
        shipping=False
        orderitems=self.orderitem_set.all()
        for i in orderitems:
            if i.product.status==True:
                shipping=True

        return shipping
    
    @property
    def getCartItems(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

   
class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    dateAdded=models.DateTimeField(auto_now_add=True)

class ShippingAddress(models.Model):
    receiver=models.ForeignKey(Receiver,on_delete=models.SET_NULL,null=True)
    issuer=models.ForeignKey(Issuer,on_delete=models.SET_NULL,null=True,blank=True)

    
    division=models.CharField(max_length=200,null=True)
    dept=models.CharField(max_length=200,null=True)
    location=models.CharField(max_length=200,null=True)
    purpose=models.CharField(max_length=300,null=True)
    def __str__(self):
        return self.address

    
