from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Avg
from django.utils import timezone
from datetime import timedelta, date
from django.contrib.auth import login
from dotenv import load_dotenv
from django.shortcuts import render
from django.http import JsonResponse
from decimal import Decimal

# Load environment variables
load_dotenv()
import os

# REST Framework imports
from rest_framework import viewsets
from .serializers import (
    ProfileSerializer, GoalSerializer, ExerciseSerializer, 
    WorkoutSerializer, FastingSessionSerializer, BodyMeasurementSerializer,
    NutritionEntrySerializer, WaterIntakeSerializer
)

from .models import (
    Profile, Goal, Exercise, ExerciseCategory, 
    Workout, WorkoutExercise, BodyMeasurement,
    NutritionEntry, WaterIntake, FastingSession,
    ChatMessage  # Make sure this is imported
)
from .forms import (
    UserRegistrationForm, ProfileForm, GoalForm,
    WorkoutForm, WorkoutExerciseFormSet, BodyMeasurementForm,
    NutritionEntryForm, WaterIntakeForm
)

# Constants for unit conversion
ML_TO_OZ = Decimal('0.033814')
OZ_TO_ML = Decimal('29.5735')

def welcome(request):
    """Display the welcome/landing page"""
    return render(request, 'tracker/welcome/index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Use get_or_create instead of create to prevent unique constraint error
            Profile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, f'Account created successfully. Welcome to FitTrack!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'tracker/register.html', {'form': form})

@login_required
def dashboard(request):
    # Recent workouts
    recent_workouts = Workout.objects.filter(user=request.user).order_by('-date')[:5]
    
    # In-progress goals
    active_goals = Goal.objects.filter(user=request.user, completed=False).order_by('target_date')[:5]
    
    # Latest body measurements
    latest_measurement = BodyMeasurement.objects.filter(
        user=request.user
    ).order_by('-date').first()
    
    # Workout stats
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    workouts_this_week = Workout.objects.filter(
        user=request.user, 
        date__gte=start_of_week
    ).count()
    
    # Nutrition summary for today
    today_nutrition = NutritionEntry.objects.filter(
        user=request.user,
        date=today
    )
    calories_today = today_nutrition.aggregate(Sum('calories'))['calories__sum'] or 0
    
    # Water intake today
    water_today = WaterIntake.objects.filter(
        user=request.user,
        date=today
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Convert water to oz if user prefers oz
    water_unit_preference = getattr(request.user.profile, 'water_unit_preference', 'ml')
    if water_unit_preference == 'oz':
        water_today_display = water_today * ML_TO_OZ
    else:
        water_today_display = water_today
    
    # Get active fasting session if any
    active_fasting = FastingSession.objects.filter(
        user=request.user,
        is_active=True
    ).first()
    
    context = {
        'recent_workouts': recent_workouts,
        'active_goals': active_goals,
        'latest_measurement': latest_measurement,
        'workouts_this_week': workouts_this_week,
        'calories_today': calories_today,
        'water_today': water_today_display,
        'water_unit': water_unit_preference,
        'active_fasting': active_fasting
    }
    
    return render(request, 'tracker/dashboard.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'tracker/profile.html', {'form': form})

# Goals Views
@login_required
def goal_list(request):
    active_goals = Goal.objects.filter(user=request.user, completed=False).order_by('target_date')
    completed_goals = Goal.objects.filter(user=request.user, completed=True).order_by('-completed_at')
    
    context = {
        'active_goals': active_goals,
        'completed_goals': completed_goals
    }
    
    return render(request, 'tracker/goals/goal_list.html', context)

@login_required
def goal_create(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, 'Goal created successfully!')
            return redirect('goal_list')
    else:
        form = GoalForm()
    
    return render(request, 'tracker/goals/goal_form.html', {'form': form})

@login_required
def goal_update(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Goal updated successfully!')
            return redirect('goal_list')
    else:
        form = GoalForm(instance=goal)
    
    return render(request, 'tracker/goals/goal_form.html', {'form': form})

@login_required
def goal_complete(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    goal.completed = True
    goal.completed_at = timezone.now()
    goal.save()
    messages.success(request, f'Congratulations on completing your goal: {goal.title}!')
    return redirect('goal_list')

@login_required
def goal_delete(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Goal deleted successfully!')
        return redirect('goal_list')
    return render(request, 'tracker/goals/goal_confirm_delete.html', {'goal': goal})

# Workout Views
@login_required
def workout_list(request):
    workouts = Workout.objects.filter(user=request.user).order_by('-date')
    return render(request, 'tracker/workouts/workout_list.html', {'workouts': workouts})

@login_required
def workout_detail(request, pk):
    workout = get_object_or_404(Workout, id=pk, user=request.user)
    exercises = workout.exercises.all().order_by('order')
    
    context = {
        'workout': workout,
        'exercises': exercises
    }
    
    return render(request, 'tracker/workouts/workout_detail.html', context)

@login_required
def workout_create(request):
    if request.method == 'POST':
        workout_form = WorkoutForm(request.POST)
        exercise_formset = WorkoutExerciseFormSet(request.POST, prefix='exercises')
        
        if workout_form.is_valid() and exercise_formset.is_valid():
            workout = workout_form.save(commit=False)
            workout.user = request.user
            workout.save()
            
            # Save exercises
            exercises = exercise_formset.save(commit=False)
            for i, exercise_form in enumerate(exercises):
                exercise_form.workout = workout
                exercise_form.order = i
                exercise_form.save()
            
            messages.success(request, 'Workout logged successfully!')
            return redirect('workout_detail', pk=workout.pk)
    else:
        workout_form = WorkoutForm(initial={'date': timezone.now().date()})
        exercise_formset = WorkoutExerciseFormSet(prefix='exercises')
    
    context = {
        'workout_form': workout_form,
        'exercise_formset': exercise_formset,
        'exercises': Exercise.objects.all()
    }
    
    return render(request, 'tracker/workouts/workout_form.html', context)

@login_required
def workout_update(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    
    if request.method == 'POST':
        workout_form = WorkoutForm(request.POST, instance=workout)
        exercise_formset = WorkoutExerciseFormSet(
            request.POST, 
            prefix='exercises',
            queryset=WorkoutExercise.objects.filter(workout=workout)
        )
        
        if workout_form.is_valid() and exercise_formset.is_valid():
            workout_form.save()
            
            # First, delete existing exercise relationships
            WorkoutExercise.objects.filter(workout=workout).delete()
            
            # Save new exercises
            exercises = exercise_formset.save(commit=False)
            for i, exercise_form in enumerate(exercises):
                exercise_form.workout = workout
                exercise_form.order = i
                exercise_form.save()
            
            messages.success(request, 'Workout updated successfully!')
            return redirect('workout_detail', pk=workout.pk)
    else:
        workout_form = WorkoutForm(instance=workout)
        exercise_formset = WorkoutExerciseFormSet(
            prefix='exercises',
            queryset=WorkoutExercise.objects.filter(workout=workout)
        )
    
    context = {
        'workout_form': workout_form,
        'exercise_formset': exercise_formset,
        'exercises': Exercise.objects.all(),
        'workout': workout
    }
    
    return render(request, 'tracker/workouts/workout_form.html', context)

@login_required
def workout_delete(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    
    if request.method == 'POST':
        workout.delete()
        messages.success(request, 'Workout deleted successfully!')
        return redirect('workout_list')
    
    return render(request, 'tracker/workouts/workout_confirm_delete.html', {'workout': workout})

# Body Measurement Views
@login_required
def measurement_list(request):
    measurements = BodyMeasurement.objects.filter(user=request.user).order_by('-date')
    return render(request, 'tracker/measurements/measurement_list.html', {'measurements': measurements})

@login_required
def measurement_create(request):
    if request.method == 'POST':
        form = BodyMeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.user = request.user
            measurement.save()
            messages.success(request, 'Measurement recorded successfully!')
            return redirect('measurement_list')
    else:
        form = BodyMeasurementForm(initial={'date': timezone.now().date()})
    
    return render(request, 'tracker/measurements/measurement_form.html', {'form': form})

@login_required
def measurement_update(request, pk):
    measurement = get_object_or_404(BodyMeasurement, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = BodyMeasurementForm(request.POST, instance=measurement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Measurement updated successfully!')
            return redirect('measurement_list')
    else:
        form = BodyMeasurementForm(instance=measurement)
    
    return render(request, 'tracker/measurements/measurement_form.html', {'form': form})

@login_required
def measurement_delete(request, pk):
    measurement = get_object_or_404(BodyMeasurement, pk=pk, user=request.user)
    
    if request.method == 'POST':
        measurement.delete()
        messages.success(request, 'Measurement deleted successfully!')
        return redirect('measurement_list')
    
    return render(request, 'tracker/measurements/measurement_confirm_delete.html', {'measurement': measurement})

# Nutrition Views
@login_required
def nutrition_list(request):
    # Default to today's entries
    selected_date = request.GET.get('date', timezone.now().date())
    if isinstance(selected_date, str):
        try:
            selected_date = date.fromisoformat(selected_date)
        except ValueError:
            selected_date = timezone.now().date()
    
    entries = NutritionEntry.objects.filter(
        user=request.user,
        date=selected_date
    ).order_by('meal_type')
    
    # Calculate totals
    totals = entries.aggregate(
        total_calories=Sum('calories'),
        total_protein=Sum('protein'),
        total_carbs=Sum('carbs'),
        total_fat=Sum('fat')
    )
    
    # Group by meal type
    meals = {}
    for meal_type, meal_name in NutritionEntry.MEAL_TYPES:
        meals[meal_name] = entries.filter(meal_type=meal_type)
    
    context = {
        'entries': entries,
        'meals': meals,
        'totals': totals,
        'selected_date': selected_date,
    }
    
    return render(request, 'tracker/nutrition/nutrition_list.html', context)

@login_required
def nutrition_create(request):
    if request.method == 'POST':
        form = NutritionEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, 'Food entry added successfully!')
            return redirect('nutrition_list')
    else:
        form = NutritionEntryForm(initial={'date': timezone.now().date()})
    
    return render(request, 'tracker/nutrition/nutrition_form.html', {'form': form})

@login_required
def nutrition_update(request, pk):
    entry = get_object_or_404(NutritionEntry, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = NutritionEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Food entry updated successfully!')
            return redirect('nutrition_list')
    else:
        form = NutritionEntryForm(instance=entry)
    
    return render(request, 'tracker/nutrition/nutrition_form.html', {'form': form})

@login_required
def nutrition_delete(request, pk):
    entry = get_object_or_404(NutritionEntry, pk=pk, user=request.user)
    
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Food entry deleted successfully!')
        return redirect('nutrition_list')
    
    return render(request, 'tracker/nutrition/nutrition_confirm_delete.html', {'entry': entry})

# Water Intake Views
@login_required
def water_list(request):
    selected_date = request.GET.get('date', timezone.now().date())
    if isinstance(selected_date, str):
        try:
            selected_date = date.fromisoformat(selected_date)
        except ValueError:
            selected_date = timezone.now().date()
            
    intakes = WaterIntake.objects.filter(
        user=request.user,
        date=selected_date
    ).order_by('time')
    
    total_intake = intakes.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Convert to ounces for display if needed
    total_intake_oz = total_intake * ML_TO_OZ
    
    # Get user's daily water goal from profile or use default
    daily_goal = getattr(request.user.profile, 'water_goal', 3000)  # Default to 3000ml if not set
    percentage = min(100, round((total_intake / daily_goal) * 100)) if total_intake else 0
    
    context = {
        'intakes': intakes,
        'total_intake': total_intake,
        'total_intake_oz': total_intake_oz,
        'selected_date': selected_date,
        'percentage': percentage,
        'daily_goal': daily_goal
    }
    
    return render(request, 'tracker/water/water_list.html', context)

@login_required
def water_add(request):
    if request.method == 'POST':
        form = WaterIntakeForm(request.POST)
        if form.is_valid():
            water = form.save(commit=False)
            water.user = request.user
            
            # Handle unit conversion if needed
            amount = form.cleaned_data['amount']
            unit = request.POST.get('unit', 'ml')
            
            if unit == 'oz':
                # Convert from oz to ml for storage
                water.amount = amount * OZ_TO_ML
            
            water.save()
            
            if unit == 'oz':
                messages.success(request, f'Added {amount} oz of water!')
            else:
                messages.success(request, f'Added {amount} ml of water!')
                
            return redirect('water_list')
    else:
        # Get user's preferred unit
        unit_preference = getattr(request.user.profile, 'water_unit_preference', 'ml')
        
        # Default amount based on user preference
        default_amount = 250 if unit_preference == 'ml' else 8  # 8oz ~= 240ml
        
        form = WaterIntakeForm(initial={
            'date': timezone.now().date(),
            'time': timezone.now().time(),
            'amount': default_amount
        })
    
    context = {
        'form': form,
        'unit': getattr(request.user.profile, 'water_unit_preference', 'ml')
    }
    
    return render(request, 'tracker/water/water_form.html', context)

@login_required
def water_edit(request, pk):
    intake = get_object_or_404(WaterIntake, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = WaterIntakeForm(request.POST, instance=intake)
        if form.is_valid():
            water = form.save(commit=False)
            
            # Handle unit conversion if needed
            amount = form.cleaned_data['amount']
            unit = request.POST.get('unit', 'ml')
            
            if unit == 'oz':
                # Convert from oz to ml for storage
                water.amount = amount * OZ_TO_ML
                
            water.save()
            messages.success(request, 'Water intake updated successfully!')
            return redirect('water_list')
    else:
        # Get user's preferred unit
        unit_preference = getattr(request.user.profile, 'water_unit_preference', 'ml')
        
        # Convert amount based on preference for display
        if unit_preference == 'oz':
            display_amount = intake.amount * ML_TO_OZ
        else:
            display_amount = intake.amount
            
        form = WaterIntakeForm(instance=intake, initial={
            'amount': display_amount
        })
    
    context = {
        'form': form,
        'intake': intake,
        'unit': getattr(request.user.profile, 'water_unit_preference', 'ml')
    }
    
    return render(request, 'tracker/water/water_form.html', context)

@login_required
def water_delete(request, pk):
    intake = get_object_or_404(WaterIntake, pk=pk, user=request.user)
    
    if request.method == 'POST':
        intake.delete()
        messages.success(request, 'Water intake entry deleted!')
        return redirect('water_list')
    
    return render(request, 'tracker/water/water_confirm_delete.html', {'intake': intake})

@login_required
def update_water_preference(request):
    """View to update user's water unit preference."""
    if request.method == 'POST':
        preference = request.POST.get('water_unit_preference')
        
        if preference in ['ml', 'oz']:
            profile = request.user.profile
            profile.water_unit_preference = preference
            profile.save()
            
            messages.success(request, f'Water unit preference updated to {preference}!')
            
            # If AJAX request, return JSON response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
        
        # Redirect back to water list
        return redirect('water_list')
    
    # If not POST, redirect to water list
    return redirect('water_list')

# Analytics and Reports
@login_required
def analytics(request):
    # Get date range (default to last 30 days)
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Workout statistics
    workout_count = Workout.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    ).count()
    
    # Weight tracking over time
    weight_data = BodyMeasurement.objects.filter(
        user=request.user,
        date__range=[start_date, end_date],
        weight__isnull=False
    ).order_by('date').values('date', 'weight')
    
    # Average daily nutrition
    nutrition_data = NutritionEntry.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    ).values('date').annotate(
        daily_calories=Sum('calories'),
        daily_protein=Sum('protein'),
        daily_carbs=Sum('carbs'),
        daily_fat=Sum('fat')
    ).order_by('date')
    
    # Most common exercises
    exercise_data = WorkoutExercise.objects.filter(
        workout__user=request.user,
        workout__date__range=[start_date, end_date]
    ).values('exercise__name').annotate(count=Sum('sets')).order_by('-count')[:10]
    
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'workout_count': workout_count,
        'weight_data': list(weight_data),
        'nutrition_data': list(nutrition_data),
        'exercise_data': list(exercise_data)
    }
    
    return render(request, 'tracker/analytics.html', context)

# Fasting Views
@login_required
def fasting_dashboard(request):
    # Get active fasting session
    active_session = FastingSession.objects.filter(
        user=request.user,
        is_active=True
    ).first()
    
    # Get recent fasting history
    recent_sessions = FastingSession.objects.filter(
        user=request.user,
        is_active=False
    ).order_by('-start_time')[:5]
    
    # Calculate streak (consecutive completed sessions)
    streak = 0
    for session in FastingSession.objects.filter(
        user=request.user,
        is_active=False,
        completed=True
    ).order_by('-end_time'):
        streak += 1
    
    context = {
        'active_session': active_session,
        'recent_sessions': recent_sessions,
        'streak': streak
    }
    
    return render(request, 'tracker/fasting/dashboard.html', context)

@login_required
def fasting_start(request):
    # Check if there's already an active session
    existing_active = FastingSession.objects.filter(
        user=request.user, 
        is_active=True
    ).exists()
    
    if existing_active:
        messages.warning(request, 'You already have an active fasting session')
        return redirect('fasting_dashboard')
    
    if request.method == 'POST':
        # Extract data from form
        protocol = request.POST.get('protocol')
        custom_hours = request.POST.get('custom_hours')
        
        # Create new fasting session
        session = FastingSession(
            user=request.user,
            start_time=timezone.now(),
            protocol=protocol,
            is_active=True
        )
        
        # Set planned duration based on protocol
        if protocol == 'custom':
            try:
                custom_hours = int(custom_hours)
                session.custom_hours = custom_hours
                session.planned_duration = custom_hours
            except (ValueError, TypeError):
                messages.error(request, 'Invalid custom hours value')
                return redirect('fasting_start')
        else:
            protocol_hours = {
                '16_8': 16,
                '18_6': 18,
                '20_4': 20,
                '5_2': 120  # 5 days in hours
            }.get(protocol, 16)
            session.planned_duration = protocol_hours
        
        session.save()
        messages.success(request, f'Started a new {session.get_protocol_display()} fasting session!')
        return redirect('fasting_dashboard')
    
    return render(request, 'tracker/fasting/start.html', {'protocols': FastingSession.PROTOCOL_CHOICES})

@login_required
def fasting_end(request, pk):
    session = get_object_or_404(FastingSession, pk=pk, user=request.user, is_active=True)
    
    if request.method == 'POST':
        notes = request.POST.get('notes', '')
        completed = request.POST.get('completed') == 'true'
        
        session.is_active = False
        session.completed = completed
        session.end_time = timezone.now()
        session.notes = notes
        session.save()
        
        if completed:
            messages.success(request, 'Congratulations on completing your fast!')
        else:
            messages.info(request, 'Your fasting session has been ended early.')
        
        return redirect('fasting_dashboard')
    
    return render(request, 'tracker/fasting/end.html', {'session': session})

@login_required
def fasting_history(request):
    sessions = FastingSession.objects.filter(
        user=request.user
    ).order_by('-start_time')
    
    # Calculate stats
    total_sessions = sessions.count()
    completed_sessions = sessions.filter(completed=True).count()
    completion_rate = round((completed_sessions / total_sessions) * 100) if total_sessions > 0 else 0
    
    longest_session = sessions.filter(completed=True).order_by('-planned_duration').first()
    
    context = {
        'sessions': sessions,
        'total_sessions': total_sessions,
        'completed_sessions': completed_sessions,
        'completion_rate': completion_rate,
        'longest_session': longest_session
    }
    
    return render(request, 'tracker/fasting/history.html', context)

# Chat with AI Assistant
@login_required
def chat_view(request):
    # Get chat history
    messages_history = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
    
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()
        
        if user_message:
            # Save user message
            ChatMessage.objects.create(
                user=request.user,
                is_user=True,
                message=user_message
            )
            
            # Get AI response
            ai_response = get_ai_response(request.user, user_message)
            
            # Save AI response
            ChatMessage.objects.create(
                user=request.user,
                is_user=False,
                message=ai_response
            )
            
            return redirect('chat')
    
    return render(request, 'tracker/chat/chat.html', {'messages': messages_history})

def get_ai_response(user, message):
    """Get response from AI service without external API dependency"""
    try:
        # Get user context information
        recent_workouts = Workout.objects.filter(user=user).order_by('-date')[:3]
        active_goals = Goal.objects.filter(user=user, completed=False)[:3]
        latest_measurement = BodyMeasurement.objects.filter(user=user).order_by('-date').first()
        
        # Create rule-based responses based on keywords
        message_lower = message.lower()
        
        if 'chest' in message_lower and ('workout' in message_lower or 'exercise' in message_lower):
            return "For chest development, the best exercises include bench press (flat, incline, and decline), push-ups, dumbbell flyes, and cable crossovers. Aim for 3-4 sets of 8-12 reps for hypertrophy, or 4-6 reps for strength. Make sure to incorporate proper form and adequate rest between workouts."
        
        elif 'workout' in message_lower:
            if recent_workouts:
                return f"I see you've recently done these workouts: {', '.join([w.title for w in recent_workouts])}. Would you like suggestions for your next workout?"
            else:
                return "You haven't logged any workouts recently. Would you like some workout suggestions to get started?"
        
        elif 'goal' in message_lower:
            if active_goals:
                return f"You're currently working on these goals: {', '.join([g.title for g in active_goals])}. Keep up the good work!"
            else:
                return "You don't have any active goals. Setting specific fitness goals can help keep you motivated!"
        
        elif 'weight' in message_lower or 'measurement' in message_lower:
            if latest_measurement and hasattr(latest_measurement, 'weight') and latest_measurement.weight:
                return f"Your most recent weight measurement was {latest_measurement.weight} kg. Remember that weight is just one metric of fitness progress!"
            else:
                return "You haven't recorded any recent measurements. Regular tracking can help you see your progress over time."
        
        elif 'water' in message_lower or 'hydration' in message_lower:
            return "Staying hydrated is crucial for fitness! Aim for at least 2-3 liters of water daily, more during intense workouts."
        
        elif 'nutrition' in message_lower or 'diet' in message_lower or 'food' in message_lower:
            return "A balanced diet is essential for fitness. Focus on lean proteins, complex carbohydrates, healthy fats, and plenty of fruits and vegetables. Remember to adjust your caloric intake based on your fitness goals."
     
        elif 'motivation' in message_lower or 'tired' in message_lower or 'giving up' in message_lower:
            return "Remember why you started! Every workout gets you closer to your goals, even on tough days. Try mixing up your routine if you're feeling unmotivated."
        
        else:
            return "I'm here to help with your fitness journey! You can ask me about workouts, goals, nutrition, or measurements, or ask for general fitness advice."
    
    except Exception as e:
        return f"I'm sorry, I had trouble processing your request: {str(e)}. Try asking something about workouts, goals, or measurements."

# API ViewSets
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    def get_queryset(self):
        # Only return the current user's profile
        return Profile.objects.filter(user=self.request.user)

class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    
    def get_queryset(self):
        # Only return the current user's goals
        return Goal.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set the user when creating
        serializer.save(user=self.request.user)

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    
    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FastingSessionViewSet(viewsets.ModelViewSet):
    queryset = FastingSession.objects.all()
    serializer_class = FastingSessionSerializer
    
    def get_queryset(self):
        return FastingSession.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BodyMeasurementViewSet(viewsets.ModelViewSet):
    queryset = BodyMeasurement.objects.all()
    serializer_class = BodyMeasurementSerializer
    
    def get_queryset(self):
        return BodyMeasurement.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NutritionEntryViewSet(viewsets.ModelViewSet):
    queryset = NutritionEntry.objects.all()
    serializer_class = NutritionEntrySerializer
    
    def get_queryset(self):
        return NutritionEntry.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WaterIntakeViewSet(viewsets.ModelViewSet):
    queryset = WaterIntake.objects.all()
    serializer_class = WaterIntakeSerializer
    
    def get_queryset(self):
        return WaterIntake.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@login_required
def clear_chat(request):
    if request.method == 'POST':
        # Delete all chat messages for this user
        ChatMessage.objects.filter(user=request.user).delete()
        messages.success(request, 'Chat history cleared!')
    return redirect('chat')

def profile_view(request):
    return render(request, 'tracker/profile.html')

