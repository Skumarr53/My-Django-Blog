# How I built my first website using Django 

Even though I am not Computer science gradute I am always passionate about things technology has to offer particularly python. This my first Django Project is one among them wanted have my own personal website where I can publish my ideas and experience. As I go along I try my best to explain the step I carried. I hope it helps you to build your own or going to build one in future. Lets get started.

1. create Django environment and setup Project.
I created a project main directory under 'MyDjangoBlog' and setup a conda environment under Python 3.7.3 version. Please make sure that is working directory is set to Project root directroy when executing the commands in terminal/powrshell.
```
    $~ conda create -n DjangoEnv pyton=3.7.3 # DjangoEnv is the env name
    $~ conda activate DjangoEnv
    $~ conda install Django
    $~ django-admin startproject MyDjangoBlog # creates a Django project skeleton.
```


2. The project dir MyDjangoBlog is package the connects project with the Django app.

The moment you run last line in the above section. A project dir is created which contains a main folder under same name and manage.py file. django-admin is CLI utility lets us run various administrative tasks app creation. manage.py does the same
thing as django-admin plus it takes care of few things for you. For example, before you can use Django, you need to tell it which settings.py file to use. manage.py does this by defining an environment variable with the name “DJANGO_SETTINGS_MODULE”. and setting up database. The manage.py lets us interact with the Django project. migrations folder contains the migration files for the app and also used to push updates whenever required. These are used to apply changes to the database 'db.sqlite3'. The database file 'db.sqlite3' stores all the application data in SQL tables. All our project configurations happens in settings.py file. I urge you to take a look at them once. 

Creating apps 
- Applications the packages we create thta adds features to our project. app are groups of similar set of features. 
- We have only initiated the project. We don't have anything to show. Lets create a app that displays on out site. I will create a blog under same name.
``` 
- python manage.py startapp blog # blog is the app name
```
   

- apps.py is used to configure the app
- models.py file store information about the data you want to work with. Typically each model maps to a database table.

Now that we have created the app. we should also connect or link it with the main project by adding it into 'INSTALLED_APPS' along with the django owned apps in the 'settings.py' file. 

Creating a index.html or homepage
- Its time to create a homepage which is html file the renders the information  we would to show when user visits our website. By default 'templates/appname' is the folder where django look for html files. I am creating a template called 'home.html' which the homepage for my site inside templetes dir.
    - mkdir -p ./blog/templates/blog
    - touch ./blog/templates/blog/home.html

Creating folder inside templates with the name same as app name may look bit odd. But Django by default expects same structure because Django discovers templete. 


before filling in home.html file lets create a base html file  that stores stuff that are common across the pages like Web logo, asteutic properties, navigation panel etc so that we inherit these properties from the base.html instead recreating them from scratch on every page. Another advantage is that if we wish to redesign same can be done at single point.
    - touch ./blog/templates/blog/base.html


After creating the home html file. We have to add route into 'urlpatterns' the MyDjangoBlog/urls.py file.
    - path('', views.about, name = 'blog-about'), #Not supplied match keyword refers to hompage

In the path first argument is the route pattern which is the string that follows our web domain name since. This is the homepage I am passing empty string as the first argument telling wherever there is no string attached in front of domain name (url for homepage) call the 'views.about' def. name stores the  


WSGI is a specification that deals with interactions between web servers and Python web applications. The startproject command sets up default configuration for it in wsgi.py.

Templete Inheritance
Remember we created a base template (base.html) from which properties and syles can be inherited onto other templates Lets see how its done. Open base html then fill with the lines that give  basic look to the webpage. Then add  this block '{% block content %}{% endblock %}'. When other templetes inherits from base template this tag acts like a opening portal between which you can add content specific to that page.
    ex: 
    Here is my base.html
    - <!DOCTYPE html>
        <html lang="en">
            <head>
                <title>DjangoBlog</title>
            </head>
            <body>
                <div id="content">
                    {% block content %}{% endblock %}  <---
                </div>
            </body>
        </html>

I wish to inherit base.html into about.html then add 'About Me' as title of this page.
    -{% extends 'blog/base.html' %} /*/ inherits from base templete
        {% block content %}
            <h1> About Me</h1>  /*/ content of the page goes inside tags
        {% endblock %}

In my case I want to keep about.html as home page when user enters domain page. 

```
    from django.urls import path, include

    path('', include('blog.urls'))
```

This tells the project whatever the string part in the url after the root domain url is routed to urls in the blog. In the above case the string is empty ('') so root url is routed to blog.

Go to the 'blog/urls.py' and add this code.
```
    from . import views
    
    path('',views.about, name='about')
```

