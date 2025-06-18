# --- FILE: blog_app/views.py ---
from django.contrib import messages # <--- Import messages
from django.db import IntegrityError
from .forms import NewsletterSubscriberForm # <--- Import the new form
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from .models import Post, Tag  # Corrected: Import models from the same app ('.')

def blog_home_view(request):
    """
    Renders the home page with various sections of posts.
    """
    # Base queryset for all published and active posts
    all_posts = Post.objects.filter(is_active=True, status=Post.Status.PUBLISHED)

    # Data for the hero section's floating cards
    hero_posts = all_posts.order_by('-publish_date')[:3]
    
    # "Trending" is defined as posts with the most engagement (likes + comments)
    trending_posts = all_posts.annotate(
        engagement=Count('appreciations') + Count('comments')
    ).order_by('-engagement')
    
    # "Latest Articles" are the most recently published
    latest_posts = all_posts.order_by('-publish_date')[:2]
    
    # "AI Suggestions" can be a random selection for now
    # Using order_by('?') can be slow on large databases. Consider a different strategy in production.
    ai_suggestions = all_posts.order_by('?')[:3] 

    # "From the Archives" features a hand-picked, recommended post
    archive_post = all_posts.filter(is_recommended=True).first()

    context = {
        'hero_posts': hero_posts,
        'trending_main': trending_posts.first(),
        'trending_sidebar': trending_posts[1:4],
        'latest_posts': latest_posts,
        'ai_suggestions': ai_suggestions,
        'archive_post': archive_post,
    }
    return render(request, 'blog_app/blog_home.html', context)


def blog_list_view(request):
    """
    Renders the list of all articles, with category filtering and pagination.
    """
    posts_list = Post.objects.filter(is_active=True, status=Post.Status.PUBLISHED)
    categories = Tag.objects.all()

    # Filter posts if a category is specified in the URL query parameters
    category_filter = request.GET.get('category')
    if category_filter and category_filter.lower() != 'all':
        posts_list = posts_list.filter(tags__name__iexact=category_filter)
    
    # Paginate the results, showing 9 posts per page
    paginator = Paginator(posts_list, 9)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'categories': categories,
        'current_category': category_filter,
    }
    return render(request, 'blog_app/blog_list.html', context)


def blog_detail_view(request, slug):
    """
    Renders the detail page for a single blog post.
    """

    # Retrieve the post or return a 404 error if not found/not published
    post = get_object_or_404(Post, slug=slug, is_active=True, status=Post.Status.PUBLISHED)
    
    # Find related posts based on shared tags
    post_tags_ids = post.tags.values_list('id', flat=True)
    related_posts = Post.objects.filter(tags__in=post_tags_ids)\
                                .exclude(id=post.id)\
                                .filter(is_active=True, status=Post.Status.PUBLISHED)\
                                .annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags', '-publish_date')[:2]

    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog_app/blog_dtl.html', context)


def about_author_view(request):
    """
    Renders the static 'About Me' page.
    """
    return render(request, 'blog_app/about_author.html')

def subscribe_view(request):
    if request.method == 'POST':
        # Get the URL of the page the user was on
        next_page = request.POST.get('next', '/') 
        form = NewsletterSubscriberForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Thank you for subscribing!')
            except IntegrityError:
                # This error occurs if the email is already in the database
                messages.warning(request, 'This email is already subscribed. Thank you!')
        else:
            # If the form is not valid (e.g., not a proper email)
            messages.error(request, 'Please enter a valid email address.')
        
        return redirect(next_page)
    
    # If it's a GET request, just redirect to the home page
    return redirect('blog_app:home')