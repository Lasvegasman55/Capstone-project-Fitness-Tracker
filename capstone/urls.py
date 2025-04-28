from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from tracker.views import welcome

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome, name='welcome'),  # Set welcome page as home
    path('tracker/', include('tracker.urls')),  # Move tracker URLs under /tracker/
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
