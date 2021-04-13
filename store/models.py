from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
import random
from django.core.validators import RegexValidator

# Create your models here.



class Customer(models.Model):
    phone_regex = RegexValidator(regex = r'^\+?1?\d{0,9}$',message = "Phone number must be in a pattern of +63")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=200,null=True,blank=True)
    province = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    mobile_number = models.CharField(max_length=12,null=True,blank=True,unique=True,validators=[phone_regex])

class SmsCode(models.Model):
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE,null=True,blank=True)
    code = models.CharField(max_length=5,null=True,blank=True)

    def __str__(self):
        return self.code
    
    def save(self,*args,**kwargs):
        number_list = [x for x in range(10)]
        code_items = []

        for i in range(5):
            num = random.choice(number_list)
            code_items.append(num)
        
        code_string = "".join(str(item) for item in code_items)
        self.code = code_string
        super().save(*args,**kwargs)
    

class Product(models.Model):
    cat_list = (
        ('1','Grower'),
        ('2','Pre-lay')
    )
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200,choices=cat_list)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)

    @property
    def imgURL(self):
        url = ''
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    status_list = (
        ('1','Order confirmed'),
        ('2','Picked by courier'),
        ('3','On the way'),
        ('4','Delivered'),
        ('5','Cancelled'),
    )
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True,unique=True)
    status = models.CharField(max_length=80,blank=True,null=True,choices=status_list)

    @property
    def get_cart_items(self):
        total = 0
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_cart_total(self):
        total = 0
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    def __str__(self):
        return self.transaction_id

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True,validators=[MinValueValidator(0)])
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
class DeliveryInfo(models.Model):
    province_list = (('1','Isabela'),('2','Something'))
    city_list = (('1','Santiago'),('2','Quirino'))
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200,null=True)
    mobile_number = models.CharField(max_length=12,null=True)
    province = models.CharField(max_length=200,null=True,choices=province_list)
    city = models.CharField(max_length=200,null=True,choices=city_list)
    zipcode = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
        



