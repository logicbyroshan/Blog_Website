from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog-admin/', include('admin_app.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('blog_app:home')), name='logout'),
    path('', include('blog_app.urls', namespace='blog_app')),
    path('accounts/', include('accounts.urls')),]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
