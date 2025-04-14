from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tracker.views import welcome  # Import the welcome view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome, name='welcome'),  # Set welcome page as home
    path('tracker/', include('tracker.urls')),  # Move tracker URLs under /tracker/
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

