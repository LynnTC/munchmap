import uuid
import boto3
import os
import requests
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Exists, OuterRef
from .models import Restaurant, Review, Photo, Following

# Create your views here.
def feed(request):
  following = Following.objects.filter(follower=request.user)
  reviews = Review.objects.all()
  return render(request, 'feed.html', {
    'following': following,
    'reviews': reviews
  })

@login_required
def follow_user(request, restaurant_id, target_id):
    Following.objects.create(target_id=target_id, follower=request.user)
    return redirect(f'/restaurants/{restaurant_id}/')

@login_required
def unfollow_user(request, restaurant_id, target_id):
    follow = Following.objects.get(target_id=target_id, follower=request.user)
    follow.delete()
    return redirect(f'/restaurants/{restaurant_id}/')

@login_required
def home_unfollow_user(request, target_id):
    follow = Following.objects.get(target_id=target_id, follower=request.user)
    follow.delete()
    return redirect('feed')

@login_required
def profile_unfollow_user(request, target_id):
  follow = Following.objects.get(target_id=target_id, follower=request.user)
  follow.delete()
  return redirect(f'/profile/{target_id}/')

@login_required
def profile_follow_user(request, target_id):
  Following.objects.create(target_id=target_id, follower=request.user)
  return redirect(f'/profile/{target_id}/')
  
def home(request):
  return render(request, 'home.html')

def restaurant_index(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurants/index.html', {
        'restaurants': restaurants
    })

def restaurants_detail(request, restaurant_id):
  restaurant = Restaurant.objects.get(id=restaurant_id)
  revs = Review.objects.filter(restaurant=restaurant)
  reviews = []
  for r in revs:
    followed = Following.objects.filter(target=r.user, follower=request.user).exists()   
    reviews.append({
      'review': r,
      'followed': followed
    })
  return render(request, 'restaurants/detail.html', {
    'restaurant': restaurant,
    'reviews': reviews
  })

@login_required
def restaurant_create(request, id):
  YELP_URL = f'https://api.yelp.com/v3/businesses/{id}'
  headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.environ['YELP_API_KEY']}"
    }
  response = requests.get(YELP_URL, headers=headers)
  yelp_data = response.json()
  catlist = yelp_data['categories']
  desc = ""
  for li in catlist:
    desc += li['alias']
    desc += ', '  
  try:
    if Restaurant.objects.get(yelp_api_id=id):
      restaurant = Restaurant.objects.get(yelp_api_id=id)
      return redirect(f'/restaurants/{restaurant.id}')
  except:   
    restaurant = Restaurant.objects.create(
      name=yelp_data['name'],
      description=desc,
      price=yelp_data['price'],
      user=request.user,
      yelp_api_id=id,
      picture=yelp_data['image_url']
      )
    restaurant.save()
    return redirect('../')

@login_required
def restaurant_search(request):
  YELP_URL = 'https://api.yelp.com/v3/businesses/search?categories=[restaurant]&term={}&location={}'
  term = request.GET.get('search')
  location = request.GET.get('location')
  url = YELP_URL.format(term, location)
  headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.environ['YELP_API_KEY']}"
    }
  response = requests.get(url, headers=headers)
  if 'businesses' in response.json():
    return render(request, 'restaurants/create.html', {
    'restaurants': response.json()['businesses'],
    'search': term
    })
  else: 
    return render(request, 'restaurants/create.html', {
      'search': term
    })


class ReviewCreate(LoginRequiredMixin, CreateView):
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


class ReviewUpdate(LoginRequiredMixin, UpdateView):
  model = Review
  fields = ['content', 'rating']
  success_url = '/restaurants/{restaurant_id}'


class ReviewDelete(LoginRequiredMixin, DeleteView):
  model = Review
  restaurant = model.restaurant
  success_url = '/restaurants/{restaurant_id}'

def profile_detail(request, target_id):
  reviewer = User.objects.get(id=target_id)
  reviews = Review.objects.filter(user_id=reviewer)
  followed = Following.objects.filter(target=target_id, follower=request.user).exists()   

  return render(request, 'profile/detail.html', {
    'reviews': reviews,
    'reviewer': reviewer,
    'followed': followed
  })

  
@login_required
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
    
