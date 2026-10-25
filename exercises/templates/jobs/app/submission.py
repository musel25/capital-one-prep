from fastapi import HTTPException

from .queue import enqueue


def submit(registry, request, key):
    if key is not None and (not key.strip() or len(key) > 64):
        raise HTTPException(422, 'Idempotency-Key must contain 1 to 64 characters and not be blank')
    payload = request.model_dump()
    if key is not None and key in registry.keys:
        previous = registry.keys[key]
        if previous['payload'] != payload:
            raise HTTPException(409, 'Idempotency-Key belongs to another export')
        return previous['job']
    job = enqueue(registry, request)
    if key is not None:
        registry.keys[key] = {'payload': payload, 'job': job}
    return job
