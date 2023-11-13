from blog_app.models import Posts,Categories,Tags
from django.db.models import Count

def sidebar_data(request):
    random_posts = Posts.objects.order_by('?')[:3]
    categories = Categories.objects.annotate(post_count=Count('posts')).order_by('-post_count')[:5]
    tags = Tags.objects.annotate(tag_count=Count('posts')).order_by('-tag_count')[:5]
    return {
        'random_posts':random_posts,
        'categories':categories,
        'tags':tags
    }

