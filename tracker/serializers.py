from rest_framework import serializers
from .models import Profile, Goal, Exercise, Workout, FastingSession, BodyMeasurement, NutritionEntry, WaterIntake

# Profile serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'height', 'weight', 'date_of_birth', 'profile_picture']

# Goal serializer
class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'user', 'title', 'description', 'goal_type', 
                  'target_value', 'target_date', 'created_at', 
                  'completed', 'completed_at']

# Exercise serializer
class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'category', 
                  'primary_muscle_group', 'is_cardio']

# Workout serializer
class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'user', 'title', 'notes', 'date', 
                  'duration', 'calories_burned']

# Fasting session serializer
class FastingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FastingSession
        fields = ['id', 'user', 'start_time', 'end_time', 
                  'planned_duration', 'protocol', 'custom_hours',
                  'is_active', 'completed', 'notes', 
                  'created_at', 'updated_at']
        
    # Add additional methods if needed
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Add calculated fields
        if instance.is_active:
            representation['progress_percentage'] = instance.progress_percentage()
        if instance.end_time:
            representation['duration_in_hours'] = instance.duration_in_hours()
        return representation

# Body measurement serializer
class BodyMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyMeasurement
        fields = ['id', 'user', 'date', 'weight', 'body_fat_percentage',
                  'chest', 'waist', 'hips', 'arms', 'thighs', 'notes']

# Nutrition entry serializer
class NutritionEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionEntry
        fields = ['id', 'user', 'date', 'meal_type', 'food_name',
                  'calories', 'protein', 'carbs', 'fat', 'notes']

# Water intake serializer
class WaterIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterIntake
        fields = ['id', 'user', 'date', 'amount', 'time']