from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Task
from rest_framework.response import Response
from rest_framework import status
from .serializers import  TaskSerializer
from .pagination import TaskPagination
from django.utils.timezone import now
from rest_framework.views import APIView

class TaskListCreateAPIView(APIView):

  permission_classes = [IsAuthenticated]

  def get(self, request):

    tasks = Task.objects.filter(
      user=request.user,
      is_deleted=False
    )

    status_param = request.query_params.get('status')
    search_query = request.query_params.get('search')
    priority_param = request.query_params.get('priority')
    overdue_param = request.query_params.get('overdue')

    if status_param:

      tasks = tasks.filter(
        status=status_param
      )

    if search_query:

      tasks = tasks.filter(
        title__icontains=search_query
      )
    
    if priority_param:

      tasks = tasks.filter(
        priority=priority_param
      )

    if overdue_param == "true":

      tasks = tasks.filter(
        due_date__lt=now().date(),
        status="pending" 
      )

    paginator = TaskPagination()

    paginated_tasks = paginator.paginate_queryset(
      tasks,
      request
    )
    
    serializer = TaskSerializer(
      paginated_tasks, 
      many=True
    )

    return paginator.get_paginated_response(
      serializer.data
    )
  

  def post(self, request):

    serializer = TaskSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
      
      serializer.save(user=request.user)

      return Response({
        'message': 'Task created successfully',
        'data': serializer.data
      }, status=status.HTTP_201_CREATED)  
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailAPIView(APIView):

  permission_classes = [IsAuthenticated]

  def get(self, request, task_id):

    task = get_object_or_404(Task, id=task_id, user=request.user)

    serializer = TaskSerializer(task)

    return Response({
      'data': serializer.data
    }, status=status.HTTP_200_OK)


  def patch(self, request, task_id):

    task = get_object_or_404(
      Task, 
      id=task_id, 
      user=request.user,
      is_deleted=False
    )
    
    serializer = TaskSerializer(task, data=request.data, partial=True)

    if serializer.is_valid():

      serializer.save()

      return Response({
        'message': 'Task Updated successfully',
        'data': serializer.data
      })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

  def delete(self, request, task_id):

    task = get_object_or_404(Task, id=task_id, user=request.user, is_deleted=False)

    task.is_deleted = True
    task.save()

    return Response({
      'message': "task deleted successfully."
    })
