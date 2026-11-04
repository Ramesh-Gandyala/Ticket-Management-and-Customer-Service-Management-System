from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from accounts.roles import ALL_ROLES


class Command(BaseCommand):
    help = "Create the standard support-platform role groups."

    def handle(self, *args, **options):
        created_count = 0

        for role_name in ALL_ROLES:
            _, created = Group.objects.get_or_create(name=role_name)
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f"Created role group: {role_name}"
                ))
            else:
                self.stdout.write(f"Role group already exists: {role_name}")

        self.stdout.write(self.style.SUCCESS(
            f"Role setup complete. {created_count} group(s) created."
        ))
