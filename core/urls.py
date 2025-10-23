from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks', views.task_list, name='task-list'),
    path('tasks/create/', views.task_create, name='task-create'),
    path('tasks/<int:pk>/', views.task_detail, name='task-detail'),
    path('tasks/<int:pk>/edit/', views.task_update, name='task-edit'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task-delete'),
    path('tasks/<int:pk>/toggle/', views.task_toggle_complete, name='task-toggle'),
    path('tasks/<int:pk>/progress/', views.task_update_progress, name='task-progress'),
    path('tasks/<int:pk>/steps/toggle/<int:step_pk>/', views.step_toggle, name='step-toggle'),
    path('tasks/<int:pk>/steps/add/', views.steps_add, name='steps-add'),
    path('dashboard/', views.dashboard, name='dashboard'),
]