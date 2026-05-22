from rest_framework import serializers
from .models import Task

class CreateTaskSerializer(serializers.ModelSerializer):

  class Meta:
    model = Task
    fields = ['id', 'title', 'description', 'status', 'priority', 'due_date']

  def create(self, validated_data):
    
    task = Task.objects.create(
      user = self.context['request'].user,
      title = validated_data['title'],
      description = validated_data['description'],
      status = validated_data['status'],
      priority = validated_data.get('priority'),
      due_date = validated_data.get('due_date')
    )

    return task
  

class EditTaskSerializer(serializers.ModelSerializer):

  class Meta:
    model = Task
    fields = ['id', 'title', 'description', 'status', 'priority', 'due_date']



class TasksSerializer(serializers.ModelSerializer):

  class Meta:
    model = Task
    fields = ['id', 'title', 'description', 'status', 'priority', 'due_date']
    