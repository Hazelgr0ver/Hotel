from django import forms
from django.contrib.auth import get_user_model
from .models import Room, Comment, Booking

User = get_user_model()


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['title', 'text', 'slug', 'image', 'pub_date', 'location', 'category', 'price', 'capacity']
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
