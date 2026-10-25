def summary(samples, service_id):
    rows = samples.for_service(service_id)
    return {'service_id': service_id, 'count': len(rows),
            'error_count': sum(row['status'] == 'error' for row in rows),
            'slow_count': sum(row['duration_us'] >= 200000 for row in rows)}
