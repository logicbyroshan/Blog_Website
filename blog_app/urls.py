# --- FILE: blog_app/urls.py ---

from django.urls import path
from . import views

app_name = 'blog_app'

urlpatterns = [
    # Example: /
    path('', views.blog_home_view, name='home'),
    path('articles/', views.blog_list_view, name='blog_list'),
    path('article/<slug:slug>/', views.blog_detail_view, name='blog_detail'),
    path('about/', views.about_author_view, name='about'),
    path('subscribe/', views.subscribe_view, name='subscribe'),

]