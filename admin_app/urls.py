# --- FILE: admin_app/urls.py ---

from django.urls import path
from . import views


app_name = 'admin_app'  # Namespace for the admin app

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('blogs/', views.blog_list_view, name='blog_list'),
    path('activity/', views.blog_activity_view, name='activity'),
    path('blogs/write/', views.write_blog_view, name='write_blog'),
    path('blogs/plan/', views.plan_blog_view, name='plan_blog'), 
    path('blogs/edit/<int:post_id>/', views.write_blog_view, name='edit_blog'),
    path('blogs/edit/<int:post_id>/', views.write_blog_view, name='edit_blog'),
    path('blogs/delete/<int:post_id>/', views.delete_post_view, name='delete_post'),
    path('blogs/toggle-active/<int:post_id>/', views.toggle_post_active_view, name='toggle_post_active'),
    path('activity/toggle-pin/<int:comment_id>/', views.toggle_pin_comment_view, name='toggle_pin_comment'),
    path('activity/delete-comment/<int:comment_id>/', views.delete_comment_view, name='delete_comment'),
    path('blogs/recommend/', views.recommend_blog_view, name='recommend_blog'),

]