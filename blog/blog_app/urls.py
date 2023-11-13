from django.urls import path
from . import views

urlpatterns =[
    path('',views.index,name='home'),
    path('contact',views.contact,name='contact'),
    path('about',views.about_us,name='about_us'),
    path('test',view=views.test,name='test')
]