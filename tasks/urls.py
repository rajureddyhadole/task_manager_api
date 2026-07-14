from django.urls import path
from .views import  edit_task, delete_task, task_list_create

urlpatterns = [
  path('tasks/', task_list_create, name='task_list_create'),
  path('tasks/edit/<int:task_id>/', edit_task, name='edit_task'),
  path('tasks/delete/<int:task_id>/', delete_task, name='delete_task')
]