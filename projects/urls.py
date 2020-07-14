from django.urls import path
from . import views

urlpatterns = [
    path('',views.project_list, name='project_index'),
    path("<int:pk>/", views.project_detail, name="project_detail"),
    path('projectslist',views.project_list,name="project_list")
    ]