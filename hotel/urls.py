from django.urls import path

from . import views

app_name = 'hotel'

urlpatterns = [
    path('', views.room_index, name='index'),
    path('category/<slug:category_slug>/', views.category_rooms, name='category'),
    path('rooms/create/', views.create_room, name='create_room'),
    path('rooms/<slug:room_slug>/edit/', views.edit_room, name='edit_room'),
    path('rooms/<slug:room_slug>/', views.room_detail, name='room_detail'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('rooms/<slug:room_slug>/book/', views.create_booking, name='create_booking'),
    path('bookings/', views.user_bookings, name='user_bookings'),
]
