from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
     path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
     path('like/<int:post_id>/', views.like_post, name='like_post'),
     path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
     path('profile/', views.profile, name='profile'),
     path('edit-profile/', views.edit_profile, name='edit_profile'),
     path(
    "follow/<int:user_id>/",
    views.follow_user,
    name="follow_user"
),
path('search/', views.search_users, name='search_users'),
path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
]