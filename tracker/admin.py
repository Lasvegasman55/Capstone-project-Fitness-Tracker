from django.contrib import admin
from .models import (
    Profile, Goal, ExerciseCategory, Exercise, 
    Workout, WorkoutExercise, BodyMeasurement,
    NutritionEntry, WaterIntake
)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'height', 'weight')
    search_fields = ('user__username',)

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'goal_type', 'target_date', 'completed')
    list_filter = ('goal_type', 'completed')
    search_fields = ('title', 'user__username')

@admin.register(ExerciseCategory)
class ExerciseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'primary_muscle_group', 'is_cardio')
    list_filter = ('category', 'is_cardio')
    search_fields = ('name', 'description')

class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 1

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date', 'duration')
    list_filter = ('date',)
    search_fields = ('title', 'user__username')
    inlines = [WorkoutExerciseInline]

@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'workout', 'sets', 'reps', 'weight')
    list_filter = ('exercise__category',)

@admin.register(BodyMeasurement)
class BodyMeasurementAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'weight', 'body_fat_percentage')
    list_filter = ('date',)
    search_fields = ('user__username',)

@admin.register(NutritionEntry)
class NutritionEntryAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'user', 'date', 'meal_type', 'calories')
    list_filter = ('date', 'meal_type')
    search_fields = ('food_name', 'user__username')

@admin.register(WaterIntake)
class WaterIntakeAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'amount', 'time')
    list_filter = ('date',)
    search_fields = ('user__username',)