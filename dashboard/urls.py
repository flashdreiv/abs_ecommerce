from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="dashboard"),
    path('details/<str:type>',views.details,name="details"),
    path('chart_data/',views.get_data_chart,name="chart-data"),
    path('update/order/<int:pk>',views.update_orders,name="update-order"),
]