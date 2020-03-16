from django.contrib import admin
from .models import Board, Topic, Post

# Register your models here.


class BoardAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name", "description"]
    list_per_page = 20


admin.site.register(Board, BoardAdmin)


class TopicAdmin(admin.ModelAdmin):
    list_display = ["subject", "board", "starter"]
    search_fields = ["board__name", "starter__username"]
    list_filter = ["board__name"]
    list_per_page = 20


admin.site.register(Topic, TopicAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ["topic", "created_by", "created_at"]
    search_fields = ["topic__subject", "created_by__username"]
    list_filter = ["topic__subject"]
    list_per_page = 20


admin.site.register(Post, PostAdmin)
