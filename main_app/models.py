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
  yelp_api_id = models.CharField(max_length=50)

  def __str__(self):
    return f'{self.name} ({self.id})'
  
  def get_absolute_url(self):
    return reverse('detail', kwargs={'restaurant_id': self.id})
  

class Review(models.Model):
  content = models.TextField(max_length=1000)
  date = models.DateField('Review Date', auto_now_add=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  rating = models.IntegerField(
    choices = RATING,
    default = RATING[4][0]
    )
  
  def get_rating_display(self):
    return dict(RATING)[self.rating]
  
  restaurant = models.ForeignKey(
    Restaurant,
    on_delete=models.CASCADE
  )

  class Meta:
    ordering = ['-date']


class Following(models.Model):
  target = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "followers")
  follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "targets")


class Photo(models.Model):
  url = models.CharField(max_length=200)
  restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for restaurant_id: {self.restaurant_id} @{self.url}"
