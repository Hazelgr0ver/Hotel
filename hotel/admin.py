from django.contrib import admin
from .models import Category, Location, Room, Booking, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'category', 'location', 'pub_date', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('title', 'text')
    list_filter = ('category', 'location', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'pub_date'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'author', 'check_in', 'check_out', 'created_at')
    search_fields = ('room__title', 'author__username')
    list_filter = ('check_in', 'check_out')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('room', 'author', 'created_at')
    search_fields = ('text', 'author__username')
    list_filter = ('created_at',)
