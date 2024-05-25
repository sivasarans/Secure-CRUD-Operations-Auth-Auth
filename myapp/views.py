from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Task
from .forms import TaskForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')  # or redirect to dashboard
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    tasks = Task.objects.all()
    form = TaskForm()
    return render(request, 'dashboard.html', {'tasks': tasks, 'form': form})

@csrf_exempt
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            return JsonResponse({'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed})
    return JsonResponse({'error': 'Invalid form'}, status=400)

@csrf_exempt
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            return JsonResponse({'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed})
    elif request.method == 'GET':
        return JsonResponse({'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed})
    return JsonResponse({'error': 'Invalid form'}, status=400)

@csrf_exempt
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return JsonResponse({'success': True})
