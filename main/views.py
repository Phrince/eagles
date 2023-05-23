from distutils.log import info
from msilib.schema import Feature
from multiprocessing import context
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import logout, login,authenticate,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from .forms import *
from .models import *

# Create your views here.
def homepage(request):
    popular = product.objects.filter(popular=True)
    featured = product.objects.filter(featured=True)
    
    context = {
        'popular':popular,
        'featured':featured
    }
    
    return render(request, 'index.html', context)

def Product(request):
    prod = product.objects.all()
    p = Paginator(prod, 8)
    page = request.GET.get('page')
    pagin = p.get_page(page)
    
    context = {
        'pagin':pagin,
    }
    
    return render(request, 'Product.html', context)

def category(request, id):
    catname = Category.objects.get(pk=id)
    catprod = product.objects.filter(type_id=id)
    
    context = {
        'catname':catname,
        'catprod':catprod
    }
    
    return render(request, 'category.html', context)

def detail(request, id, slug):
    fdet = product.objects.get(pk=id)
    fsize = Size.objects.all()
    
    context = {
        'fdet':fdet,
        'fsize':fsize
    }
    
    return render(request, 'detail.html', context)

def search(request):
    if request.method == 'POST':
        item = request.POST['item']
        search_item = Q(Q(name__icontains=item)| Q(description__icontains=item))
        search = product.objects.filter(search_item)
        
        context = {
            'search':search,
            'item':item
        }
        
        return render(request, 'search.html', context)

def contact(request):
    contact = ContactForm()
    if request.method == 'POST':
        contact = ContactForm(request.POST)
        if contact.is_valid():
            contact.save()
            messages.success(request, 'your message is sent successfully')
            return redirect('home')
        
        
    context = {
            'contact':contact
    }
        
    return render(request, 'contact.html', context)

def signout(request):
    logout(request)
    messages.success(request, 'you are now logged out')
    return redirect('home')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'you are now signed in')
            return redirect('home')
        else:
            messages.info(request, 'username/password is incorrect')
            return redirect('signin')
    return render(request, 'signin.html')

def signup(request):
    customer = CustomerForm()
    if request.method == 'POST':
        phone = request.POST['phone']
        address = request.POST['address']
        pix = request.POST['pix']
        customer = CustomerForm(request.POST)
        if customer.is_valid():
            user = customer.save()
            newuser = Customer()
            newuser.user = user
            newuser.first_name = user.first_name
            newuser.last_name = user.last_name
            newuser.email = user.email
            newuser.phone = phone
            newuser.address = address
            newuser.pix = pix
            newuser.save()
            messages.success(request, f'dear {user} your account is created successfully')
            return redirect('home')
        else:
            messages.error(request, customer.errors)
            return redirect('signup')
        
    return render(request, 'signup.html')
          
def profile(request):
    userprof =  Customer.objects.get(user__username = request.user.username)
    
    
    context = {
        'userprof':userprof
    }
    
    return render(request,'profile.html',context)

def profile_update(request):
    userprof = Customer.objects.get(user__username = request.user.username)
    profile =ProfileUpdateForm(instance=request.user.customer)
    if request.method == 'POST':
        profile = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.customer)
        if profile.is_valid():
            pupdate = profile.save()
            new = pupdate.first_name.title()
            messages.success(request, f'dear {new} your profile update is successful')
            return redirect('profile')
        else:
            new = pupdate.first_name.title()
            messages.error(request, f'dear {new} your profile update generated the following errors: {profile.errors}')
            return redirect('profile_update')
        
    context = {
        'userprof':userprof
    }
    
    return render(request, 'profile_update.html', context)

def password_update(request):
    userprof = Customer.objects.get(user__username = request.user.username)
    passupdate = PasswordChangeForm(request.user)
    if request.method == 'POST':
        new = request.user.username.title()
        passupdate = PasswordChangeForm(request.POST, request.user)
        if passupdate:
            update_session_auth_hash(request, passupdate)
            messages.success(request, f'dear {new} your password is updated successfully')
            return redirect('profile')
        else:
            messages.error(request, f'the following errors occured: {passupdate.errors}')
            return redirect('password_update')
        
    context = {
        'userprof':userprof,
        'passupdate':passupdate
    }
    
    return render(request, 'password_update.html', context)

def add_to_cart(request):
    if request.method == 'POST':
        item = request.POST['itemid']
        quantity = int(request.POST['quantity'])
        Product = product.objects.get(pk=item)
        cart = Cart.objects.filter(user__username = request.user.username, paid=False)
        if cart:
            basket = Cart.objects.filter(user__username = request.user.username, product=Product.id, price=Product.price, quantity=quantity,paid=False).first()
            if basket:
                basket.quantity += quantity
                basket.amount = Product.price * basket.quantity
                basket.save()
                messages.success(request, 'one item added to cart')
                return redirect('home')
            else:
                newitem = Cart()
                newitem.user = request.user 
                newitem.product = Product
                newitem.price = Product.price
                newitem.quantity = quantity
                newitem.amount = Product.price * quantity
                newitem.paid = False
                newitem.save()
                messages.success(request, 'one item added to cart')
                return redirect('home')
        else:
           newitem = Cart()
           newitem.user = request.user 
           newitem.product = Product
           newitem.price = Product.price
           newitem.quantity = quantity
           newitem.amount = Product.price * quantity
           newitem.paid = False
           newitem.save()
           messages.success(request, 'one item added to cart')
           return redirect('home')
       
def cart(request):
    cart = Cart.objects.filter(user__username = request.user.username)
    for item in cart:
        item.amount = item.price * item.quantity
        item.save()
        
        subtotal = 0
        vat = 0
        total = 0
        
        for item in cart:
            subtotal += int(item.amount)
            vat = 0.075 * subtotal
            total = subtotal + vat
    
    context = {
        'cart':cart,
        'subtotal':subtotal,
        'vat':vat,
        'total':total
    }
    
    return render(request, 'cart.html', context)

def delete(request):
    if request.method == 'POST':
        delid = request.POST['delid']
        Cart.objects.get(pk=delid).delete()
        messages.success(request, 'item removed')
        return redirect('cart')
    
def update(request):
    if request.method == 'POST':
        itemid = request.POST['itemid']
        quant = request.POST['quant']
        newquant = Cart.objects.get(pk=itemid)
        newquant.quantity = quant
        newquant.amount = newquant.price * newquant.quantity
        newquant.save()
        messages.success(request, 'quantity added')
        return redirect('cart')
    
def checkout(request):
    userprof = Customer.objects.get(user__username = request.user.username)
    cart = Cart.objects.filter(user__username = request.user.username)
    for item in cart:
        item.amount = item.price * item.quantity
        item.save()
        
        subtotal = 0
        vat = 0
        total = 0
        
        for item in cart:
            subtotal += int(item.amount)
            vat = 0.075 * subtotal
            total = subtotal + vat
    
    context = {
        'cart':cart,
        'userprof':userprof,
        'total':total
    }
    
    return render(request, 'checkout.html', context)

             