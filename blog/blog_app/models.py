from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django_resized import ResizedImageField


class Users(AbstractUser):
    profile_picture = ResizedImageField(size=[500, 300], upload_to='user_images/', blank=True, null=True)
    bio = models.TextField(null=True)

    class Meta:
        managed = True
        db_table = 'users'



class Categories(models.Model):
    name = models.CharField(max_length=255,null=False)
    class Meta:
        managed = True
        db_table = 'categories'

class Tags(models.Model):
    name = models.CharField(max_length=255,null=False)
    class Meta:
        managed = True
        db_table = 'tags'


class Posts(models.Model):
    title = models.CharField(max_length=255,null=False,default='')
    subtitle = models.CharField(max_length=255,null=False,default='')
    slug = models.CharField(max_length=255,null=False)
    content = models.TextField(null=False)
    author = models.ForeignKey(Users,models.CASCADE,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='blog_post_images')
    categories = models.ManyToManyField(Categories)
    tags = models.ManyToManyField(Tags)
    class Meta:
        managed = True
        db_table = 'blog_posts'



class Comments(models.Model):
    blog_post = models.ForeignKey(Posts,models.CASCADE,null=False,related_name='comments')
    author = models.ForeignKey(Users,models.CASCADE,null=False)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    parent_comment = models.ForeignKey('self',null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    
    class Meta:
        managed = True
        db_table = 'comments'
        
class PasswordResetToken(models.Model):
    user = models.OneToOneField(Users,on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self) :
        return self.user.username
    
    class Meta:
        managed = True
        db_table = 'password_reset_tokens'