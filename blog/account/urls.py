from django.urls import path
from . import views

urlpatterns = [
    path('register',views.register,name='register'),
    path('log-in',views.log_in,name='log_in'),
    path('log-out',views.log_out,name='log_out'),
    path('profile',views.update_profile,name='update_profile'),
    path('change-password',views.change_password,name='change_password'),
    path('forgot-password',views.forgot_password,name='forgot_password'),
    path('reset-password/<str:token>/',views.reset_password,name='reset_password')
]