from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User ,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200 ,null=True)
    phone = models.CharField(max_length=200 ,null=True)
    email = models.CharField(max_length=200 ,null=True)
    profile_pic = models.ImageField(default="cart.png",null=True,blank=True)
    address = models.CharField(max_length=200,null=True)
    district = models.CharField(max_length=200,null=True)
    amphoe = models.CharField(max_length=200,null=True)
    province = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=200,null=True)
    date_created = models.DateTimeField(auto_now_add=True ,null=True)
    last_updated = models.DateTimeField(auto_now=True ,null=True)
    
    def __str__(self):
        return str(self.name)
          
class Tag(models.Model):
    name = models.CharField(max_length=200 ,null=True)
    
    def __str__(self):
        return self.name 

class Company(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    phone=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    added_on=models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True ,null=True)
    objects=models.Manager()
    
    def __str__(self):
        return self.name     
      
class Product(models.Model):
    CATEGORY = (
                ('Indoor', 'Indoor') ,
                ('Out Door', 'Out Door') ,
            ) 
    name = models.CharField(max_length=200 ,null=True)
    price = models.DecimalField(null=True,max_digits=7,decimal_places=2)
    category = models.CharField(max_length=200 ,null=True,choices=CATEGORY)
    description = models.CharField(max_length=200 ,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True ,null=True)
    qty=models.IntegerField(null=True)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(null=True,blank=True)
    medical_typ=models.CharField(max_length=255,null=True)
    buy_price=models.FloatField(max_length=255,null=True)
    company_id=models.ForeignKey(Company,on_delete=models.CASCADE,null=True)
    last_updated = models.DateTimeField(auto_now=True ,null=True)
    objects=models.Manager()


    def __str__(self):
        return self.name      
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
         
class Order(models.Model):
    STATUS = (
                ('Pending', 'Pending') ,
                ('Out for delivery', 'Out for delivery') ,
                ('Delivered', 'Delivered') ,
            ) 
    customer = models.ForeignKey(Customer ,null=True,on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True ,null=True)
    status = models.CharField(max_length=200 ,null=True,choices=STATUS,default='Pending')
    complete = models.BooleanField(default=False,null=True,blank=False)
    order_total_price=models.FloatField(max_length=255,null=True)
    order_total_quantity=models.FloatField(max_length=255,null=True)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    @property
    def shipping(self):
        shipping = True
        # orderitems = self.orderitem_set.all()
        return shipping
    
    @property
    def eachquan(self):
        total = self.product.price * self.quantity
        return total
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    item_total_price = models.FloatField(max_length=255,null=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
class Medicine(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    medical_typ=models.CharField(max_length=255,null=True)
    buy_price=models.FloatField(max_length=255,null=True)
    sell_price=models.FloatField(max_length=255,null=True)
    company_id=models.ForeignKey(Company,on_delete=models.CASCADE)
    description=models.CharField(max_length=255,null=True) 
    qty=models.IntegerField()
    added_on=models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True ,null=True)
    objects=models.Manager()
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(default="placeholder.png",null=True,blank=True)
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Employee(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    phone=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    joining_date=models.DateField()
    added_on=models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True ,null=True)
    objects=models.Manager()