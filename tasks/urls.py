from django.urls import path
from .views import TaskListCreateView, TaskDetailView

urlpatterns = [
  path('tasks/', TaskListCreateView.as_view()),
  path('tasks/<int:task_id>/', TaskDetailView.as_view())
]