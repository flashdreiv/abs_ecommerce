from django.shortcuts import render,redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from store.models import Order,OrderItem
from django.http import JsonResponse
from . decorators import admin_only
from datetime import datetime,timedelta
from django.contrib import messages
from . chart_generation import get_chart_data
import json
# Create your views here.

@login_required
@admin_only
def index(request):
    customer = request.user.customer
    if request.user.is_superuser:
        order = Order.objects.filter(complete=True).order_by('-date_ordered')
        new_orders = order.filter(status=None).count()
        total_deliveries = order.filter(status='4').count()
        cancelled = order.filter(status='5').count()
    else:
        raise PermissionDenied
    context = {
        'orders':order,
        'new_orders':new_orders,
        'total_deliveries':total_deliveries,
        'cancelled':cancelled
    }

    return render(request,'dashboard/dashboard.html',context)
@login_required
@admin_only
def details(request,type):
    order = None
    if type == 'new':
        order = Order.objects.filter(complete=True,status=None)
    elif type == 'due':
        order = Order.objects.filter(complete=True,date_ordered=datetime.now()+timedelta(days=7)).exclude(status='4')
    elif type == 'deliveries':
        order = Order.objects.filter(complete=True,status = '4')
    elif type == 'cancelled':   
        order = Order.objects.filter(complete=True,status = '5')
        print(order)



    context = {
        'orders':order
    }
    return render(request,'dashboard/card_detail.html',context)

def update_orders(request,pk):
   order = Order.objects.get(pk=pk)
   status = Order.status_list
   items = order.orderitem_set.all()
   
   if request.method == "POST":
       order_status = request.POST.get('orderstatus')
       order.status = order_status
       order.save()
       messages.success(request,'Update successful')
       return redirect('dashboard')
   context = {
       'order': order,
       'items':items,
       'status':status
   }
   return render(request,'dashboard/update_order.html',context)


@login_required
@admin_only
def get_data_chart(request):
    orders = Order.objects.filter(complete=True,status='4',date_ordered__gte=datetime.now()-timedelta(days=15)).order_by('date_ordered')
    daily_orders = get_chart_data(orders,'daily')
    if request.method == "POST":
        timeseries = json.loads(request.body.decode("utf-8"))['timeseries']
        daily_orders = get_chart_data(orders,timeseries)

    data = {
        'orders':daily_orders
    }
    return JsonResponse(data,safe=False)