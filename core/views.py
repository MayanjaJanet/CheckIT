from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Task
from .forms import TaskForm
from django.utils import timezone
from django.db import OperationalError
from django.contrib import messages


def home(request):
    """
    Public landing page. Shows signup/login CTAs and a link to the app for authenticated users.
    """
    return render(request, "landing.html")

@login_required
def task_list(request):
    qs = Task.objects.filter(owner=request.user)
    status = request.GET.get('status')
    if status == 'completed':
        qs = qs.filter(completed=True)
    elif status == 'active':
        qs = qs.filter(completed=False)

    priority = request.GET.get('priority')
    if priority:
        qs = qs.filter(priority=priority)

    q = request.GET.get('q')
    if q:
        qs = qs.filter(title__icontains=q)

    qs = qs.order_by('-created_at')
    paginator = Paginator(qs, 20)
    page = request.GET.get('page')
    tasks = paginator.get_page(page)

    return render(request, 'core/task_list.html', {'tasks': tasks})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
   
    try:
        steps_qs = list(task.steps.all())
    except OperationalError:
        steps_qs = []
    return render(request, 'core/task_detail.html', {'task': task, 'steps': steps_qs})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return redirect('core:task-list')
    else:
        form = TaskForm()
    return render(request, 'core/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('core:task-list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'core/task_form.html', {'form': form, 'task': task})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('core:task-list')
    return render(request, 'core/task_confirm_delete.html', {'task': task})


@login_required
def task_toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        task.completed = not task.completed
        # If marking complete, ensure progress is 100
        if task.completed:
            task.progress = 100
        else:
            # if un-marking complete, drop progress to 0 if it was 100
            if task.progress == 100:
                task.progress = 0
        task.save()
    return redirect('core:task-detail', pk=pk)


@login_required
def task_update_progress(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        try:
            val = int(request.POST.get('progress', 0))
        except (TypeError, ValueError):
            val = task.progress
        val = max(0, min(100, val))
        task.progress = val
        # update completed flag based on progress
        task.completed = (val >= 100)
        task.save()
    return redirect('core:task-detail', pk=pk)


@login_required
def step_toggle(request, pk, step_pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    step = get_object_or_404(task.steps, pk=step_pk)
    if request.method == 'POST':
        step.done = not step.done
        step.save()
        task.recompute_progress_from_steps()
    return redirect('core:task-detail', pk=pk)


@login_required
def steps_add(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        steps_text = request.POST.get('steps_text', '').strip()
        if steps_text:
            for line in steps_text.splitlines():
                title = line.strip()
                if title:
                    task.steps.create(title=title)
            task.recompute_progress_from_steps()
    return redirect('core:task-detail', pk=pk)

@login_required
def dashboard(request):
    from .forms import QuickTaskForm

    if request.method == 'POST':
        form = QuickTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.created_at = timezone.now()
            task.save()
            messages.success(request, 'Task created successfully.')
            return redirect('core:task-list')
    else:
        form = QuickTaskForm()

    recent = Task.objects.filter(owner=request.user).order_by('-created_at')[:6]
    # compute a safe avatar URL to avoid template errors if userprofile is missing
    avatar_url = None
    try:
        profile = getattr(request.user, 'userprofile', None)
        if profile and getattr(profile, 'avatar', None):
            avatar_url = profile.avatar.url
    except Exception:
        avatar_url = None

   
    pending_count = Task.objects.filter(owner=request.user, completed=False).count()
    completed_count = Task.objects.filter(owner=request.user, completed=True).count()

    return render(request, 'core/dashboard.html', {
        'form': form,
        'recent_tasks': recent,
        'avatar_url': avatar_url,
        'pending_count': pending_count,
        'completed_count': completed_count,
    })
