from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from posts.models import Post, Comment
from posts.forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from .models import Follow
from django.contrib.auth.models import User
def home(request):
    
    return HttpResponse("<h1>Welcome to Mini Social Media Platform</h1>")
def home(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')

    else:
        form = PostForm()

    posts = Post.objects.all().order_by('?')
    return render(request, 'home.html',{
         'form': form,
        'posts': posts

    })
def register(request):
     if request.user.is_authenticated:
        return redirect('home')
     if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Registration Successful! Please Login.")
        return redirect('login')
     return render(request, 'register.html')
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        messages.error(request, "Invalid Username or Password")

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')
@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('home')
@login_required
def add_comment(request, post_id):

    if request.method == "POST":

        post = Post.objects.get(id=post_id)

        text = request.POST.get("text")

        Comment.objects.create(
            post=post,
            user=request.user,
            text=text
        )

    return redirect('home')
@login_required
def profile(request):
    posts = Post.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'profile.html', {
        'posts': posts
    })
@login_required
def edit_profile(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {
        'form': form
    })
@login_required
def follow_user(request, user_id):

    user_to_follow = User.objects.get(id=user_id)

    if request.user != user_to_follow:

        follow = Follow.objects.filter(
            follower=request.user,
            following=user_to_follow
        )

        if follow.exists():
            follow.delete()

        else:
            Follow.objects.create(
                follower=request.user,
                following=user_to_follow
            )

    return redirect("home")
@login_required
def search_users(request):

    query = request.GET.get('q')

    users = []

    if query:
        users = User.objects.filter(username__icontains=query)

    return render(request, 'search.html', {
        'users': users,
        'query': query
    })
@login_required
def delete_post(request, post_id):

    post = Post.objects.get(id=post_id)

    if post.user == request.user:
        post.delete()

    return redirect('home')