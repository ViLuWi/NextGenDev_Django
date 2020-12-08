from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .models import *
from .forms import *


def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {
        'posts': posts
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You are registered! Please login to write posts.')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {
        'form': form
    })


def edit(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save(commit=False)
            form.instance.author = request.user
            form.save()
            messages.success(request, 'Your changes were saved and updated!')
            return redirect('index')
    else:
        form = PostForm(instance=post)
    if request.user == post.author:
        return render(request, 'edit.html', {
            'form': form
        })
    else:
        messages.error(request, 'You are not the author of this post')
        return redirect('index')


def post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form.instance.author = request.user
            form.save()
            messages.success(request, 'Your post is now online!')
            return redirect('index')
    else:
        form = PostForm()
    if request.user.is_authenticated:
        return render(request, 'new-post.html', {
            'form': form
        })
    else:
        messages.error(request, 'You are not logged in! Please login first.')
        return redirect('index')


def delete(request, abc):
    post = Post.objects.get(id=abc)
    if request.user == post.author:
        post.delete()
        messages.success(request, 'Your post was deleted :(')
        return redirect('index')
    else:
        messages.error(request, 'You are not the author of this post.')
        return redirect('index')
