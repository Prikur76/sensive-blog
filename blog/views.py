from django.shortcuts import render
from django.db.models import Count
from django.http import HttpResponse

from blog.models import Comment, Post, Tag


def get_most_popular_posts(count=5):
    return  Post.objects.prefetch_related('author').annotate(
        total_likes=Count('likes')
    ).order_by('-total_likes')[:count]


def get_most_fresh_posts(count=5):
    return Post.objects.prefetch_related('author').order_by('-published_at')[:count]


def get_most_popular_tags(count=5):
    return Tag.objects.prefetch_related('posts').annotate(
        posts_with_tag=Count('posts')
    ).order_by('-posts_with_tag')[:count]


def serialize_post(post):
    # post_tags = Post.objects.prefetch_related('tags').get(id=post.id).tags.all()
    post_tags = post.tags.all()

    return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': Comment.objects.filter(post=post).count(),
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in post_tags],
        'first_tag_title': post_tags.first().title,
    }


def serialize_tag(tag):
    return {
        'title': tag.title,
        'posts_with_tag': Post.objects.filter(tags=tag).count(),
    }


def index(request):

    most_fresh_posts = get_most_fresh_posts().prefetch_related('tags')
    most_popular_posts = get_most_popular_posts().prefetch_related('tags')
    most_popular_tags = get_most_popular_tags()

    context = {
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
        'page_posts': [serialize_post(post) for post in most_fresh_posts],
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comment.objects.filter(post=post)
    serialized_comments = [
        {
            'text': comment.text,
            'published_at': comment.published_at,
            'author': comment.author.username,
        } for comment in comments
    ]

    likes_count = post.likes.all().count()
    related_tags = post.tags.all()

    serialized_post = {
        'title': post.title,
        'text': post.text,
        'author': post.author.username,
        'comments': serialized_comments,
        'likes_amount': likes_count,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in related_tags],
    }

    most_popular_posts = get_most_popular_posts()
    most_popular_tags = get_most_popular_tags()

    context = {
        'post': serialized_post,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'post-details.html', context)


def tag_filter(request, tag_title):
    tag = Tag.objects.get(title=tag_title)
    related_posts = tag.posts.all()[:20]
    most_popular_tags = get_most_popular_tags()
    most_popular_posts = get_most_popular_posts()

    context = {
        'tag': tag.title,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'posts': [serialize_post(post) for post in related_posts],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'posts-list.html', context)


def contacts(request):
    # позже здесь будет код для статистики заходов на эту страницу
    # и для записи фидбека
    return render(request, 'contacts.html', {})
