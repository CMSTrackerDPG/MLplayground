from django.shortcuts import render
from django.http import HttpResponseRedirect 
# TODO Check that this is the best option

from .models import Task
from .forms import TaskForm


def create_task_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = TaskForm()
        return render(request, "challenge/create_task.html", {'form': form})
