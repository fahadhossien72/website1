from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('custom/<str:pk_test>/', views.custom, name='custome'),


    path('createOrder/<str:pk>/', views.createOrder, name='createOrders'),
    path('updateOrder/<str:pk>/', views.updateOrder, name='updateOrder'),
    path('deleteOrder/<str:pk>/', views.deleteOrder, name='deleteOrder'),

    path('login/',views.loginform, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('register/', views.registerform, name='register'),
    path('user/', views.loginpage, name='user'),
    path('account/', views.accountSettings, name='account'),


]
