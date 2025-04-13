from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='tracker/logout.html'), name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
    
    # Goals
    path('goals/', views.goal_list, name='goal_list'),
    path('goals/new/', views.goal_create, name='goal_create'),
    path('goals/<int:pk>/edit/', views.goal_update, name='goal_update'),
    path('goals/<int:pk>/delete/', views.goal_delete, name='goal_delete'),
    path('goals/<int:pk>/complete/', views.goal_complete, name='goal_complete'),
    
    # Workouts
    path('workouts/', views.workout_list, name='workout_list'),
    path('workouts/new/', views.workout_create, name='workout_create'),
    path('workouts/<int:pk>/', views.workout_detail, name='workout_detail'),
    path('workouts/<int:pk>/edit/', views.workout_update, name='workout_update'),
    path('workouts/<int:pk>/delete/', views.workout_delete, name='workout_delete'),
    
    # Body Measurements
    path('measurements/', views.measurement_list, name='measurement_list'),
    path('measurements/new/', views.measurement_create, name='measurement_create'),
    path('measurements/<int:pk>/edit/', views.measurement_update, name='measurement_update'),
    path('measurements/<int:pk>/delete/', views.measurement_delete, name='measurement_delete'),
    
    # Nutrition
    path('nutrition/', views.nutrition_list, name='nutrition_list'),
    path('nutrition/new/', views.nutrition_create, name='nutrition_create'),
    path('nutrition/<int:pk>/edit/', views.nutrition_update, name='nutrition_update'),
    path('nutrition/<int:pk>/delete/', views.nutrition_delete, name='nutrition_delete'),
    
    # Water Intake
    path('water/', views.water_list, name='water_list'),
    path('water/add/', views.water_add, name='water_add'),
    path('water/<int:pk>/delete/', views.water_delete, name='water_delete'),
    
    # Analytics
    path('analytics/', views.analytics, name='analytics'),
]