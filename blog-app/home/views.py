from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from .models import BlogPost,Comment
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, BlogPostForm
from django.views.generic import UpdateView
from django.contrib import messages
from django.contrib.auth import login as p_login
from django.contrib.auth import logout as p_logout
from .models import BlogPost

import logging

# Get the logger instance
logger = logging.getLogger(__name__)

# Use the logger to log messages
logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')

def blogs(request):    
    posts = BlogPost.objects.filter().order_by('-dateTime')
    logger.info('Info message')
    return render(request, "blog.html", {'posts':posts})

def blogs_comments(request, slug):
    post = BlogPost.objects.filter(slug=slug).first()    
    comments = Comment.objects.filter(blog=post)
    if request.method=="POST":
        user = request.user
        content = request.POST.get('content','') 
        comment = Comment(user = user, content = content, blog=post)
        comment.save()
        logger.info('Info message')
    return render(request, "blog_comments.html", {'post':post, 'comments':comments})

def delete_blog_post(request, slug):
    posts = BlogPost.objects.get(slug=slug)
    if request.method == "POST":
        posts.delete()
        return redirect('/')
    return render(request, 'delete_blog_post.html', {'posts':posts})

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        blogs = BlogPost.objects.filter(title__contains=searched)
        logger.info('Info message')
        return render(request, "search.html", {'searched':searched, 'blogs':blogs})
    else:
        logger.info('Info message')
        return render(request, "search.html", {})

@login_required(login_url = '/login')
def add_blogs(request):
    data = BlogPost.objects.all()
    context = {
        'data': data
    }
    if request.method=="POST":
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():         
                      
            blogpost = BlogPost()
            blogpost.title=request.POST.get('title')
            blogpost.slug=request.POST.get('slug')
            blogpost.content=request.POST.get('content')
            binaryimage = request.FILES['image']
            blogpost.image_data = binaryimage.read()            
            blogpost.author = request.user
            blogpost.save()

            obj = form.instance
            alert = True

            return render(request, "add_blogs.html",{'obj':obj, 'alert':alert})
    else:
        form=BlogPostForm()
    return render(request, "add_blogs.html", {'form':form})

class UpdatePostView(UpdateView):
    model = BlogPost
    template_name = 'edit_blog_post.html'
    fields = ['title', 'slug', 'content', 'image']


def user_profile(request, myid):
    post = BlogPost.objects.filter(id=myid)
    return render(request, "user_profile.html", {'post':post})

def profile(request):
    return render(request, "profile.html")

def edit_profile(request):
    try:
        profile = request.user.profile
    except profile.DoesNotExist:
        profile = profile(request.user)
    if request.method=="POST":
        form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            alert = True
            return render(request, "edit_profile.html", {'alert':alert})
    else:
        form=ProfileForm(instance=profile)
    return render(request, "edit_profile.html", {'form':form})


def register(request):
    if request.method=="POST":   
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')
        
        user = User.objects.create_user(username, email, password1)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request, 'login.html')   
    return render(request, "register.html")

def login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            p_login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials")
        return render(request, 'blog.html')   
    return render(request, "login.html")

def logout(request):
    p_logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/login')