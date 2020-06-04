from django.urls import path
from .views import  PostListView, UserPostListView, PostDetailView
from . import views

urlpatterns = [
    path("blog/", views.blog_index, name="blog_index"),
    path('',views.about, name='about'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path("blog/<category>/", views.blog_category, name="blog_category"),
]