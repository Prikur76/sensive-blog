from django.contrib import admin
from blog.models import Post, Tag, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'image', 'published_at']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['published_at', 'author']
    search_fields = ['title', 'text']
    raw_id_fields = ['author', 'likes', 'tags']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'published_at']
    list_filter = ['published_at']
    search_fields = ['text']
    raw_id_fields = ['author', 'post']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title']
