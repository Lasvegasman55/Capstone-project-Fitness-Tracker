from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    Profile, Goal, Workout, WorkoutExercise, 
    BodyMeasurement, NutritionEntry, WaterIntake
)

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['height', 'weight', 'date_of_birth', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'description', 'goal_type', 'target_value', 'target_date']
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date'}),
        }

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['title', 'notes', 'date', 'duration', 'calories_burned']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'duration': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
        }

class WorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = ['exercise', 'sets', 'reps', 'weight', 'distance', 'duration', 'notes']
        widgets = {
            'duration': forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
        }

# This form will be used for adding multiple exercises to a workout
class WorkoutExerciseFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = WorkoutExercise.objects.none()

WorkoutExerciseFormSet = forms.modelformset_factory(
    WorkoutExercise, 
    form=WorkoutExerciseForm,
    formset=WorkoutExerciseFormSet,
    extra=3
)

class BodyMeasurementForm(forms.ModelForm):
    class Meta:
        model = BodyMeasurement
        fields = ['date', 'weight', 'body_fat_percentage', 'chest', 'waist', 'hips', 'arms', 'thighs', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class NutritionEntryForm(forms.ModelForm):
    class Meta:
        model = NutritionEntry
        fields = ['date', 'meal_type', 'food_name', 'calories', 'protein', 'carbs', 'fat', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class WaterIntakeForm(forms.ModelForm):
    class Meta:
        model = WaterIntake
        fields = ['date', 'amount', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }