from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path
from tracker.views import profile_view 

# Create a router for REST API
router = DefaultRouter()
router.register(r'profiles', views.ProfileViewSet)
router.register(r'goals', views.GoalViewSet)
router.register(r'exercises', views.ExerciseViewSet)
router.register(r'workouts', views.WorkoutViewSet)
router.register(r'fasting-sessions', views.FastingSessionViewSet)
router.register(r'measurements', views.BodyMeasurementViewSet)
router.register(r'nutrition', views.NutritionEntryViewSet)
router.register(r'water', views.WaterIntakeViewSet)

# Define URL patterns for your app
urlpatterns = [
    # Original URL patterns for web views
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('accounts/profile/', profile_view, name='profile'),
    # Goals URLs
    path('goals/', views.goal_list, name='goal_list'),
    path('goals/create/', views.goal_create, name='goal_create'),
    path('goals/<int:pk>/update/', views.goal_update, name='goal_update'),
    path('goals/<int:pk>/complete/', views.goal_complete, name='goal_complete'),
    path('goals/<int:pk>/delete/', views.goal_delete, name='goal_delete'),
    
    # Workout URLs
    path('workouts/', views.workout_list, name='workout_list'),
    path('workouts/create/', views.workout_create, name='workout_create'),
    path('workouts/<int:pk>/', views.workout_detail, name='workout_detail'),
    path('workouts/<int:pk>/update/', views.workout_update, name='workout_update'),
    path('workouts/<int:pk>/delete/', views.workout_delete, name='workout_delete'),
    
    # Measurements URLs
    path('measurements/', views.measurement_list, name='measurement_list'),
    path('measurements/create/', views.measurement_create, name='measurement_create'),
    path('measurements/<int:pk>/update/', views.measurement_update, name='measurement_update'),
    path('measurements/<int:pk>/delete/', views.measurement_delete, name='measurement_delete'),
    
    # Nutrition URLs
    path('nutrition/', views.nutrition_list, name='nutrition_list'),
    path('nutrition/create/', views.nutrition_create, name='nutrition_create'),
    path('nutrition/<int:pk>/update/', views.nutrition_update, name='nutrition_update'),
    path('nutrition/<int:pk>/delete/', views.nutrition_delete, name='nutrition_delete'),
    
    # Water URLs
    path('water/', views.water_list, name='water_list'),
    path('water/add/', views.water_add, name='water_add'),
    path('water/<int:pk>/delete/', views.water_delete, name='water_delete'),
    
    # Analytics URL
    path('analytics/', views.analytics, name='analytics'),
    
    # Fasting URLs
    path('fasting/', views.fasting_dashboard, name='fasting_dashboard'),
    path('fasting/start/', views.fasting_start, name='fasting_start'),
    path('fasting/end/<int:pk>/', views.fasting_end, name='fasting_end'),
    path('fasting/history/', views.fasting_history, name='fasting_history'),
    
    # REST API URLs
    path('api/', include(router.urls)),
    
    # API Authentication
    path('api-auth/', include('rest_framework.urls')),

    path('chat/', views.chat_view, name='chat'),

    path('tracker/chat/clear/', views.clear_chat, name='clear_chat'),
]