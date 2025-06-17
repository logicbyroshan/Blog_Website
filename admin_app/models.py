from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Post(models.Model):
    # ADD THE 'PLANNED' STATUS HERE
    class Status(models.TextChoices):
        PLANNED = 'PL', 'Planned'  # New status for blog ideas
        DRAFT = 'DF', 'Draft'
        SCHEDULED = 'SC', 'Scheduled'
        PUBLISHED = 'PB', 'Published'

    # ... (rest of your fields are fine) ...
    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=300, blank=True, null=True)
    slug = models.SlugField(max_length=250, unique_for_date='publish_date', help_text="A unique slug for the post URL.", blank=True)
    content = models.TextField(help_text="The main content of the blog post, written in Markdown or HTML.", blank=True)
    thumbnail = models.ImageField(upload_to='blog_thumbnails/', blank=True, null=True, help_text="The main image for the post.")
    
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    meta_description = models.TextField(max_length=160, blank=True, null=True, help_text="A short summary for SEO (150-160 characters).")

    # Set the default status to PLANNED when a new idea is created
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PLANNED)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    is_active = models.BooleanField(default=True, help_text="Controls if the post is visible on the site. Inactive posts are hidden.")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(default=timezone.now, help_text="The date and time the post will be or was published.")

    appreciations = models.ManyToManyField(User, related_name='appreciated_posts', blank=True)
    is_recommended = models.BooleanField(default=False, help_text="Featured or recommended posts appear in a special section.")

    class Meta:
        ordering = ['-publish_date']
        indexes = [ models.Index(fields=['-publish_date']), ]

    def __str__(self):
        return self.title

    @property
    def total_appreciations(self):
        return self.appreciations.count()


class Comment(models.Model):
    """Model for comments on a blog post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', help_text="The user who wrote the comment.")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_pinned = models.BooleanField(default=False, help_text="Pinned comments appear at the top of the comment section.")

    class Meta:
        ordering = ['-is_pinned', '-created_at'] # Pinned comments first, then newest
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post}'


class NewsletterSubscriber(models.Model):
    """Model for users who subscribe to the newsletter."""
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email