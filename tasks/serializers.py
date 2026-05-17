from rest_framework import serializers
from .models import Task

class CreateTaskSerializer(serializers.ModelSerializer):

  class Meta:
    model = Task
    fields = ['id', 'title', 'description', 'status']

  def create(self, validated_data):
    
    task = Task.objects.create(
      user = self.context['request'].user,
      title = validated_data['title'],
      description = validated_data['description'],
      status = validated_data['status']
    )

    return task
  

class EditTaskSerializer(serializers.ModelSerializer):

  class Meta:
    model = Task
    fields = ['id', 'title', 'description', 'status']



class TasksSerializer(serializers.ModelSerializer):

  class Meta:
    model = Task
    fields = ['id', 'title', 'description', 'status']
    