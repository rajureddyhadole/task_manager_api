from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Task
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateTaskSerializer, EditTaskSerializer, TasksSerializer
from .pagination import TaskPagination
from django.utils.timezone import now

# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_list_create(request):

  if request.method == "GET":
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
    
    serializer = TasksSerializer(
      paginated_tasks, 
      many=True
    )

    return paginator.get_paginated_response(
      serializer.data
    )
  


  if request.method == "POST":
    serializer = CreateTaskSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
      
      serializer.save()

      return Response({
        'message': 'Task created successfully',
        'data': serializer.data
      })  
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_detail(request, task_id):
  
  if request.method == "PUT":

    task = get_object_or_404(
      Task, 
      id=task_id, 
      user=request.user,
      is_deleted=False
    )
    
    serializer = EditTaskSerializer(task, data=request.data, partial=True)

    if serializer.is_valid():

      serializer.save()

      return Response({
        'message': 'Task Updated successfully',
        'data': serializer.data
      })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

  if request.method == "DELETE":

    task = get_object_or_404(Task, id=task_id, user=request.user)

    task.is_deleted = True
    task.save()

    return Response({
      'message': "task deleted successfully."
    })
