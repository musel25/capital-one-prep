def reading(row):
    return {'id': row['id'], 'service_id': row['service_id'],
            'duration_ms': row['duration_us'] / 1000, 'status': row['status']}
