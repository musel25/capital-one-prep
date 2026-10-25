from fastapi.testclient import TestClient

from app.main import create_app


def test_dataset_catalog_describes_export_size():
    client = TestClient(create_app())
    rows = client.get('/api/datasets').json()['items']
    assert [(row['id'], row['rows']) for row in rows] == [('visits', 240), ('tickets', 86)]


def test_unkeyed_submission_and_job_lookup():
    client = TestClient(create_app())
    result = client.post('/api/jobs', json={'dataset_id': 'tickets', 'format': 'json'})
    assert result.status_code == 201
    job = result.json()
    assert job['row_count'] == 86 and job['status'] == 'queued'
    assert client.get(f"/api/jobs/{job['id']}").json() == job
    assert client.get('/api/jobs').json() == {'items': [job]}


def test_bad_exports_leave_queue_unchanged():
    client = TestClient(create_app())
    assert client.post('/api/jobs', json={'dataset_id': 'unknown', 'format': 'csv'}).status_code == 404
    assert client.post('/api/jobs', json={'dataset_id': 'visits', 'format': 'xml'}).status_code == 422
    assert client.get('/api/jobs/missing').status_code == 404
    assert client.get('/api/jobs').json() == {'items': []}
