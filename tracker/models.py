from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.FloatField(null=True, blank=True, help_text="Height in cm")
    weight = models.FloatField(null=True, blank=True, help_text="Weight in kg")
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics', default='default.jpg')
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class Goal(models.Model):
    GOAL_TYPES = (
        ('weight', 'Weight Goal'),
        ('strength', 'Strength Goal'),
        ('endurance', 'Endurance Goal'),
        ('habit', 'Habit Formation'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)
    target_value = models.FloatField(null=True, blank=True, help_text="Target numerical value if applicable")
    target_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title

class ExerciseCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Exercise Categories"

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.ForeignKey(ExerciseCategory, on_delete=models.CASCADE, related_name='exercises')
    primary_muscle_group = models.CharField(max_length=50, blank=True)
    is_cardio = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    title = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)
    duration = models.DurationField(null=True, blank=True)
    calories_burned = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} on {self.date}"

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=0)
    
    # For strength exercises
    sets = models.PositiveSmallIntegerField(null=True, blank=True)
    reps = models.PositiveSmallIntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True, help_text="Weight in kg")
    
    # For cardio exercises
    distance = models.FloatField(null=True, blank=True, help_text="Distance in km")
    duration = models.DurationField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.exercise.name} in {self.workout.title}"

class BodyMeasurement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='measurements')
    date = models.DateField(default=timezone.now)
    weight = models.FloatField(null=True, blank=True, help_text="Weight in kg")
    body_fat_percentage = models.FloatField(null=True, blank=True)
    chest = models.FloatField(null=True, blank=True, help_text="Measurement in cm")
    waist = models.FloatField(null=True, blank=True, help_text="Measurement in cm")
    hips = models.FloatField(null=True, blank=True, help_text="Measurement in cm")
    arms = models.FloatField(null=True, blank=True, help_text="Measurement in cm")
    thighs = models.FloatField(null=True, blank=True, help_text="Measurement in cm")
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Measurements for {self.user.username} on {self.date}"

class NutritionEntry(models.Model):
    MEAL_TYPES = (
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nutrition_entries')
    date = models.DateField(default=timezone.now)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    food_name = models.CharField(max_length=100)
    calories = models.PositiveIntegerField()
    protein = models.FloatField(null=True, blank=True, help_text="Protein in grams")
    carbs = models.FloatField(null=True, blank=True, help_text="Carbohydrates in grams")
    fat = models.FloatField(null=True, blank=True, help_text="Fat in grams")
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.food_name} ({self.meal_type}) on {self.date}"
    
    class Meta:
        verbose_name_plural = "Nutrition Entries"

class WaterIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='water_intake')
    date = models.DateField(default=timezone.now)
    amount = models.FloatField(help_text="Amount in ml")
    time = models.TimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.amount}ml on {self.date}"