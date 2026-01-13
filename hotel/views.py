from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Room, Category, Comment, Booking
from .forms import RoomForm, CommentForm, ProfileForm, BookingForm

User = get_user_model()


def room_index(request):
    rooms = Room.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True,
    ).select_related('author', 'location', 'category')
    paginator = Paginator(rooms, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'hotel/index.html', context)


def category_rooms(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug, is_published=True)
    rooms = category.rooms.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
    ).select_related('author', 'location')
    paginator = Paginator(rooms, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': category, 'page_obj': page_obj}
    return render(request, 'hotel/category.html', context)


def room_detail(request, room_slug):
    room = get_object_or_404(Room, slug=room_slug, is_published=True, pub_date__lte=timezone.now())
    comments = room.comments.select_related('author')
    form = CommentForm()
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.room = room
            comment.author = request.user
            comment.save()
            return redirect('hotel:room_detail', room_slug=room.slug)
    context = {'room': room, 'comments': comments, 'form': form}
    return render(request, 'hotel/detail.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    rooms = author.room_set.filter(is_published=True).select_related('category', 'location')
    paginator = Paginator(rooms, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'author': author, 'page_obj': page_obj}
    return render(request, 'hotel/profile.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.author = request.user
            room.save()
            return redirect('hotel:profile', username=request.user.username)
    context = {'form': form}
    return render(request, 'hotel/create.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_room(request, room_slug):
    room = get_object_or_404(Room, slug=room_slug, author=request.user)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('hotel:room_detail', room_slug=room.slug)
    context = {'form': form, 'room': room}
    return render(request, 'hotel/edit.html', context)


@login_required
def edit_profile(request):
    form = ProfileForm(instance=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('hotel:profile', username=request.user.username)
    context = {'form': form}
    return render(request, 'hotel/edit_profile.html', context)

@login_required
def create_booking(request, room_slug):
    room = get_object_or_404(Room, slug=room_slug, is_published=True, pub_date__lte=timezone.now())
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.author = request.user
            booking.save()
            return redirect('hotel:room_detail', room_slug=room.slug)
    context = {'room': room, 'form': form}
    return render(request, 'hotel/booking.html', context)

@login_required
def user_bookings(request):
    bookings = Booking.objects.filter(author=request.user).select_related('room').order_by('-created_at')
    context = {'bookings': bookings}
    return render(request, 'hotel/bookings.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration_form.html', {'form': form})
