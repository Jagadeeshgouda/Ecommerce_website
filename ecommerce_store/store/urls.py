
from django.urls import path,include
from . import views  
from . views import *    
from django.contrib.auth.views import LoginView              
urlpatterns=[
    path("dashboard",views.dashboard,name="dashboard"),
    path("<int:id>",views.product_details,name="product_details"),  
    path("login",views.login_form,name="login"),     
    path('accounts/login/' ,LoginView.as_view(template_name="html/login.html"),name='login'),        
    path('logout',views.logout_form,name="logout") ,        
    path('verify/',views.verifyUser,name="verify"),
    path('success/',views.success,name="success"),
    path('home',views.dashboard,name='home'),
    path('search',views.SearchResultsView.as_view(),name="search_results"), 
    path("",views.createUser,name="signup"),   
    path('add_to_cart/',views.add_to_cart,name="add_to_cart") ,     
    path("increment_cart/<int:cart_id>/",views.increment_cart, name="increment_cart"), 
    path('decrement_cart/<int:cart_id>/',views.decrement_cart,name="decrement_cart")  ,  
    path('cart/',views.cart,name="cart"),  
    path('remove_from_cart/<int:cart_id>/',views.remove_from_cart,name="remove_from_cart"),   
    path("checkout/",views.checkout,name="checkout"),  
    path('changepassword',views.changepassword),
    path('index', views.homepage, name='index'),
	path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    # path('execute_payment/', execute_payment, name='execute_payment'),
    # path('cancel_payment/', cancel_payment, name='cancel_payment'),
    ]  