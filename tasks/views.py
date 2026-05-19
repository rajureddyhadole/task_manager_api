from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Task
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateTaskSerializer, EditTaskSerializer, TasksSerializer
from .pagination import TaskPagination

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):

  serializer = CreateTaskSerializer(data=request.data, context={'request': request})

  if serializer.is_valid():
    
    serializer.save()

    return Response({
      'message': 'Task created successfully',
      'data': serializer.data
    })  
  
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_task(request, task_id):
  
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



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_tasks(request):

  tasks = Task.objects.filter(
    user=request.user,
    is_deleted=False
  )

  status_param = request.query_params.get('status')
  search_query = request.query_params.get('search')

  if status_param:

    tasks = tasks.filter(
      status=status_param
    )

  if search_query:

    tasks = tasks.filter(
      title__icontains=search_query
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



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, task_id):
  
  task = get_object_or_404(Task, id=task_id, user=request.user)

  task.is_deleted = True
  task.save()

  return Response({
    'message': "task deleted successfully."
  })