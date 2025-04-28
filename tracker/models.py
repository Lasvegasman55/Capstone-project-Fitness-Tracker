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

class MuscleGroup(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

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

class FastingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fasting_sessions')
    
    # Fasting details
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    planned_duration = models.PositiveIntegerField(help_text="Planned fasting duration in hours")
    
    # Protocol choices
    PROTOCOL_CHOICES = [
        ('16_8', '16:8 (Leangains)'),
        ('18_6', '18:6'),
        ('20_4', '20:4 (Warrior Diet)'),
        ('5_2', '5:2 (5 normal days, 2 fasting days)'),
        ('custom', 'Custom'),
    ]
    protocol = models.CharField(max_length=10, choices=PROTOCOL_CHOICES, default='16_8')
    custom_hours = models.PositiveIntegerField(null=True, blank=True, help_text="For custom protocol, hours to fast")
    
    # Status
    is_active = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    
    # Notes/Journal
    notes = models.TextField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_time']
    
    def __str__(self):
        return f"{self.user.username}'s fast - {self.get_protocol_display()} ({self.start_time.date()})"
    
    def duration_in_hours(self):
        """Calculate actual duration of the fast in hours"""
        if self.end_time:
            delta = self.end_time - self.start_time
            return round(delta.total_seconds() / 3600, 1)  # Convert to hours
        return None
    
    def progress_percentage(self):
        """Calculate the current progress percentage of the fast"""
        if self.completed:
            return 100
            
        if not self.is_active:
            return 0
            
        current_time = timezone.now()
        elapsed = current_time - self.start_time
        elapsed_hours = elapsed.total_seconds() / 3600
        
        target_hours = self.custom_hours if self.protocol == 'custom' else {
            '16_8': 16,
            '18_6': 18,
            '20_4': 20,
            '5_2': 120,  # 5 days in hours
        }.get(self.protocol, 16)
        
        percentage = min(100, (elapsed_hours / target_hours) * 100)
        return round(percentage, 1)
    
    # Add this to tracker/models.py
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    is_user = models.BooleanField(default=True)  # True if from user, False if from AI
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.user.username}: {self.message[:30]}..."
    
