from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Creates default superuser if it does not exist'

    def handle(self, *args, **options):
        username = 'admin'
        password = 'password'
        email = 'admin@dressplatform.com'
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                user_type='admin'
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created superuser: {username}'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'Superuser {username} already exists'
                )
            )
