from django.core.management.base import BaseCommand
from payments.models import Staff  # Replace with your app name


class Command(BaseCommand):
    help = "Import a chat ID into the Staff model"

    def handle(self, *args, **kwargs):
        chat_id = 322641207  # Your chat ID
        staff_member, created = Staff.objects.get_or_create(chat_id=chat_id)

        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Chat ID {chat_id} has been added to the database.")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Chat ID {chat_id} already exists in the database.")
            )
