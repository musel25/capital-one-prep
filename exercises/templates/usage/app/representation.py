RATE_CENTS = 3


def invoice(workspace_id, month, samples, units):
    return {'workspace_id': workspace_id, 'month': month,
            'billable_samples': samples, 'units': units, 'charge_cents': units * RATE_CENTS}
