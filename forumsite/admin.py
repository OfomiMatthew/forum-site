from django.contrib import admin

# Register your models here.

from django.contrib.auth.models import User
from .models import Post, Comment

# Register your models here.



# admin.site.register() and @admin.register() performs same thing. they register a model in the django admin
#customizing the order of the django admin site
@admin.register(Post) 
class PostAdmin(admin.ModelAdmin):
  list_display = ['title','slug','author','publish','status']
  list_filter = ['status','created','publish','author']
  search_fields = ['title','body']
  prepopulated_fields = {'slug':('title',)}
  raw_id_fields = ['author']
  date_hierarchy = 'publish'
  ordering = ['status','publish']
  
  
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
  list_display =['name','email','post','created','active']
  list_filter = ['active','created','updated']
  search_fields = ['name','email','body']