from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import (
    Profile, Goal, Exercise, Workout, WorkoutExercise, 
    FastingSession, BodyMeasurement, NutritionEntry, WaterIntake
)

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'height', 'weight', 'profile_picture', 'water_unit_preference']
        widgets = {
            'water_unit_preference': forms.Select(attrs={'class': 'form-control'})
        }

class GoalForm(forms.ModelForm):
    target_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Goal
        fields = ['title', 'description', 'target_date', 'completed']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'description', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class WorkoutForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Workout
        fields = ['date', 'duration', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class WorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = ['exercise', 'sets', 'reps', 'weight']

# Form for adding multiple exercises to a workout at once - can be used with formsets
WorkoutExerciseFormSet = forms.inlineformset_factory(
    Workout, WorkoutExercise, 
    form=WorkoutExerciseForm, 
    extra=1, 
    can_delete=True
)

class FastingSessionForm(forms.ModelForm):
    PROTOCOL_CHOICES = [
        ('16:8', '16:8 (Leangains)'),
        ('18:6', '18:6'),
        ('20:4', '20:4 (Warrior Diet)'),
        ('23:1', '23:1 (OMAD)'),
        ('5:2', '5:2 (Two days fasting)'),
        ('custom', 'Custom'),
    ]
    
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False
    )
    protocol = forms.ChoiceField(choices=PROTOCOL_CHOICES)
    
    class Meta:
        model = FastingSession
        fields = ['start_time', 'end_time', 'protocol', 'completed']

class BodyMeasurementForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = BodyMeasurement
        fields = ['date', 'weight', 'body_fat_percentage', 'chest', 'waist', 'hips', 'arms', 'thighs']

class NutritionEntryForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = NutritionEntry
        fields = ['date', 'meal_type', 'food_item', 'calories', 'protein', 'carbs', 'fat']

class WaterIntakeForm(forms.ModelForm):
    UNIT_CHOICES = [
        ('ml', 'Milliliters (ml)'),
        ('oz', 'Ounces (oz)'),
    ]
    
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=forms.DateField().clean
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        initial=forms.TimeField().clean
    )
    unit = forms.ChoiceField(
        choices=UNIT_CHOICES, 
        initial='ml',
        widget=forms.Select(attrs={'class': 'form-control unit-selector'})
    )
    
    class Meta:
        model = WaterIntake
        fields = ['date', 'time', 'amount', 'unit']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(WaterIntakeForm, self).__init__(*args, **kwargs)
        
        # Set the default unit to user's preference if available
        if user and hasattr(user, 'profile'):
            self.fields['unit'].initial = user.profile.water_unit_preference
    
    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        unit = cleaned_data.get('unit')
        
        if amount is not None and amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero")
        
        return cleaned_data

class WaterUnitPreferenceForm(forms.Form):
    UNIT_CHOICES = [
        ('ml', 'Milliliters (ml)'),
        ('oz', 'Ounces (oz)'),
    ]
    
    water_unit_preference = forms.ChoiceField(
        choices=UNIT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )