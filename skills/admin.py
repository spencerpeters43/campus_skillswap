from django.contrib import admin
from .models import SkillPost, Review, Appointment


@admin.register(SkillPost)
class SkillPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'rate', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'author__username']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['requester', 'skill_post', 'date', 'time', 'created_at']
    list_filter = ['date']
    search_fields = ['requester__username', 'skill_post__title']
    readonly_fields = ['created_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'skill_post', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['reviewer__username', 'skill_post__title', 'comment']
    readonly_fields = ['created_at']
