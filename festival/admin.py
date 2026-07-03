from django.contrib import admin
from .models import Category, Work, Vote, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'category', 'vote_count', 'submitted_at')
    list_filter = ('category',)
    search_fields = ('title', 'author_name')


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'work', 'voted_at')
    list_filter = ('work',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'work', 'created_at')
    list_filter = ('work',)
    search_fields = ('body',)