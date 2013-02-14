from exchange.models import Currency


def import_class(class_path):
    """imports and returns given class string.

    :param class_path: Class path as string
    :type class_path: str

    :returns: Class that has given path
    :rtype: class

    :Example:

    >>> import_class('collections.OrderedDict').__name__
    'OrderedDict'
    """
    try:
        from django.utils.importlib import import_module
        module_name = '.'.join(class_path.split(".")[:-1])
        mod = import_module(module_name)
        return getattr(mod, class_path.split(".")[-1])
    except Exception, detail:
        raise ImportError(detail)
