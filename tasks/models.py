from django.db import models
from django.conf import settings
from django.utils.timezone import now
# Create your models here.
class Task(models.Model):

  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

  class Status(models.TextChoices):
    PENDING = "pending", "Pending"
    COMPLETED = "completed", "completed"

  title = models.CharField(max_length=200)
  description = models.CharField(max_length=400)

  status = models.CharField(
    max_length=40,
    choices=Status.choices,
    default=Status.PENDING
  )

  class Priority(models.TextChoices):
    HIGH = 'high_priority', 'High_priority'
    MEDIUM = 'medium_priority', 'Medium_priority'
    LOW = 'low_priority', 'Low_priority'

  priority = models.CharField(
    max_length=50,
    choices= Priority.choices,
    default=Priority.MEDIUM
  )

  due_date = models.DateField(null=True, blank=True)

  created_at = models.DateTimeField(auto_now_add=True)

  updated_at = models.DateTimeField(auto_now=True)

  is_deleted = models.BooleanField(default=False)

  @property
  def is_overdue(self):
    return (
      self.due_date
      and self.due_date < now().date()
      and self.status != "completed"
    )

  def __str__(self):
    return f"{self.id}. {self.title}  user_id:{self.user.id}"