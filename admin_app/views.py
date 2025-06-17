from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Post, Comment, Tag, NewsletterSubscriber
import calendar
from django.utils import timezone
from django.utils.text import slugify

# A simple check to ensure only staff members can access the admin panel.
# This provides a basic level of security.
def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def plan_blog_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            # Create a new Post with the 'PLANNED' status
            Post.objects.create(
                author=request.user,
                title=title,
                status=Post.Status.PLANNED
            )
    # Redirect back to the dashboard after processing
    return redirect('admin_app:dashboard')

@login_required
@user_passes_test(is_staff)
def recommend_blog_view(request):
    if request.method == 'POST':
        post_id_to_recommend = request.POST.get('post_to_recommend')
        post_id_to_unrecommend = request.POST.get('post_to_unrecommend')

        if post_id_to_recommend:
            post = get_object_or_404(Post, id=post_id_to_recommend)
            post.is_recommended = True
            post.save()
        
        if post_id_to_unrecommend:
            post = get_object_or_404(Post, id=post_id_to_unrecommend)
            post.is_recommended = False
            post.save()

    return redirect('admin_app:dashboard')
# Apply decorators to all views to protect them
# user_passes_test ensures only staff can access
# login_required ensures they are logged in first
@login_required
@user_passes_test(is_staff)
def dashboard_view(request):
    # ... (counts and chart data logic remains the same) ...
    published_count = Post.objects.filter(status=Post.Status.PUBLISHED).count()
    scheduled_count = Post.objects.filter(status=Post.Status.SCHEDULED).count()
    draft_count = Post.objects.filter(status=Post.Status.DRAFT).count()
    planned_posts = Post.objects.filter(status=Post.Status.PLANNED).order_by('-created_at')
    # Chart data logic...
    recent_posts_for_chart = Post.objects.filter(status=Post.Status.PUBLISHED).order_by('-publish_date')[:3]
    chart_labels = [post.title[:20] + '...' for post in recent_posts_for_chart]
    chart_views = [post.total_appreciations * 20 + 100 for post in recent_posts_for_chart] # Dummy data
    chart_appreciations = [post.total_appreciations for post in recent_posts_for_chart]
    chart_comments = [post.comments.count() for post in recent_posts_for_chart]
    chart_data = {
        'labels': chart_labels,
        'datasets': [
            {'label': 'Views', 'data': chart_views, 'backgroundColor': '#22d3ee', 'borderRadius': 4},
            {'label': 'Appreciations', 'data': chart_appreciations, 'backgroundColor': '#14b8a6', 'borderRadius': 4},
            {'label': 'Comments', 'data': chart_comments, 'backgroundColor': '#64748b', 'borderRadius': 4}
        ]
    }
    # Calendar logic...
    today = timezone.now()
    cal = calendar.Calendar()
    calendar_weeks = []
    for week in cal.monthdatescalendar(today.year, today.month):
        week_with_posts = []
        for day_date in week:
            posts_on_day = Post.objects.filter(publish_date__date=day_date).filter(Q(status=Post.Status.PUBLISHED) | Q(status=Post.Status.SCHEDULED))
            day_number = day_date.day if day_date.month == today.month else 0
            week_with_posts.append((day_number, posts_on_day))
        calendar_weeks.append(week_with_posts)

    # --- UPDATE THE DATA FOR THE TABS ---
    published_posts = Post.objects.filter(status=Post.Status.PUBLISHED)
    
    # In a real app, you would have a view count field. We'll simulate it by ordering by appreciations.
    popular_posts = published_posts.annotate(engagement=Count('appreciations') + Count('comments')).order_by('-engagement')[:5]
    latest_posts = published_posts.order_by('-publish_date')[:5]
    
    # Fetch recommended posts and posts that can be recommended
    recommended_posts = published_posts.filter(is_recommended=True)
    non_recommended_posts = published_posts.filter(is_recommended=False)

    context = {
        'published_count': published_count,
        'scheduled_count': scheduled_count,
        'draft_count': draft_count,
        'planned_posts': planned_posts,
        'chart_data': chart_data,
        'calendar_weeks': calendar_weeks,
        'calendar_month_name': today.strftime('%B'),
        'calendar_year': today.year,
        
        # Pass the updated querysets to the template
        'popular_posts': popular_posts,
        'latest_posts': latest_posts,
        'recommended_posts': recommended_posts,
        'non_recommended_posts': non_recommended_posts,
    }
    return render(request, 'admin_app/admin-dash.html', context)


# --- UPDATE blog_list_view ---
@login_required
@user_passes_test(is_staff)
def blog_list_view(request):
    """
    Displays lists of all posts, categorized by their status.
    """
    # Fetch posts and order them correctly for each section
    published_posts = Post.objects.filter(status=Post.Status.PUBLISHED).order_by('-publish_date')
    scheduled_posts = Post.objects.filter(status=Post.Status.SCHEDULED).order_by('publish_date')
    draft_posts = Post.objects.filter(status=Post.Status.DRAFT).order_by('-updated_at')
    
    context = {
        'published_posts': published_posts,
        'scheduled_posts': scheduled_posts,
        'draft_posts': draft_posts,
    }
    return render(request, 'admin_app/blog_list.html', context)

# --- NEW VIEW ---
@login_required
@user_passes_test(is_staff)
def toggle_post_active_view(request, post_id):
    """
    Toggles the is_active boolean field for a given post.
    """
    post = get_object_or_404(Post, id=post_id)
    # This view is triggered by a form submission
    if request.method == 'POST':
        post.is_active = not post.is_active
        post.save()
    return redirect('admin_app:blog_list')

