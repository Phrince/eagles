from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class Appinfo(models.Model):
    appname = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='logo')
    banner = models.ImageField(upload_to='banner')
    carousel1 = models.ImageField(upload_to='carousel1')
    carousel2 = models.ImageField(upload_to='carousel2')
    carousel3 = models.ImageField(upload_to='carousel3')
    
    def __str__(self):
        return self.appname
    
class Category(models.Model):
    name = models.CharField(max_length=50)
    catimg = models.ImageField(upload_to='catimg')
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
class product(models.Model):
    type = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)   
    slug = models.SlugField(unique=True)   
    img = models.ImageField(upload_to='product')   
    price = models.IntegerField() 
    description = models.TextField()
    size = models.CharField(max_length=50, blank=True, null=True)
    popular = models.BooleanField()
    featured = models.BooleanField()
    uploaded = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Size(models.Model):
    wearsize = models.CharField(max_length=20)
    
    def __str__(self):
        return self.wearsize


class Contact(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    message = models.TextField()
    sent = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.full_name
    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    email = models.EmailField(max_length=104)
    pix = models.ImageField(upload_to='profilepix')
    joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    amount = models.CharField(max_length=50)
    paid = models.BooleanField()
    
    def __str__(self):
        return self.user.username
