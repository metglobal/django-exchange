import functools
from datetime import datetime


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


def insert_many(objects, using="default"):
    """Insert list of Django objects in one SQL query. Objects must be
    of the same Django model. Note that save is not called and signals
    on the model are not raised.

    Mostly from: http://people.iola.dk/olau/python/bulkops.py
    """
    if not objects:
        return

    import django.db.models
    from django.db import connections
    from django.db import transaction
    con = connections[using]

    model = objects[0].__class__
    fields = [f for f in model._meta.fields
              if not isinstance(f, django.db.models.AutoField)]
    parameters = []
    for o in objects:
        params = tuple(f.get_db_prep_save(f.pre_save(o, True), connection=con)
                       for f in fields)
        parameters.append(params)

    table = model._meta.db_table
    column_names = ",".join(con.ops.quote_name(f.column) for f in fields)
    placeholders = ",".join(("%s",) * len(fields))
    con.cursor().executemany("insert into %s (%s) values (%s)"
                             % (table, column_names, placeholders), parameters)
    transaction.commit_unless_managed(using=using)


def update_many(objects, fields=[], using="default"):
    """Update list of Django objects in one SQL query, optionally only
    overwrite the given fields (as names, e.g. fields=["foo"]).
    Objects must be of the same Django model. Note that save is not
    called and signals on the model are not raised.

    Mostly from: http://people.iola.dk/olau/python/bulkops.py
    """
    if not objects:
        return

    import django.db.models
    from django.db import connections
    from django.db import transaction
    con = connections[using]

    names = fields
    meta = objects[0]._meta
    fields = [f for f in meta.fields
              if not isinstance(f, django.db.models.AutoField)
              and (not names or f.name in names)]

    if not fields:
        raise ValueError("No fields to update, field names are %s." % names)

    fields_with_pk = fields + [meta.pk]
    parameters = []
    for o in objects:
        parameters.append(tuple(f.get_db_prep_save(f.pre_save(o, True),
                          connection=con) for f in fields_with_pk))

    table = meta.db_table
    assignments = ",".join(("%s=%%s" % con.ops.quote_name(f.column))
                           for f in fields)
    con.cursor().executemany("update %s set %s where %s=%%s"
                             % (table, assignments,
                                con.ops.quote_name(meta.pk.column)),
                             parameters)
    transaction.commit_unless_managed(using=using)


def memoize(ttl=None):
    """ Cache the result of the function call with given args for until
        ttl (datetime.timedelta) expires.
    """
    def decorator(obj):
        cache = obj.cache = {}

        @functools.wraps(obj)
        def memoizer(*args, **kwargs):
            now = datetime.now()
            key = str(args) + str(kwargs)
            if key not in cache:
                cache[key] = (obj(*args, **kwargs), now)
            value, last_update = cache[key]
            if ttl and (now - last_update) > ttl:
                cache[key] = (obj(*args, **kwargs), now)
            return cache[key][0]
        return memoizer
    return decorator
