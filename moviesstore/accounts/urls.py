from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import CustomPasswordResetForm, CustomPasswordResetView, reset_password, reset_request_view
from .views import reset_request_view, reset_password_view

urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('orders/', views.orders, name='accounts.orders'),

   # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/', reset_request_view, name='password_reset'),
    path('reset-password/<str:token>/', reset_password_view, name='reset_password'),
    #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]