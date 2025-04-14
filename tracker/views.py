from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Avg
from django.utils import timezone
from datetime import timedelta, date
from django.contrib.auth import login


from .models import (
    Profile, Goal, Exercise, ExerciseCategory, 
    Workout, WorkoutExercise, BodyMeasurement,
    NutritionEntry, WaterIntake
)
from .forms import (
    UserRegistrationForm, ProfileForm, GoalForm,
    WorkoutForm, WorkoutExerciseFormSet, BodyMeasurementForm,
    NutritionEntryForm, WaterIntakeForm
)

def welcome(request):
    """Display the welcome/landing page"""
    return render(request, 'tracker/welcome/index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a profile for the user
            Profile.objects.create(user=user)
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
    
    context = {
        'recent_workouts': recent_workouts,
        'active_goals': active_goals,
        'latest_measurement': latest_measurement,
        'workouts_this_week': workouts_this_week,
        'calories_today': calories_today,
        'water_today': water_today
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
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
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
    
    context = {
        'intakes': intakes,
        'total_intake': total_intake,
        'selected_date': selected_date,
    }
    
    return render(request, 'tracker/water/water_list.html', context)

@login_required
def water_add(request):
    if request.method == 'POST':
        form = WaterIntakeForm(request.POST)
        if form.is_valid():
            water = form.save(commit=False)
            water.user = request.user
            water.save()
            messages.success(request, f'Added {water.amount}ml of water!')
            return redirect('water_list')
    else:
        form = WaterIntakeForm(initial={
            'date': timezone.now().date(),
            'time': timezone.now().time(),
            'amount': 250  # Default to 250ml
        })
    
    return render(request, 'tracker/water/water_form.html', {'form': form})

@login_required
def water_delete(request, pk):
    intake = get_object_or_404(WaterIntake, pk=pk, user=request.user)
    
    if request.method == 'POST':
        intake.delete()
        messages.success(request, 'Water intake entry deleted!')
        return redirect('water_list')
    
    return render(request, 'tracker/water/water_confirm_delete.html', {'intake': intake})

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