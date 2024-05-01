from django import template
from django.db.models import Count
from . .models import Post 

register = template.Library()


# we can use the function as the name for a custom tag or use the name attribute as the custom tag
@register.simple_tag(name='my_tag') 
def total_posts():
    return Post.published.count()

@register.inclusion_tag('forumsite/post/latest_posts.html')
def show_latest_posts(count=3):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

@register.simple_tag
def most_commented_posts(count=3):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