# --- NEW VIEW ---
@login_required
@user_passes_test(is_staff)
def delete_post_view(request, post_id):
    """
    Deletes a post.
    """
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
    return redirect('admin_app:blog_list')


# blog_activity_view and write_blog_view remain the same for now
# ...
@login_required
@user_passes_test(is_staff)
def blog_activity_view(request):
    total_appreciations = Post.objects.aggregate(total=Count('appreciations'))['total']
    total_comments = Comment.objects.count()
    registered_users = User.objects.all()
    subscribers = NewsletterSubscriber.objects.all()
    all_posts_with_comments = Post.objects.filter(comments__isnull=False).distinct()
    comments = Comment.objects.order_by('-is_pinned', '-created_at')
    context = {'total_appreciations': total_appreciations, 'total_comments': total_comments, 'registered_users': registered_users, 'subscribers': subscribers, 'all_posts_with_comments': all_posts_with_comments, 'comments': comments,}
    return render(request, 'admin_app/blog_activity.html', context)

@login_required
@user_passes_test(is_staff)
def blog_activity_view(request):
    """
    Shows community activity and handles comment filtering.
    """
    # Overall statistics
    total_appreciations = Post.objects.aggregate(total=Count('appreciations'))['total'] or 0
    total_comments = Comment.objects.count()
    registered_users = User.objects.all().order_by('-date_joined')
    subscribers = NewsletterSubscriber.objects.all().order_by('-subscribed_at')

    # Get all posts that have at least one comment for the filter dropdown
    all_posts_with_comments = Post.objects.filter(comments__isnull=False).distinct()
    
    # Filter comments based on the selected post from the dropdown
    selected_post_id = request.GET.get('post_id')
    comments = Comment.objects.select_related('post', 'author').order_by('-is_pinned', '-created_at')

    if selected_post_id:
        comments = comments.filter(post__id=selected_post_id)

    context = {
        'total_appreciations': total_appreciations,
        'total_comments': total_comments,
        'registered_users': registered_users,
        'subscribers': subscribers,
        'all_posts_with_comments': all_posts_with_comments,
        'comments': comments,
        'selected_post_id': selected_post_id, # To keep the dropdown selected
    }
    return render(request, 'admin_app/blog_activity.html', context)

# --- NEW VIEW ---
@login_required
@user_passes_test(is_staff)
def toggle_pin_comment_view(request, comment_id):
    """
    Toggles the is_pinned boolean field for a given comment.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment.is_pinned = not comment.is_pinned
        comment.save()
    # Redirect back to the activity page, preserving any filters
    post_id = request.POST.get('post_id')
    redirect_url = redirect('admin_app:activity').url
    if post_id:
        redirect_url += f'?post_id={post_id}'
    return redirect(redirect_url)

# --- NEW VIEW ---
@login_required
@user_passes_test(is_staff)
def delete_comment_view(request, comment_id):
    """
    Deletes a comment.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment.delete()
    # Redirect back to the activity page, preserving any filters
    post_id = request.POST.get('post_id')
    redirect_url = redirect('admin_app:activity').url
    if post_id:
        redirect_url += f'?post_id={post_id}'
    return redirect(redirect_url)


@login_required
@user_passes_test(is_staff)
def write_blog_view(request, post_id=None):
    """
    Handles both creating a new blog post and editing an existing one.
    """
    post = None
    if post_id:
        # If a post_id is provided, we are in 'edit' mode.
        post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        # --- Form Processing Logic ---
        title = request.POST.get('blog-title')
        subtitle = request.POST.get('blog-subtitle')
        content = request.POST.get('blog-editor-content')
        meta_description = request.POST.get('meta-description')
        tags_string = request.POST.get('blog-tags')
        
        # Determine the action and set the status accordingly
        action = request.POST.get('action')
        if action == 'publish':
            status = Post.Status.PUBLISHED
            publish_date = timezone.now()
        elif action == 'schedule':
            status = Post.Status.SCHEDULED
            # For a real app, you'd get this from a date picker input
            publish_date = timezone.now() + timezone.timedelta(days=7) 
        else: # Default to saving as draft
            status = Post.Status.DRAFT
            publish_date = post.publish_date if post else timezone.now()

        # Generate a slug from the title
        slug = slugify(title)

        # Create or Update the Post object
        if post: # Update existing post
            post.title = title
            post.subtitle = subtitle
            post.content = content
            post.meta_description = meta_description
            post.status = status
            post.publish_date = publish_date
            post.slug = slug # Update slug in case title changed
            if 'blog-thumbnail' in request.FILES:
                post.thumbnail = request.FILES['blog-thumbnail']
            post.save()
        else: # Create new post
            post = Post.objects.create(
                author=request.user,
                title=title,
                subtitle=subtitle,
                slug=slug,
                content=content,
                meta_description=meta_description,
                status=status,
                publish_date=publish_date,
                thumbnail=request.FILES.get('blog-thumbnail')
            )
        
        # Handle Tags
        post.tags.clear() # Clear existing tags to replace them
        if tags_string:
            tag_names = [name.strip() for name in tags_string.split(',') if name.strip()]
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)

        # Redirect to the blog list page after saving
        return redirect('admin_app:blog_list')

    # For a GET request, pass the post object to the template if it exists
    context = {
        'post': post
    }
    return render(request, 'admin_app/write_blog.html', context)