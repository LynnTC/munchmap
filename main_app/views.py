import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Restaurant, Review, Photo, Following

# Create your views here.
def home(request):
  following = Following.objects.all()
  reviews = Review.objects.all()
  return render(request, 'home.html', {
    'following': following,
    'reviews': reviews
  })

def follow_user(request, restaurant_id, target_id):
    Following.objects.create(target_id=target_id, follower=request.user)
    return redirect(f'/restaurants/{restaurant_id}/')

def unfollow_user(request, restaurant_id, target_id):
    follow = Following.objects.get(target_id=target_id, follower=request.user)
    follow.delete()
    return redirect(f'/restaurants/{restaurant_id}/')
  
def about(request):
  return render(request, 'about.html')

def restaurant_index(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurants/index.html', {
        'restaurants': restaurants
    })

def restaurants_detail(request, restaurant_id):
  restaurant = Restaurant.objects.get(id=restaurant_id)
  return render(request, 'restaurants/detail.html', {
    'restaurant': restaurant,
  })

class RestaurantCreate(CreateView):
  model = Restaurant
  fields = ['name', 'description', 'genre', 'price']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


class ReviewCreate(CreateView):
  model = Review
  fields = ['content', 'rating']

  def form_valid(self, form):
    form.instance.user = self.request.user
    form.instance.date = timezone.now()
    restaurant_id = self.kwargs.get('restaurant_id')
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    form.instance.restaurant = restaurant

    return super().form_valid(form)
  
  success_url = '/restaurants/{restaurant_id}'


class ReviewUpdate(UpdateView):
  model = Review
  fields = ['content', 'rating']
  success_url = '/restaurants/{restaurant_id}'


class ReviewDelete(DeleteView):
  model = Review
  restaurant = model.restaurant
  success_url = '/restaurants/{restaurant_id}'
  

def add_photo(request, restaurant_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      Photo.objects.create(url=url, restaurant_id=restaurant_id)
    except Exception as e:
      print('An error occurred uploading file to S3')
      print(e)
  return redirect('detail', restaurant_id=restaurant_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
    
