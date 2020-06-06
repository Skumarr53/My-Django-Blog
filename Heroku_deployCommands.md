### Install Heroku CLI tools
```bash
pip install heroku
```
### Login into Heroku
```bash
heroku login
```

Now you are authenticated

### install Gunicorn
```bash
pip install gunicorn
```

### create reqirements.txt
```bash
pip freeze > requirements.txt
```

### Git commit

``` bash
git add .
git push origin master
```
### Heroku app creation
```bash
heroku create skumar-djangoblog
```

### Set STATIC_ROOT
add the following command in ```settings.py```
```python
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
```

### create a proc file
create a txt file named as 'Procfile' for configring web process (tells heroku how we want to run our application). paste the following code into it.
```yml
web: gunicorn MyDjangoBlog.wsgi # MyDjangoBlog is my directory where settings.py resides
```

### create a secret key for prodcution enviorment 
Secret key is useful Debugging app in production from local machine (use key to get access permission to debug app in production enviroment). I'm using python's
```secrets``` package to generate key.

```python
import secrets
secrets.token_hex(24)
```
### Add key to environment variable
Copy the key you generated and add to bash profile

```python
# DJANGO BLOG VARS
export SECRET_KEY="Your key enclosed in quotes"
export DEBUG_VALUE="True"
```
### Register key on Heroku

Use same key you added to your bash profile
```yml
heroku config:set SECRET_KEY="Your key enclosed in quotes"
heroku config:set DEBUG_VALUE="True"
```

### Add Email Cretiditals
Used for automated sending info to your subscibers (such as share newly published blog) 
``` python
heroku config:set EMAIL_USER="Your@Email"
heroku config:set EMAIL_PASS="Your Password"
```

### Set Secret Key in settings.py file
Tell Django to use your SECRET_KEY from bash profile instaed of default generated. Open ```settings.py```file comment the SECRET_KEY line add the caommand that grabs key from bash profile.

```python
#SECRET_KEY = '*41$dqx9)opnx^*^&*tdb0boiwgtv5w%&_%$sb*l!@s@$0h5#q'
SECRET_KEY = os.environ.get('SECRET_KEY')
```

### Install Postgres Database
We need to have Postgres Database as heroku expects it instaed of default sqlite3 database which Django uses.
```bash
sudo apt-get install postgresql
```

check ```psql``` if it throws error probably user does not recognized by ```postgres```

To make it work execute following commands 

```bash 
sudo su - postgres

## postgres shell activates
createuser username # username of user you want to add
createdb -O username username
```
exit 

### Install django-heroku

Helps to sync congirations between django and heroku
``` bash
pip install django-heroku
```

add the lines below in settings.py file

```python
import django_heroku
django_heroku.settings(locals())
```

### Update requiremenats.txt file
Add newly installed packages

```bash
pip freeze > requirements.txt
```
### Create Database on heroku

```python
heroku run python manage.py migrate
```

### Add super user on heroku
connect to heroku bash shell

```bash
heroku run bash
```
### Modify the Debug value in settings.py file
change the Debug value to the one shown below.
``` python
DEBUG = (os.environ.get('DEBUG_VALUE') == "True")
```
### Git commit 
Commit the changes you made till this point


### Push project
Now that heroku created Git Repo for us Let's push it to our GitHub in Heroku
```bash
git push heroku master
```

### roll back to previous version

In case you you want to roll back to the previous version for some reason. 

``` bash
heroku releases
```
outputs a table where first column is the version number. Choose the version you want to roll back to.

```bash
heroku rollback 'VersionNo'
```

## Atomated processing md files to HTML posts on Heroku

```bash
heroku run bash
python manage.py shell
exec(open("blog/markdown2post.py").read())
```