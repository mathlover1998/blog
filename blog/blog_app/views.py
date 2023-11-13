from django.shortcuts import render,redirect
from .models import Posts
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count



# Create your views here.
def index(request):
    posts_by_comment = Posts.objects.annotate(comment_count = Count('comments')).order_by('-comment_count')[:6]
    posts_by_time = Posts.objects.order_by('-created_at')
    
    return render(request,'index.html',{'posts_by_comment':posts_by_comment,'posts_by_time':posts_by_time})

def contact(request):
    if request.method =='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        send_mail(
            f'{subject}',
            f'From {name},\n{message}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
            )
        return redirect('contact')
    return render(request,'pages/contact.html')

def about_us(request):
    return render(request,'pages/about.html')

def test(request):
    return render(request,'test.html')