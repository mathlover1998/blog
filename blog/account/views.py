from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from blog_app.models import Users,PasswordResetToken
from django.contrib.auth.hashers import check_password
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.core.mail import send_mail,BadHeaderError
from django.conf import settings
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)


# Create your views here.

def register(request):
    if request.method =='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        if Users.objects.filter(username = username).exists():
            messages.error(request,'This username is taken! Please login instead!')
            return redirect('log_in')
        elif Users.objects.filter(email=email).exists():
            messages.error(request,'This email is taken! Please using another email to register!')
            return redirect('register')
        elif password!= re_password:
            messages.error(request,'Confirm password must be the same with password!')
            return redirect('register')
        else:
            user = Users.objects.create_user(
                username=username, email=email, password=password)
            user.save()
            login(request,user)
            return redirect('home')
    return render(request, 'account/register.html')
    
def log_in(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username =username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            if not Users.objects.filter(username = username).exists():
                messages.error(request,'This account does not exist! Please register first!')
                return redirect('register')
            else:
                messages.error(request,'Invalid password!')
                return redirect('log_in')

    return render(request, 'account/login.html')


    

@login_required
def log_out(request):
    logout(request)
    return redirect('log_in')


@login_required
def update_profile(request):
    current_user = request.user
    if request.method == 'POST':
        new_username = request.POST.get('username')
        if Users.objects.exclude(pk=current_user.pk).filter(username=new_username).exists():
            messages.error(request, 'This username is already taken.')
        else:
            current_user.username = new_username
            image = request.FILES.get('image')
            if image:
                current_user.profile_picture = image
            current_user.first_name = request.POST.get('first_name')
            current_user.last_name = request.POST.get('last_name')
            current_user.bio = request.POST.get('bio')
            current_user.save()
            messages.success(request, 'Profile updated successfully.')
    return render(request, 'account/user-profile.html', {'current_user': current_user})



@login_required
def change_password(request):
    if request.method == 'POST':
        user = request.user
        old_password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        re_password = request.POST.get('re_password')
        if not user.check_password(old_password):
            messages.error(request, 'Incorrect old password')
        else:
            if new_password != re_password:
                messages.error(request, 'New password and confirmation do not match')
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Keep the user logged in

                messages.success(request, 'Password changed successfully')
                return redirect('change_password')

    return render(request, 'account/change-password.html')

def forgot_password(request):
    if request.method =='POST':
        email = request.POST.get('email')
        user = get_object_or_404(Users,email = email)
        token = get_random_string(length=32)
        reset_token = PasswordResetToken.objects.filter(user=user, is_used = False).first()
        if reset_token:
            reset_token.token = token
            reset_token.created_at = timezone.now()
            reset_token.save()
        else:
            PasswordResetToken.objects.create(user=user, token=token)

        reset_link = f'{settings.BASE_URL}/account/reset-password/{token}/'
        try:
            send_mail(
            'Password Reset',
            f'Click the following link to reset your password: {reset_link}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
            )
        except BadHeaderError as e:
            logger.error(f'Error occurred while sending email: {e}')
        return render(request, 'account/password-reset-sent.html')
    return render(request,'account/forgot-password.html')

def reset_password(request,token):
    reset_token = get_object_or_404(PasswordResetToken, token =token, is_used = False)
    if reset_token.created_at < timezone.now() - timezone.timedelta(hours=1):
        return render(request,'account/password-reset-expired.html')
    if request.method =='POST':
        password =request.POST.get('password')
        user = reset_token.user
        user.set_password(password)
        user.save()
        reset_token.delete()
        return render(request, 'account/password-reset-done.html')
    
    return render(request, 'account/reset-password.html')


#remember password