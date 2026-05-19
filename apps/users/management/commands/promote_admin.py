from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Promote an existing user email to admin/staff access."

    def add_arguments(self, parser):
        parser.add_argument("email", help="Email address of the user to promote.")

    def handle(self, *args, **options):
        email = options["email"].strip().lower()
        User = get_user_model()

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist as exc:
            raise CommandError(f"No user found with email: {email}") from exc

        user.role = "admin"
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(update_fields=["role", "is_staff", "is_superuser", "is_active", "updated_at"])

        self.stdout.write(self.style.SUCCESS(f"Promoted {user.email} to admin."))
