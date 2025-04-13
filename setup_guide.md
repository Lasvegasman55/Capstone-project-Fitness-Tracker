# FitTrack Setup Guide

This guide will help you set up and run your Personal Fitness Tracker application.

## 1. Setup Virtual Environment and Install Dependencies

```bash
# Create a virtual environment
python -m venv fitness_env

# Activate the virtual environment
# On Windows
fitness_env\Scripts\activate
# On macOS/Linux
source fitness_env/bin/activate

# Install dependencies
pip install django djangorestframework django-crispy-forms crispy-bootstrap5 pillow
```

## 2. Run Migrations

```bash
# Generate migration files
python manage.py makemigrations tracker

# Apply migrations to create database tables
python manage.py migrate
```

## 3. Create a Superuser

```bash
# Create an admin user
python manage.py createsuperuser
```

## 4. Populate Exercise Data

Create a data loading script to populate initial exercise categories and exercises.

Create a file called `tracker/management/commands/load_exercises.py`:

```python
from django.core.management.base import BaseCommand
from tracker.models import ExerciseCategory, Exercise

class Command(BaseCommand):
    help = 'Loads initial exercise data'

    def handle(self, *args, **kwargs):
        # Create categories
        categories = {
            'cardio': 'Cardiovascular exercises',
            'strength': 'Strength training exercises',
            'flexibility': 'Flexibility and mobility exercises',
            'balance': 'Balance and stability exercises',
            'functional': 'Functional training exercises'
        }
        
        category_instances = {}
        for key, description in categories.items():
            category, created = ExerciseCategory.objects.get_or_create(
                name=key.title(),
                defaults={'description': description}
            )
            category_instances[key] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {key.title()}'))
            else:
                self.stdout.write(self.style.WARNING(f'Category exists: {key.title()}'))
        
        # Create exercises
        exercises = [
            # Cardio
            {'name': 'Running', 'category': 'cardio', 'primary_muscle_group': 'Legs', 'is_cardio': True},
            {'name': 'Cycling', 'category': 'cardio