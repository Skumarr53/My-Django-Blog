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

### Push project
Now that heroku created Git Repo for us Let's push it to our GitHub in Heroku
```bash
git push heroku master
```