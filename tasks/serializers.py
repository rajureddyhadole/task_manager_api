from rest_framework import serializers
from .models import Task
from django.utils.timezone import now

class TaskSerializer(serializers.ModelSerializer):

  class Meta:
    model = Task
    fields = ['id', 'title', 'description', 'status', 'priority', 'due_date']

  def validate_due_date(self, value):

    if value and value < now().date():

      raise serializers.ValidationError(
        "Due date cannot be in past"
      )
    
    return value

  
  def validate_due_date(self, value):

    if value and value < now().date():

      raise serializers.ValidationError(
        "Due date cannot be in past"
      )
    
    return value
