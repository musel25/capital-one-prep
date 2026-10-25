from copy import deepcopy


def queue_key(team, status):
    return (team, status)


def cached_rows(store, team, status, load):
    key = queue_key(team, status)
    if key not in store.queue_cache:
        store.queue_cache[key] = deepcopy(load())
    return deepcopy(store.queue_cache[key])


def invalidate(store):
    store.queue_cache.clear()
