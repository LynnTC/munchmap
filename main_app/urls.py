from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('feed/', views.feed, name='feed'),
  path('restaurants/', views.restaurant_index, name='index'),
  path('restaurants/<int:restaurant_id>/', views.restaurants_detail, name='detail'),
  path('restaurants/create/', views.RestaurantCreate.as_view(), name='restaurants_create'),
  path('restaurants/<int:restaurant_id>/review/', views.ReviewCreate.as_view(), name='reviews_create'),
  path('review/<int:pk>/update/', views.ReviewUpdate.as_view(), name='reviews_update'),
  path('review/<int:pk>/delete/', views.ReviewDelete.as_view(), name='reviews_delete'),
  path('restaurants/<int:restaurant_id>/add_photo/', views.add_photo, name='add_photo'),
  path('restaurants/<int:restaurant_id>/follow/<int:target_id>/', views.follow_user, name='follow_user'),
  path('restaurants/<int:restaurant_id>/unfollow/<int:target_id>/', views.unfollow_user, name='unfollow_user'),
  path('unfollow/<int:target_id>/', views.home_unfollow_user, name='home_unfollow_user'),
  path('profile/<int:target_id>/', views.profile_detail, name="profile_detail"),
  path('accounts/signup', views.signup, name='signup'),
]