from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Restaurant(models.Model):
  name = models.CharField(max_length=50)
  description = models.TextField(max_length=250)
  genre = models.CharField(max_length=50)
  price = models.CharField(max_length=50)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.name} ({self.id})'
  
  def get_absolute_url(self):
    return reverse('detail', kwargs={'restaurant_id': self.id})
  


