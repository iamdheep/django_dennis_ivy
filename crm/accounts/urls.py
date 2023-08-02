from django.urls import path
from . import views

urlpatterns = [
    path("",views.home, name="home"),
    path("product/",views.product, name="product"),
    path("customer/<str:pk_c_id>/",views.customer, name="customer"),
    
    path("create_order/<str:pk_c_id>",views.createOrder, name="createorder"),
    path("update_order/<str:pk_u_id>",views.updateOrder, name="updateorder"),
    path("delete_order/<str:pk_d_id>",views.deleteOrder, name="deleteorder"),
]