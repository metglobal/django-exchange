from django.core.management.base import BaseCommand, CommandError

from exchange.adapters import update


class Command(BaseCommand):
    """This command triggers exchane update process"""

    def handle(self, *args, **options):
        """Handle command"""

        try:
            update()
        except Exception, e:
            raise CommandError(e)