Here the string cut/routed string ('') matches with one in here then about view rendered from the views.py. In short when an person clicks domian/root url it will be redircted to about.html. Strings is the main urls.py and the one in blog/urls.py should match.

# Show the shreenshot of the page

Optional:
If you launch you webite It will look ugly as it has only text with not proper sturture given or styles added. Let's do that.
Create a stylesheet called 'main.css' then place it in  'static/blog/' in side blog app directory.
The css file which I designed you can download it from following link and modify it if you wish.
    - \\ link to css \\

Once you main.css is ready we need to tell our templetes to use this file.
    add this line  into base.html on top of DOCTYPE html.

    -below title tag  add this tag:
    ```
    {% load static %}
    <DOCTYPE html>
    <link rel="stylesheet" type="text/css" href="{% static 'blog/main.css' %}" />
Note: Make sure that 'django.contrib.staticfiles' app is added into the INSTALLED_APPS list inside settings.py. Its installed by default.

- Go ahead and launch project by running.
    - python manage.py runserver

    // add a screenshot


## Creating models
All of our model reside in models.py created by default. 

For demotration lets create a model called myFirstModel a sub class of 'django.db.models' class with title attribute. It is the class which allow us to store information in the sql database. Open models.py file and enter the following code.
```
    from django.db import models
    from django.utils import timezone
    from django.contrib.auth.models import User
    from django.urls import reverse

    class Post(models.Model):
        title = models.CharField(max_length=100)
        content = models.TextField()   # post content paragraph 
        date_posted = models.DateTimeField(default=timezone.now) #take date&time post creation  
        author = models.ForeignKey(User, on_delete=models.CASCADE) # asking it delete the post when user is deleted 

        def __str__(self):
            return self.title

        def get_absolute_url(self):
            return reverse('post-detail', kwargs = {'pk': self.pk})

```
we created a model to define sql data schema or metadata with title column and other attributes. Also we created '__str__' that output title when a post is created and url generating method 'get_absolute_url'.

We also need to register this in admin.py 
    - from blog.models import myFirstModel
    - admin.site.register(Post)

Then run below line:
    - python manage.py makemigrations
    - python manage.py migrate

the first generates the SQL commands and second executes those commands. This will put tables inside db.sqlite3. If you look look into the 0001_initial.py generated inside the migrations folder you will see information about model you just created. If you interested to know the SQL command that will be executed when you run make migrations type the line below in cmd.
```
    python manage.py sqlmigrate blog 0001
```

Once this ready now we are able add users.

Lets create SuperUser with admin accsess. Run below command and fill the admin details.
    - python manage.py createsuperuser

Go to http://127.0.0.1:8000/admin and fill in credentials acess control.

Now you are directed to the admin page and you should be able to see Post under 'Blog' (app name) which you created before. If click on that It let's you to add posts. However, It is added in the backend not rendered on frontend which web users see for that we have to create a funtion in views.py that does exactly that. open '

Create a class that renders list view of the posts added by us. Sound like big task but actual pretty simple. There are classes already availble in creating general specific views to inherit from.
Add below lines of code in views.py in the blog app folder.

```
    from django.views.generic.list import ListView
    from .models import Post

    class PostListView(ListView):
        model = Post
        template_name = 'blog/bloglist.html' # templete name
        context_object_name = 'posts' # name refering outside
        ordering = ['-date_posted']
```

Here we are creating subclass of Django's ListView called PostListView that creates list view for our posts. Here notice that we assigned a html templete name to the templete_name variable. This is the templete renders our list view. we will create this templete. before that create a routing url in the urls.py that renders this view. Add below lines into urls.py  
```
from .views import  PostListView
```

Add below line into urlpatterns list in the same file.
```
path('blog/', PostListView.as_view(), name='blog-home'),
```
We are ready with url that directs user Lets. go ahed and create the templete.

```
touch ./blog/templates/blog/bloglist.html 
``` 
open the templete you just created. paste the code block below.

```
{% extends 'blog/base.html' %}
{% block content %}
    {% for post in posts %}
    <article class="media content-section">
        <img class="rounded-circle article-img" src="{{ post.author.profile.image.url }}" >
          <div class="media-body">

            <div class="article-metadata">              
              <small class="text-muted">published on: {{ post.date_posted|date:"F d, Y" }}</small>
            </div>
            <h2><a class="article-title" href="{% url 'post-detail' post.id %}">{{ post.title }}</a></h2>
            <!--<h2><a class="article-title" href='#'>{{ post.title }}</a></h2>-->
            <p class="article-content">{{ post.content }}</p>
          </div>
        </article> 
    {% endfor %}

{% endblock %}
```


