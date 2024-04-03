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

# def serialize_post(post):
#     post_tags = post.tags.all()
#     return {
#         'title': post.title,
#         'teaser_text': post.text[:200],
#         'author': post.author.username,
#         'comments_amount': Comment.objects.filter(post=post).count(),
#         'image_url': post.image.url if post.image else None,
#         'published_at': post.published_at,
#         'slug': post.slug,
#         'tags': [serialize_tag(tag) for tag in post_tags],
#         'first_tag_title': post_tags.first().title,
#     }


def serialize_tag(tag):
    context = {
        'title': tag.title,
        'posts_with_tag': tag.posts_count,
    }
    return context


def serialize_post_optimized(post):
    post_tags = post.tags.posts_count()
    context = {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': post.comments_count,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in post_tags],
        'first_tag_title': post_tags.first().title,
    }
    return context


def index(request):
    most_popular_posts = get_most_popular_posts()
    most_fresh_posts = get_most_fresh_posts()
    most_popular_tags = get_most_popular_tags()

    context = {
        'most_popular_posts': [
            serialize_post_optimized(post) for post in most_popular_posts
        ],
        'page_posts': [serialize_post_optimized(post) for post in most_fresh_posts],
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    post = Post.objects.popular().fetch_with_comments_count().get(slug=slug)
    comments = Comment.objects.filter(post=post)
    serialized_comments = [
        {
            'text': comment.text,
            'published_at': comment.published_at,
            'author': comment.author.username,
        } for comment in comments
    ]

    related_tags = post.tags.posts_count()

    serialized_post = {
        'title': post.title,
        'text': post.text,
        'author': post.author.username,
        'comments': serialized_comments,
        'likes_amount': post.likes_count,
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
            serialize_post_optimized(post) for post in most_popular_posts
        ]
    }
    return render(request, 'post-details.html', context)


def tag_filter(request, tag_title):
    tag = Tag.objects.get(title=tag_title)
    related_posts = tag.posts.all()[:20].fetch_with_comments_count()
    most_popular_tags = get_most_popular_tags()
    most_popular_posts = get_most_popular_posts()

    context = {
        'tag': tag.title,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'posts': [serialize_post_optimized(post) for post in related_posts],
        'most_popular_posts': [
            serialize_post_optimized(post) for post in most_popular_posts
        ],
    }
    return render(request, 'posts-list.html', context)


def contacts(request):
    # позже здесь будет код для статистики заходов на эту страницу
    # и для записи фидбека
    return render(request, 'contacts.html', {})
