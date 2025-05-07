from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal

# Conversion constants
ML_TO_OZ = Decimal('0.033814')
OZ_TO_ML = Decimal('29.5735')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in cm
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in kg
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    water_unit_preference = models.CharField(
        max_length=2, 
        choices=[('ml', 'Milliliters'), ('oz', 'Ounces')], 
        default='ml'
    )
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    target_date = models.DateField()
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.name

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    duration = models.IntegerField(help_text="Duration in minutes")
    notes = models.TextField(blank=True)
    exercises = models.ManyToManyField(Exercise, through='WorkoutExercise')
    
    def __str__(self):
        return f"{self.user.username}'s workout on {self.date}"

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField()
    reps = models.IntegerField()
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.exercise.name} - {self.sets} sets of {self.reps}"

class FastingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    protocol = models.CharField(max_length=50, default="16:8")
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s fasting session on {self.start_time.date()}"

class BodyMeasurement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in kg
    body_fat_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    chest = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in cm
    waist = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in cm
    hips = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in cm
    arms = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in cm
    thighs = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in cm
    
    def __str__(self):
        return f"{self.user.username}'s measurements on {self.date}"

class NutritionEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    meal_type = models.CharField(max_length=50, choices=[
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack')
    ])
    food_item = models.CharField(max_length=100)
    calories = models.IntegerField()
    protein = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # in grams
    carbs = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # in grams
    fat = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # in grams
    
    def __str__(self):
        return f"{self.food_item} - {self.user.username} on {self.date}"

class WaterIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)  # Always stored in ml
    unit = models.CharField(
        max_length=2, 
        choices=[('ml', 'Milliliters'), ('oz', 'Ounces')], 
        default='ml'
    )
    
    def save(self, *args, **kwargs):
        # Convert to ml before saving if entered as oz
        if self.unit == 'oz':
            self.amount = self.amount * OZ_TO_ML
            self.unit = 'ml'  # Always store in ml
        super().save(*args, **kwargs)
    
    def get_amount_in_ml(self):
        return self.amount
    
    def get_amount_in_oz(self):
        return self.amount * ML_TO_OZ
    
    def get_amount_in_user_preferred_unit(self):
        try:
            preference = self.user.profile.water_unit_preference
            if preference == 'oz':
                return self.get_amount_in_oz()
            else:
                return self.amount
        except:
            return self.amount
    
    def __str__(self):
        return f"{self.user.username}'s water intake on {self.date} at {self.time}"
    
    class Meta:
        ordering = ['-date', '-time']
    
