from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Task
from rest_framework import filters
from .serializers import  TaskSerializer
from .pagination import TaskPagination
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


class TaskViewSet(viewsets.ModelViewSet):
  serializer_class = TaskSerializer
  permission_classes = [IsAuthenticated]
  pagination_class = TaskPagination
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
  filterset_fields = ['status', 'priority']
  search_fields = ['title', 'description']
  ordering_fields = ['created_at', 'title']

  def get_queryset(self):
    return Task.objects.filter(user=self.request.user, is_deleted=False)

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

  def perform_destroy(self, instance):
    instance.is_deleted = True
    instance.save()
