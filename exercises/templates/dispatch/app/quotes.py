from .packages import billable_units
from .rates import RATES, SIGNATURE_CENTS


def quote(weights, service, signature):
    rate = RATES[service]
    units = billable_units(weights)
    transport = len(weights) * rate['base_cents'] + units * rate['unit_cents']
    signature_cents = SIGNATURE_CENTS if signature else 0
    return {'parcels': len(weights), 'billable_units': units, 'transport_cents': transport,
            'signature_cents': signature_cents, 'total_cents': transport + signature_cents}
