from django.shortcuts import render
from django.db.models import Count
from django.http import HttpResponse

from blog.models import Post, Comment, Tag


def get_most_popular_posts(count=5):
    most_popular_posts = Post.objects.popular()[:count].fetch_with_comments_count()
    return most_popular_posts


def get_most_fresh_posts(count=5):
    most_fresh_posts = Post.objects.fresh()[:count].fetch_with_comments_count()
    return most_fresh_posts


def get_most_popular_tags(count=5):
    most_popular_tags = Tag.objects.popular()[:count].posts_count()
    return most_popular_tags


def serialize_tag(tag):
    context = {
        'title': tag['title'],
        'posts_with_tag': tag['posts_count']
    }
    return context


def serialize_comment(comment):
    serialized_comment = {
        'text': comment['text'],
        'published_at': comment['published_at'],
        'author': comment['author__username']
    }
    return serialized_comment


def serialize_post_optimized(post):
    post_tags = list(post.tags.posts_count().values('title', 'posts_count'))
    serialized_tags = [serialize_tag(tag) for tag in post_tags]
    context = {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': post.comments_count,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': serialized_tags,
        'first_tag_title': post_tags[0]['title'],
    }
    return context


def index(request):
    most_popular_posts = get_most_popular_posts()
    serialized_popular_posts = [
        serialize_post_optimized(post) for post in most_popular_posts
    ]

    most_fresh_posts = get_most_fresh_posts()
    serialized_fresh_posts = [
        serialize_post_optimized(post) for post in most_fresh_posts
    ]

    most_popular_tags = get_most_popular_tags().values('title', 'posts_count')
    serialized_tags = [
        serialize_tag(tag) for tag in most_popular_tags
    ]

    context = {
        'most_popular_posts': serialized_popular_posts,
        'page_posts': serialized_fresh_posts,
        'popular_tags': serialized_tags,
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    post = Post.objects.popular().fetch_with_comments_count().get(slug=slug)

    related_tags = list(post.tags.posts_count().values('title', 'posts_count'))
    serialized_tags = [serialize_tag(tag) for tag in related_tags]

    comments = Comment.objects.prefetch_related(
        'post', 'author__username'
    ).filter(post=post).values('author__username', 'text', 'published_at')
    serialized_comments = [serialize_comment(comment) for comment in comments]

    serialized_post = {
        'title': post.title,
        'text': post.text,
        'author': post.author.username,
        'comments': serialized_comments,
        'likes_amount': post.likes_count,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': serialized_tags,
    }

    most_popular_tags = get_most_popular_tags().values('title', 'posts_count')
    serialized_popular_tags = [
        serialize_tag(tag) for tag in most_popular_tags
    ]

    most_popular_posts = get_most_popular_posts()
    serialized_posts = [serialize_post_optimized(post) for post in most_popular_posts]

    context = {
        'post': serialized_post,
        'popular_tags': serialized_popular_tags,
        'most_popular_posts': serialized_posts
    }
    return render(request, 'post-details.html', context)


def tag_filter(request, tag_title):
    tag = Tag.objects.get(title=tag_title)

    related_posts = tag.posts.all()[:20].fetch_with_comments_count()
    serialized_posts = [serialize_post_optimized(post) for post in related_posts]

    most_popular_tags = get_most_popular_tags().values('title', 'posts_count')
    serialized_tags = [serialize_tag(tag) for tag in most_popular_tags]

    most_popular_posts = get_most_popular_posts()
    serialized_popular_posts = [serialize_post_optimized(post) for post in most_popular_posts]

    context = {
        'tag': tag.title,
        'popular_tags': serialized_tags,
        'posts': serialized_posts,
        'most_popular_posts': serialized_popular_posts,
    }

    return render(request, 'posts-list.html', context)


def contacts(request):
    # позже здесь будет код для статистики заходов на эту страницу
    # и для записи фидбека
    return render(request, 'contacts.html', {})
