from django.urls import path
from . import views
from .views import reset_request_view, reset_password_view

urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('orders/', views.orders, name='accounts.orders'),
    path('password_reset/', reset_request_view, name='password_reset'),
    path('reset-password/<str:token>/', reset_password_view, name='reset_password'),
]