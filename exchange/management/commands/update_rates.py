from django.core.management.base import BaseCommand, CommandError

from exchange.conversion import update_rates


class Command(BaseCommand):
    """This command triggers exchane update process"""

    def handle(self, *args, **options):
        """Handle command"""

        try:
            update_rates()
        except Exception, e:
            raise CommandError(e)
