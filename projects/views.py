from pathlib import Path
from django.shortcuts import render
from projects.models import Project

# Create your views here.
def project_index(request):
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request,'project_index.html',context)

def project_detail(request, pk):
    project = Project.objects.get(pk=pk)
    context = {
        'project': project
    }
    return render(request, 'project_detail.html', context)

def project_list(request):
    with open('projects/Pjects_list/readme.md','r') as f:
        text = f.read()
    context = {'text': text}
    return render(request,'projects_lists.html', context) 