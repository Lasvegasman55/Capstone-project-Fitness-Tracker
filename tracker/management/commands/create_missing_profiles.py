from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tracker.models import Profile

class Command(BaseCommand):
    help = 'Creates profile objects for users that do not have one'

    def handle(self, *args, **kwargs):
        users_without_profile = []
        for user in User.objects.all():
            try:
                # Try to access the profile
                user.profile
            except Profile.DoesNotExist:
                # Create profile if it doesn't exist
                users_without_profile.append(user)
                Profile.objects.create(user=user)
                self.stdout.write(self.style.SUCCESS(f'Created profile for user: {user.username}'))
        
        if not users_without_profile:
            self.stdout.write(self.style.SUCCESS('All users have profiles already.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Created {len(users_without_profile)} profiles.'))
