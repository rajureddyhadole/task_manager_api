from rest_framework import serializers
from .models import Task
from django.utils.timezone import now

class CreateTaskSerializer(serializers.ModelSerializer):

  class Meta:
    model = Task
    fields = ['id', 'title', 'description', 'status', 'priority', 'due_date']

  def validate_due_date(self, value):

    if value and value < now().date():

      raise serializers.ValidationError(
        "Due date cannot be in past"
      )
    
    return value

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

  def validate_due_date(self, value):

    if value and value < now().date():

      raise serializers.ValidationError(
        "Due date cannot be in past"
      )
    
    return value



class TasksSerializer(serializers.ModelSerializer):

  class Meta:
    model = Task
    fields = ['id', 'title', 'description', 'status', 'priority', 'due_date']