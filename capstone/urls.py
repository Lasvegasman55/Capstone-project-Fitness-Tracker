from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tracker.views import welcome, fasting_dashboard, fasting_start, fasting_end, fasting_history
# Import all the fasting views directly

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome, name='welcome'),  # Set welcome page as home
    path('tracker/', include('tracker.urls')),  # Move tracker URLs under /tracker/
    path('fasting/', fasting_dashboard, name='fasting_dashboard'),
    path('fasting/start/', fasting_start, name='fasting_start'),
    path('fasting/end/<int:pk>/', fasting_end, name='fasting_end'),
    path('fasting/history/', fasting_history, name='fasting_history'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

