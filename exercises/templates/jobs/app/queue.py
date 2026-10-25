from fastapi import HTTPException


def enqueue(registry, request):
    dataset = registry.datasets.get(request.dataset_id)
    if dataset is None:
        raise HTTPException(404, 'Dataset not found')
    job = {
        'id': f'job-{len(registry.jobs) + 1}',
        'dataset_id': dataset['id'],
        'format': request.format,
        'row_count': dataset['rows'],
        'status': 'queued',
    }
    registry.jobs[job['id']] = job
    return job
