#!/usr/bin/env python

#----------------Run the below commands to convert Medium to Markdown---
#mediumexporter Link-to-article > path-of-output-md-file
#For ex:
#mediumexporter https://medium.com/@skumarr53/setting-up-python-jupyter-spark-integrated-environment-in-aws-ec2-instance-6dfd93a85c84 > medium_post.md

#----------------run the below commands to upload all the md files and register in database----------
#python manage.py shell
#exec(open("blog/markdown2post.py").read())

# python manage.py makemigrations
# python manage.py migrate

# ---------------

from pathlib import Path
from django.contrib.auth.models import User
from blog.models import Post
from pdb import set_trace

# user defined paths
user = User.objects.all()[0]
posts_folder  = Path('blog/posts_markdown')

# dict post for fillingin details

#prev_titles = [i.title for i in Post.objects.all()]
prev_titles = []

for path in posts_folder.iterdir():
    
    title = str(path).split('/')[-1].replace('-',' ') # 
    filname = str(path).split('/')[-1]
    if title not in prev_titles:
        with open(path/f'{filname}.md','r') as f:
            txt = f.read()
        dict_post = {'title':title,'content':txt,'author':user}
        post = Post(**dict_post)
        post.save()
        print(f"processed: {title}")
    
