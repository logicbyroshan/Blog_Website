# --- FILE: admin_app/urls.py ---

from django.urls import path
from . import views

# Namespacing the app's URLs is a best practice to avoid conflicts with other apps.
app_name = 'admin_app'

urlpatterns = [
    # Main Admin Pages
    # Example: /admin/
    path('', views.dashboard_view, name='dashboard'),
    # Example: /admin/blogs/
    path('blogs/', views.blog_list_view, name='blog_list'),
    # Example: /admin/activity/
    path('activity/', views.blog_activity_view, name='activity'),
    
    # Blog Post Creation & Editing
    # Example: /admin/blogs/write/
    path('blogs/write/', views.write_blog_view, name='write_blog'),
    # Example: /admin/blogs/edit/1/
    path('blogs/edit/<int:post_id>/', views.write_blog_view, name='edit_blog'),

    # Backend Actions for Posts
    # Handles the "Plan a New Blog" form submission from the dashboard
    path('blogs/plan/', views.plan_blog_view, name='plan_blog'),
    # Toggles the is_active field for a post
    path('blogs/toggle-active/<int:post_id>/', views.toggle_post_active_view, name='toggle_post_active'),
    # Deletes a post
    path('blogs/delete/<int:post_id>/', views.delete_post_view, name='delete_post'),
    # Handles the "Recommend Blog" form submission from the dashboard
    path('blogs/recommend/', views.recommend_blog_view, name='recommend_blog'),

    # Backend Actions for Comments
    # Toggles the is_pinned field for a comment
    path('activity/toggle-pin/<int:comment_id>/', views.toggle_pin_comment_view, name='toggle_pin_comment'),
    # Deletes a comment
    path('activity/delete-comment/<int:comment_id>/', views.delete_comment_view, name='delete_comment'),
]