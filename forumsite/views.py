from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post,Comment
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from .forms import EmailPostForm,CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
# Create your views here.


def post_list(request, tag_slug=None):
  post_list = Post.published.all()
  tag = None
  if tag_slug:
    tag = get_object_or_404(Tag,slug=tag_slug)
    post_list = post_list.filter(tags__in=[tag])
  paginator = Paginator(post_list,6) #3 posts per page
  page_number = request.GET.get('page',1)
  try:
    posts = paginator.page(page_number)
  except PageNotAnInteger:
    posts = paginator.page(1) #deliver first page is page is not an integer
  except EmptyPage:
    posts = paginator.page(paginator.num_pages) #always return last page if not page number is found
  return render(request,'forumsite/post/list.html',{'posts':posts,'tag':tag})


# class based view
# class PostListView(ListView):
#   queryset = Post.published.all()
#   context_object_name = 'posts'
#   paginate_by=3
#   template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
  post = get_object_or_404(Post,status =Post.Status.PUBLISHED,
                          slug=post,publish__year = year, publish__month=month,
                          publish__day=day)
  comments = post.comments.filter(active=True)
  form = CommentForm()
  return render(request,'forumsite/post/detail.html',{'post':post,'comments':comments,'form':form})
  
def post_share(request,post_id):
  post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
  sent = False
  if request.method =='POST':
    form = EmailPostForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      post_url = request.build_absolute_uri(post.get_absolute_url())
      subject = f"{cd['name']} recommends you read {post.title}"
      message = f"Read {post.title} at {post_url} {cd['name']}\'s comments: {cd['comments']}"
      send_mail(subject,message,"matthewofomi2015@gmail.com",[cd['to']])
      sent = True
  else:
      form = EmailPostForm()
  return render(request,'forumsite/post/share.html',{'post':post,'form':form,'sent':sent})

@require_POST
def post_comment(request,post_id):
  post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
  comment = None
  form = CommentForm(data=request.POST)
  if form.is_valid():
    comment = form.save(commit=False)
    comment.post = post
    comment.save()
  return render(request,'forumsite/post/comment.html',{'post':post,'form':form,'comment':comment})