# --- FILE: blog_app/context_processors.py ---

def user_context(request):
    """
    Makes the 'user' object available in the context of every template.
    This ensures that the navbar, which is in a base template, always
    knows about the current authentication state.
    """
    # The request object already contains the user, we just need to pass it
    # to the context explicitly.
    return {
        'user': request.user
    }