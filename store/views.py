from django.shortcuts import render,redirect
from . models import *
import json
from django.http import JsonResponse
from django.core.paginator import Paginator,EmptyPage
from django.contrib import messages
import uuid
from django.db.models import F
from . forms import CheckOutForm,CodeForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .decorators import unverified_user

# Create your views here.
# @login_required
def store(request):
    products = Product.objects.order_by('-name')
    categories = Product.cat_list
    cartItems = 0
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(customer=customer,complete=False)
            cartItems = order.get_cart_items
        except:
            cartItems = 0
    else:
        pass
        

    page_num  = request.GET.get('page',1)
    paginator = Paginator(products,8)

    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = paginator.page(1)
    
    
    context = {
        'products':page,
        'categories':categories,
        'pages':page,
        'cartTotal':cartItems
    }
    return render(request,'store/index.html',context)

# @login_required
# @unverified_user
def product(request,pk):
    if request.user.is_authenticated:
        customer = request.user.customer

    product = Product.objects.get(pk=pk)
    featured_products = Product.objects.filter(category = product.category)
    try: 
        cartItems = Order.objects.get(customer=customer,complete=False).get_cart_items
    except:
        cartItems = 0
    context = {
        'product':product,
        'featured':featured_products[:3],
        'cartTotal':cartItems
    }

    return render(request,'store/product.html',context)
@login_required
# @unverified_user
def add_to_cart(request,pk):
    if request.user.is_authenticated:
        if request.method=="POST":
            product = Product.objects.get(pk=pk)
            customer = request.user.customer
            order,created = Order.objects.get_or_create(customer=customer,complete=False)
            orderItem,created = OrderItem.objects.get_or_create(product=product,order=order)
            orderItem.quantity = F('quantity') + request.POST.get('quantity')
            orderItem.save()
            cartTotal = order.get_cart_items
        else:
            return redirect('store')

    return JsonResponse(cartTotal,safe=False)


@login_required
# @unverified_user
def cart(request):
    customer = request.user.customer
    try:
        order = Order.objects.get(customer=customer,complete=False)
        cartItems = order.get_cart_items
        total_amount = order.get_cart_total
        orderItem = OrderItem.objects.filter(order=order)
    except:
        cartItems = 0
        total_amount = 0 
        orderItem = {}

    context = {
        'cartTotal':cartItems,
        'total_amount':total_amount,
        'products':orderItem

    }
    return render(request,'store/cart.html',context)

@login_required
# @unverified_user
def update_cart(request,pk):   
    if request.method == 'POST':
        customer = request.user.customer
        order = Order.objects.get(customer=customer,complete=False)
        orderItem,create = OrderItem.objects.get_or_create(product__id=pk,order=order)
        action = request.POST.get('action')
        quantity = request.POST.get('quantity')
        if(action=='add'):
            orderItem.quantity = F('quantity') + quantity
        elif(action=='remove'):
            orderItem.quantity = F('quantity') - quantity
        elif(action=='delete'):
            orderItem.quantity = 0
        
        

        orderItem.save()
        orderItem.refresh_from_db()

        cartItems = order.get_cart_items
        cartTotal = order.get_cart_total
    
        qty = orderItem.quantity
        if qty <= 0:
            orderItem.delete()
    else:
        raise PermissionDenied

    
    data = {
        'cartItems':cartItems,
        'orderQty':qty,
        'cartTotal':cartTotal
    }
    
    return JsonResponse([cartItems,qty,cartTotal],safe=False)
@login_required
# @unverified_user
def checkout(request):
    form = CheckOutForm()
    if request.user.is_authenticated:
        customer = request.user.customer
        try:
            order = Order.objects.get(customer=customer,complete=False)
            cartItems = order.get_cart_items
            total_amount = order.get_cart_total
            orderItem = OrderItem.objects.filter(order=order)
        except:
            cartItems = 0
            total_amount = 0 
            orderItem = {}


    context = {
        'cartTotal':cartItems,
        'total_amount':total_amount,
        'orders':orderItem,
        'form':form

    }
    return render(request,'store/checkout.html',context)


@login_required
# @unverified_user
def process_order(request):
    
    if request.method == "POST":
        if request.user.is_authenticated:
            customer = request.user.customer
            order = Order.objects.get(customer=customer,complete=False)
        form = CheckOutForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.order = order
            instance.customer = customer
            order.complete=True
            order.transaction_id = order.id + 100000
            order.save()
            instance.save()
            print('saved!')
        else:
            return JsonResponse('Error saving',safe=False)
        
    return redirect('store')

@login_required
# @unverified_user
def track_order(request):
    orders = {}
    order = 0
    cartTotal = 0
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            orders = Order.objects.filter(customer=customer,complete=True).order_by('-date_ordered')
            order = Order.objects.get(customer=customer,complete=False)
            cartTotal = order.get_cart_items
        except:
            pass

    page_num  = request.GET.get('page',1)
    paginator = Paginator(orders,2)

    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = paginator.page(1)
                

    context = {
        'orders':page,
        'cartTotal':cartTotal,
        'pages':page
    }
    return render(request,'store/track_order.html',context)

@login_required
#add security on bruteforcing numbers
def account_verification(request,type):
    customer = request.user.customer
    smscode = customer.smscode.code
    form = CodeForm()
    if request.method == "POST":
        if(type=="resend"):
            pass
        if(type=="new"):
            form = CodeForm(request.POST)
            usercode = request.POST.get('code')
            if form.is_valid():
                if(str(usercode)==smscode):
                    customer.verified = True
                    customer.save()
                    return redirect('store')
                else:
                    messages.error(request,"Invalid code")
            
            return redirect('sms-verification') 

    context = {
        'form':form
    }
    return render(request,'account/verify_sms.html',context)



