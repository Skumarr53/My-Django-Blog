from django.shortcuts import render
from django.views.generic import (ListView,
DetailView
)
from django.contrib.auth.models import User
from .models import Post, Comment, Category
from .forms import CommentForm

# Create your views here.
# the class below is for create list view rendering of blog pages
# ListView is the base module that presents list of objects or posts in this case

#class PostListView(ListView):
#    model = Post # yet to create model

def blog_index(request):
    posts = Post.objects.all().order_by('-date_posted')
    context = {
        "posts": posts,
    }
    return render(request, "blog/blog_index.html", context)
    

def about(request):
    return render(request,'blog/about.html', {'title':'About'})

def bloghome(request):
    return render(request,'blog/about.html', {'title':'home'})

class PostListView(ListView):
    model = Post
    template_name = 'blog/bloglist.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post

def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post
            )
            comment.save()

    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }
    return render(request, "blog/blog_detail.html", context)


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/bloglist.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/blog_category.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        category = get_object_or_404(Category, name=self.kwargs.get('name'))
        return Post.objects.filter(categories=category).order_by('-date_posted')

def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-created_on'
    )
    context = {
        "category": category,
        "posts": posts
    }
    return render(request, " blog/blog_category.html", context)