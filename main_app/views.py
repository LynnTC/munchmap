from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Restaurant
from .forms import ReviewForm

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def restaurant_index(request):
  return render(request, 'restaurants/index.html')

def restaurants_detail(request, restaurant_id):
  restaurant = Restaurant.objects.get(id=restaurant_id)
  review_form = ReviewForm()
  return render(request, 'restaurants/detail.html', {
    'restaurant': restaurant,
    'review_form': review_form,
  })

class RestaurantCreate(CreateView):
  model = Restaurant
  fields = ['name', 'description', 'genre', 'price']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

def ReviewCreate(request, restaurant_id):
  form = ReviewForm(request.POST)
  if form.is_valid():
    new_review = form.save(commit=False)
    new_review.restaurant_id = restaurant_id
    new_review.save()
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
    
