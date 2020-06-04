from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

# Categories for filtering posts based on keywords
class Category(models.Model):
    name = models.CharField(max_length=20)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()   #lines of characters
    date_posted = models.DateTimeField(default=timezone.now) #take date&time post creation  
    author = models.ForeignKey(User, on_delete=models.CASCADE) # asking it delete the post when user is deleted 
    categories = models.ManyToManyField('Category', related_name='posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs = {'pk': self.pk})

class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)



