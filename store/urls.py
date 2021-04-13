
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.store,name="store"),
    path('product/<int:pk>', views.product,name="product"),
    path('cart/', views.cart,name="cart"),
    path('checkout/', views.checkout,name="checkout"),
    path('add_to_cart/<int:pk>', views.add_to_cart,name="add-to-cart"),
    path('update_cart/<int:pk>', views.update_cart,name="update-cart"),
    path('process_order', views.process_order,name="process-order"),
    path('orders/', views.track_order,name="track-order"),
    path('sms_verification/<str:type>', views.account_verification,name="sms-verification"),

    
]