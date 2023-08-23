from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse_lazy

urlpatterns = [

    path("",views.home, name="home"),
    path("product/",views.product, name="product"),
    path("customer/<str:pk_c_id>/",views.customer, name="customer"),
    path("login",views.loginPage, name = "login"),
    path("logout",views.logoutUser, name="logout"),
    path("register",views.registerPage, name = "register"),
    path("user", views.userPage, name="user-page"),
    path('account/', views.accountSettings, name="account"),
    path("create_order/<str:pk_c_id>",views.createOrder, name="createorder"),
    path("update_order/<str:pk_u_id>",views.updateOrder, name="updateorder"),
    path("delete_order/<str:pk_d_id>",views.deleteOrder, name="deleteorder"),
    
    path('reset_pasword/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('reset_pasword_sent/', auth_views.PasswordResetDoneView.as_view(), name="reset_password_done"),
    path('reset/<uidb64>/<tocken>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_pasword_compelete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete")

]