# --- FILE: blog_app/forms.py ---

from django import forms
from .models import NewsletterSubscriber

class NewsletterSubscriberForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'flex-grow bg-bg-dark border border-border-color rounded-lg px-4 py-3 text-white placeholder-paragraph-color focus:outline-none focus:border-accent-start transition-colors',
                'placeholder': 'Enter your email'
            })
        }