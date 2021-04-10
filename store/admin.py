from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(Customer)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price']
    list_filter = ['category']

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(DeliveryInfo)