from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

RATING = (
    (1, '⭐'),
    (2, '⭐⭐'),
    (3, '⭐⭐⭐'),
    (4, '⭐⭐⭐⭐'),
    (5, '⭐⭐⭐⭐⭐')
)

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
  

class Review(models.Model):
  content = models.TextField(max_length=1000)
  date = models.DateField('Review Date', auto_now_add=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  rating = models.IntegerField(
    max_length=1,
    choices = RATING,
    default = RATING[4][0]
    )
  
  restaurant = models.ForeignKey(
    Restaurant,
    on_delete=models.CASCADE
  )

  class Meta:
    ordering = ['-date']



