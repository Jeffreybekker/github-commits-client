from django.core.cache import cache
import time


def get_cached_commits(key, fetch_function, timeout=300):
    """
    Haalt data uit de cache of roept een functie aan om de data op te halen.

    Parameters:
    - key (str): Unieke cache sleutel
    - fetch_function (callable): Functie die data ophaalt als het niet gecached is
    - timeout (int): Tijd in seconden om data te cachen (default = 1 uur)

    Returns:
    - Opgehaalde of gecachete data
    """
    start_time = time.perf_counter()
    cached_data = cache.get(key)
    if cached_data is not None:
        duration = (time.perf_counter() - start_time) * 1000  # in milliseconden
        return cached_data, duration, "cache"
    else:
        data = fetch_function()
        cache.set(key, data, timeout=timeout)
        duration = (time.perf_counter() - start_time) * 1000  # in milliseconden
        return data, duration, "API"
