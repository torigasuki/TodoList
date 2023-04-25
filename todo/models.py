from django.db import models

from users.models import User

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completion_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    
    