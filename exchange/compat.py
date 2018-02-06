from django.core import signals


def get_cache(backend, **kwargs):
    """
    Django cache backend compatibility
    """
    try:
        from django.core.cache import _create_cache
    except ImportError:
        from django.core.cache import get_cache as _get_cache
        return _get_cache(backend, **kwargs)

    cache = _create_cache(backend, **kwargs)
    signals.request_finished.connect(cache.close)
    return cache
