from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from exchange.utils import import_class
from exchange.adapters import BaseAdapter


class Command(BaseCommand):
    """This command triggers any
    :py:class:`exchange.adapters.BaseAdapter` implementation given by
    ``class`` option

    """
    option_list = BaseCommand.option_list + (
        make_option(
            '-c', '--class', dest='class', help='adapter class',
            default='exchange.adapters.'
                    'openexchangerates.OpenExchangeRatesAdapter'
        ),
    )

    def handle(self, *args, **options):
        """
        Handle command
        """
        adapter_class_name = options['class']
        try:
            adapter_class = import_class(adapter_class_name)
            adapter = adapter_class()
            if not isinstance(adapter, BaseAdapter):
                raise TypeError
        except (ImportError, TypeError), detail:
            raise CommandError("invalid adapter class: Detail: %s" % detail)
        adapter.update()
