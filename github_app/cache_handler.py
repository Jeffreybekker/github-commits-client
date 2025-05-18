from django.core.cache import cache
import time

# Haalt data uit de cache of gebruikt de functie voor ophalen data.
# Geeft terug cache (van redis) of data van API terug.
# Geeft de duur mee hoe lang het duurde voor ophalen uit cache of API.
def get_cached_commits(key, fetch_function, timeout=300):
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
