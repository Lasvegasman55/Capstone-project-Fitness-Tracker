from django.core.management.base import BaseCommand
from django.db import transaction
from tracker.models import Exercise, ExerciseCategory, MuscleGroup

class Command(BaseCommand):
    help = 'Loads a predefined set of exercises into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to load exercises...')
        
        # Define exercise categories
        categories = {
            'strength': 'Strength Training',
            'cardio': 'Cardiovascular',
            'flexibility': 'Flexibility & Mobility',
            'bodyweight': 'Bodyweight Exercises'
        }
        
        # Create categories if they don't exist
        created_categories = {}
        for key, name in categories.items():
            category, created = ExerciseCategory.objects.get_or_create(
                name=name,
                defaults={'description': f'Exercises focusing on {name.lower()}'}
            )
            created_categories[key] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {name}'))
            else:
                self.stdout.write(f'Category already exists: {name}')
        
        # Define common muscle groups
        muscle_groups = {
            'chest': 'Chest',
            'back': 'Back',
            'shoulders': 'Shoulders',
            'legs': 'Legs',
            'arms': 'Arms',
            'abs': 'Abdominals',
            'full_body': 'Full Body',
            'cardio': 'Cardio'
        }
        
        # Create muscle groups if they don't exist
        created_groups = {}
        for key, name in muscle_groups.items():
            muscle_group, created = MuscleGroup.objects.get_or_create(name=name)
            created_groups[key] = muscle_group
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created muscle group: {name}'))
            else:
                self.stdout.write(f'Muscle group already exists: {name}')
        
        # Define exercises with their corresponding categories and muscle groups
        exercises = [
            # Strength exercises - Chest
            {
                'name': 'Bench Press', 
                'description': 'Lie on a flat bench and press weight upward.', 
                'category': created_categories['strength'],
                'primary_muscle_group': 'Chest',
                'is_cardio': False
            },
            {
                'name': 'Incline Bench Press', 
                'description': 'Bench press on an inclined bench.', 
                'category': created_categories['strength'],
                'primary_muscle_group': 'Chest',
                'is_cardio': False
            },
            {
                'name': 'Decline Bench Press', 
                'description': 'Bench press on a declined bench.', 
                'category': created_categories['strength'],
                'primary_muscle_group': 'Chest',
                'is_cardio': False
            },
            {
                'name': 'Dumbbell Flyes', 
                'description': 'Lie on bench and open arms wide with dumbbells.', 
                'category': created_categories['strength'],
                'primary_muscle_group': 'Chest',
                'is_cardio': False
            },
            
            # Strength exercises - Back
            {
                'name': 'Bent-Over Row', 
                'description': 'Bend at waist and pull weight to torso.', 
                'category': created_categories['strength'],
                'primary_muscle_group': 'Back',
                'is_cardio': False
            },
            {
                'name': 'Deadlift', 
                'description': 'Lifting barbell from ground to hips.', 
                'category': created_categories['strength'],
                'primary_muscle_group': 'Back',
                'is_cardio': False
            },
            {
                'name': 'Lat Pulldown', 
                'description': 'Using machine to pull bar down to chest.', 
                'category': created_categories['strength'],
                'primary_muscle_group': 'Back',
                'is_cardio': False
            },
            {
                'name': 'Seated Cable Row', 
                'description': 'Sitting and pulling cable toward abdomen.', 
                'category': created_categories['strength'],
                'primary_muscle_group': 'Back',
                'is_cardio': False
            },
            
            # Strength exercises - Shoulders
            {
                'name': 'Overhead Press', 
                'description': 'Press weight overhead from shoulders.', 
                'category': created_categories['strength'],
                'primary_muscle_group': 'Shoulders',
                'is_cardio': False
            },
            {
                'name': 'Lateral Raises', 
                'description': 'Raise weights to sides to shoulder height.', 
                'category': created_categories['strength'],
                'primary_muscle_group': 'Shoulders',
                'is_cardio': False
            },
            {
                'name': 'Front Raises', 
                'description': 'Raise weights in front to shoulder height.', 
                'category': created_categories['strength'],
                'primary_muscle_group': 'Shoulders',
                'is_cardio': False
            },
            {
                'name': 'Face Pulls', 
                'description': 'Pull rope to face level with elbows high.', 
                'category': created_categories['strength'],
                'primary_muscle_group': 'Shoulders',
                'is_cardio': False
            },
            
            # Strength exercises - Legs
            {
                'name': 'Squats', 
                'description': 'Bend knees and hips to lower body with weight on back.', 
                'category': created_categories['strength'],
                'primary_muscle_group': 'Legs',
                'is_cardio': False
            },
            {
                'name': 'Leg Press', 
                'description': 'Push weight away with legs using machine.', 
                'category': created_categories['strength'],
                'primary_muscle_group': 'Legs',
                'is_cardio': False
            },
            {
                'name': 'Lunges', 
                'description': 'Step forward and lower body with weights.', 
                'category': created_categories['strength'],
                'primary_muscle_group': 'Legs',
                'is_cardio': False
            },
            {
                'name': 'Leg Extensions', 
                'description': 'Using machine to extend legs forward.', 
                'category': created_categories['strength'],
                'primary_muscle_group': 'Legs',
                'is_cardio': False
            },
            
            # Strength exercises - Arms
            {
                'name': 'Bicep Curls', 
                'description': 'Curl weight from extended arm position.', 
                'category': created_categories['strength'],
                'primary_muscle_group': 'Arms',
                'is_cardio': False
            },
            {
                'name': 'Tricep Extensions', 
                'description': 'Extend arms to work triceps with weight.', 
                'category': created_categories['strength'],
                'primary_muscle_group': 'Arms',
                'is_cardio': False
            },
            {
                'name': 'Hammer Curls', 
                'description': 'Curl with neutral grip (thumbs up).', 
                'category': created_categories['strength'],
                'primary_muscle_group': 'Arms',
                'is_cardio': False
            },
            {
                'name': 'Skull Crushers', 
                'description': 'Lying and lowering weight to forehead.', 
                'category': created_categories['strength'],
                'primary_muscle_group': 'Arms',
                'is_cardio': False
            },
            
            # Bodyweight exercises
            {
                'name': 'Push-Ups', 
                'description': 'Classic bodyweight exercise for chest.', 
                'category': created_categories['bodyweight'],
                'primary_muscle_group': 'Chest',
                'is_cardio': False
            },
            {
                'name': 'Pull-Ups', 
                'description': 'Bodyweight exercise pulling up to a bar.', 
                'category': created_categories['bodyweight'],
                'primary_muscle_group': 'Back',
                'is_cardio': False
            },
            {
                'name': 'Dips', 
                'description': 'Lower and raise body between parallel bars.', 
                'category': created_categories['bodyweight'],
                'primary_muscle_group': 'Arms',
                'is_cardio': False
            },
            {
                'name': 'Bodyweight Squats', 
                'description': 'Squat using only body weight for resistance.', 
                'category': created_categories['bodyweight'],
                'primary_muscle_group': 'Legs',
                'is_cardio': False
            },
            {
                'name': 'Plank', 
                'description': 'Hold position similar to push-up start.', 
                'category': created_categories['bodyweight'],
                'primary_muscle_group': 'Abdominals',
                'is_cardio': False
            },
            {
                'name': 'Mountain Climbers', 
                'description': 'In plank, alternately bring knees to chest.', 
                'category': created_categories['bodyweight'],
                'primary_muscle_group': 'Abdominals',
                'is_cardio': True
            },
            
            # Cardio exercises
            {
                'name': 'Running', 
                'description': 'Basic cardio exercise.', 
                'category': created_categories['cardio'],
                'primary_muscle_group': 'Legs',
                'is_cardio': True
            },
            {
                'name': 'Cycling', 
                'description': 'Indoor or outdoor cycling.', 
                'category': created_categories['cardio'],
                'primary_muscle_group': 'Legs',
                'is_cardio': True
            },
            {
                'name': 'Jumping Rope', 
                'description': 'Skipping with a rope.', 
                'category': created_categories['cardio'],
                'primary_muscle_group': 'Full Body',
                'is_cardio': True
            },
            {
                'name': 'Swimming', 
                'description': 'Water-based cardio exercise.', 
                'category': created_categories['cardio'],
                'primary_muscle_group': 'Full Body',
                'is_cardio': True
            },
            {
                'name': 'Rowing', 
                'description': 'Using rowing machine or boat.', 
                'category': created_categories['cardio'],
                'primary_muscle_group': 'Back',
                'is_cardio': True
            },
            {
                'name': 'Elliptical', 
                'description': 'Low-impact cardio on elliptical machine.', 
                'category': created_categories['cardio'],
                'primary_muscle_group': 'Legs',
                'is_cardio': True
            },
            
            # Flexibility exercises
            {
                'name': 'Hamstring Stretch', 
                'description': 'Stretch targeting the hamstrings.', 
                'category': created_categories['flexibility'],
                'primary_muscle_group': 'Legs',
                'is_cardio': False
            },
            {
                'name': 'Quad Stretch', 
                'description': 'Stretch targeting the quadriceps.', 
                'category': created_categories['flexibility'],
                'primary_muscle_group': 'Legs',
                'is_cardio': False
            },
            {
                'name': 'Shoulder Stretch', 
                'description': 'Stretch targeting the shoulders.', 
                'category': created_categories['flexibility'],
                'primary_muscle_group': 'Shoulders',
                'is_cardio': False
            },
            {
                'name': 'Child\'s Pose', 
                'description': 'Yoga pose for back stretching.', 
                'category': created_categories['flexibility'],
                'primary_muscle_group': 'Back',
                'is_cardio': False
            },
            {
                'name': 'Cobra Stretch', 
                'description': 'Yoga pose for spine flexibility.', 
                'category': created_categories['flexibility'],
                'primary_muscle_group': 'Back',
                'is_cardio': False
            },
        ]
        
        # Use a transaction to ensure data integrity
        with transaction.atomic():
            # Create exercises
            created_count = 0
            existing_count = 0
            
            for exercise_data in exercises:
                exercise, created = Exercise.objects.get_or_create(
                    name=exercise_data['name'],
                    defaults={
                        'description': exercise_data['description'],
                        'category': exercise_data['category'],
                        'primary_muscle_group': exercise_data['primary_muscle_group'],
                        'is_cardio': exercise_data['is_cardio']
                    }
                )
                
                if created:
                    created_count += 1
                else:
                    existing_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {created_count} new exercises'))
        self.stdout.write(f'{existing_count} exercises already existed in the database')