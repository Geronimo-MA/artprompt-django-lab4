from django.contrib import admin
from .models import ArtPrompt, Category, TagPrompt, PromptMeta


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(TagPrompt)
class TagPromptAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'slug')
    list_display_links = ('id', 'tag')
    search_fields = ('tag',)
    prepopulated_fields = {'slug': ('tag',)}


@admin.register(PromptMeta)
class PromptMetaAdmin(admin.ModelAdmin):
    list_display = ('id', 'difficulty', 'estimated_time', 'materials')
    list_display_links = ('id', 'difficulty')
    search_fields = ('difficulty', 'materials')


@admin.register(ArtPrompt)
class ArtPromptAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'slug',
        'style',
        'status',
        'cat',
        'time_create',
    )
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content', 'style')
    list_filter = ('status', 'cat', 'tags', 'time_create')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)