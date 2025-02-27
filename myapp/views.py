from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from myapp.models import CustomUser

def homepage(request):
    data = Categories.objects.all()
    return render(request, 'homepage.html', {'data': data})

def signup(request):
    data=" "
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')

        if CustomUser.objects.filter(username=username).exists():
            data="Username already taken. Choose a different one."
            return render(request,'signup.html',{'data':data})
        
        if CustomUser.objects.filter(email=email).exists():
            data="Username already exists. Choose a different one."
            return render(request,'signup.html',{'data':data})
        
        user = CustomUser.objects.create_user(username=username, email=email, password=password1)
        user.save()
        return redirect('login')  
    
    return render(request, 'signup.html',{'data':data})

def login_user(request):
    data=""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', 'myapp:homepage'))
        else:
            data="Invalid username or password"
            return render(request, 'login.html', {'data': data})
    
    return render(request, 'login.html',{'data':data})

def logout_user(request):
    logout(request)
    return render(request,'homepage.html')


def cartPage(request):
    if request.user.is_authenticated:
        data = cart.objects.filter(user=request.user)  
        total_items = sum(item.number for item in data)

        if not data:
            return render(request, 'cart.html', {'data': data, 'subtotal': 0, 'discount': 0, 'shipping': 0, 'totalprice': 0})

   
        subtotal = sum(item.price * item.number for item in data)

    
        total_discount = sum((item.price * item.number * item.product.Discount / 100) for item in data)

    
        discounted_price = subtotal - total_discount

        shipping = 50  
        totalprice = discounted_price + shipping  

        return render(request, 'cart.html', {
            'data': data,
            'total_items': total_items,
            'subtotal': subtotal,
            'discount': total_discount,
            'shipping': shipping,
            'totalprice': totalprice
        })
    else:
        return redirect('login')


@login_required(login_url='signup')
def orders(request):
    user_orders = Orders.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': user_orders})

def milkshakes(request):

    data = products.objects.filter(Category='milkshakes')
    cart_items = cart.objects.values_list('product_id', flat=True)
    return render(request, 'milkshakes.html', {'data': data, 'cart_items': cart_items})

def fruitjuices(request):
    data = products.objects.filter(Category='fruitjuices')
    cart_items = cart.objects.values_list('product_id', flat=True)
    return render(request, 'fruitjuices.html', {'data': data, 'cart_items': cart_items})

def hotbeverages(request):
    data = products.objects.filter(Category='hotbeverages')
    cart_items = cart.objects.values_list('product_id', flat=True)
    return render(request, 'hotbeverages.html', {'data': data, 'cart_items': cart_items})

def softdrinks(request):
    data = products.objects.filter(Category='softdrinks')
    cart_items = cart.objects.values_list('product_id', flat=True)
    return render(request, 'softdrinks.html', {'data': data, 'cart_items': cart_items})


def energydrinks(request):
    data = products.objects.filter(Category='energydrinks')
    cart_items = cart.objects.values_list('product_id', flat=True)
    return render(request, 'energydrinks.html', {'data': data, 'cart_items': cart_items})

def mocktails(request):
    data = products.objects.filter(Category='mocktails')
    cart_items = cart.objects.values_list('product_id', flat=True)
    return render(request, 'mocktails.html', {'data': data, 'cart_items': cart_items})

def beers(request):
    data = products.objects.filter(Category='beers')
    cart_items = cart.objects.values_list('product_id', flat=True)
    return render(request, 'beers.html', {'data': data, 'cart_items': cart_items})

def wines(request):
    data = products.objects.filter(Category='wines')
    cart_items = cart.objects.values_list('product_id', flat=True)
    return render(request, 'wines.html', {'data': data, 'cart_items': cart_items})

def addToCart(request, id):
    if request.user.is_authenticated:
        product = products.objects.get(id=id)
        cart.objects.create(
            user=request.user,  
            product=product, 
            image=product.image,  
            price=product.productPrice
        )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect('login')  

def update_cart(request):
    if request.method == "POST":
        prod_id = request.POST.get('prod_id') 
        action = request.POST.get('action')
        cart_item = cart.objects.get(id=prod_id)  
        if action == "+":
            cart_item.number += 1
        elif action == "-" and cart_item.number > 1:
            cart_item.number -= 1
        cart_item.save() 
        return redirect('myapp:cartpage') 

def delete_item(request):
    if request.method == "POST":
        prod_id = request.POST.get('prod_id')
        cart_item = cart.objects.get(id=prod_id)
        cart_item.delete() 
        return redirect('myapp:cartpage')

def place_order(request):
    if request.user.is_authenticated:
        user_cart = cart.objects.filter(user=request.user)  

        if not user_cart:
            return redirect('myapp:cartpage')  
        
        for item in user_cart:
            Orders.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.number,
                price=item.price * item.number,
            )
        user_cart.delete()
        
        return redirect('myapp:orders')  
    else:
        return redirect('login')  

def offer_milk(request,d):
    data = products.objects.filter(Discount=d)
    cart_items = cart.objects.values_list('product_id', flat=True)
    return render(request,'offer_milk.html',{"data":data, 'cart_items': cart_items})