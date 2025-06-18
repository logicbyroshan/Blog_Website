# --- FILE: accounts/forms.py ---

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    """
    A custom form for user registration that includes first name, last name, and email.
    """
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. A valid email address.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        """
        Add custom Tailwind CSS classes to the form fields.
        """
        super().__init__(*args, **kwargs)
        # The class for all form inputs
        input_class = 'form-input w-full p-3 rounded-md focus:outline-none focus:border-cyan-400'
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = input_class
            # Add specific placeholders if needed
            if field_name == 'username':
                field.widget.attrs['placeholder'] = 'e.g., roshandamor'
            if field_name == 'email':
                field.widget.attrs['placeholder'] = 'you@example.com'

# --- ADD THIS NEW FORM CLASS ---
class EditProfileForm(forms.ModelForm):
    """
    A form for users to edit their own profile information.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        """
        Add custom Tailwind CSS classes to the form fields.
        """
        super().__init__(*args, **kwargs)
        input_class = 'w-full bg-slate-900/70 border border-slate-700 rounded-lg p-2.5 text-white focus:outline-none focus:border-cyan-400'
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': input_class})