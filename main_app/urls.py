from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('restaurants/', views.restaurant_index, name='index'),
  path('restaurants/<int:restaurant_id>/', views.restaurants_detail, name='detail'),
  path('restaurants/create/', views.RestaurantCreate.as_view(), name='restaurants_create'),
  path('restaurants/<int:restaurant_id>/review/', views.ReviewCreate.as_view(), name='reviews_create'),
  path('review/<int:pk>/update/', views.ReviewUpdate.as_view(), name='reviews_update'),
  path('restaurants/<int:restaurant_id>/review_delete/', views.ReviewDelete.as_view(), name='reviews_delete'),
  path('restaurants/<int:restaurant_id>/add_photo/', views.add_photo, name='add_photo'),
  path('accounts/signup', views.signup, name='signup'),
]