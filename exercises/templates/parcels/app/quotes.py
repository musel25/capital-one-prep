from fastapi import HTTPException
from .rates import rate_for


def quote(request):
    rate = rate_for(request.zone)
    units = (request.weight_grams + 499) // 500
    transport = rate['base_cents'] + units * rate['per_unit_cents']
    days = rate['standard_days']
    if request.service == 'express':
        transport *= 2
        days = (days + 1) // 2
    signature = 250 if request.signature else 0
    return {'zone': request.zone, 'service': request.service, 'billable_units': units,
            'transport_cents': transport, 'signature_cents': signature,
            'total_cents': transport + signature, 'estimated_days': days}
