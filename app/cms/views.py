from django.shortcuts import render, redirect
from .models import Post

def index(request):
    posts = Post.objects.filter(status="publish")
    return render(request, 'cms/index.html', {'posts': posts})

def post(request, post_id):
    post = Post.objects.get(pk = post_id, status="publish")
    return render(request, 'cms/view.html', {'post_id': post_id, 'post': post})

def post_tags(request, tag):
    posts = Post.objects.filter(tags__name__in=[tag], status="publish")
    return render(request, 'cms/post_tags.html',{'posts': posts})
