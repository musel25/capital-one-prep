from fastapi import HTTPException

RATES = {
    'local': {'zone': 'local', 'base_cents': 300, 'per_unit_cents': 100, 'standard_days': 2},
    'regional': {'zone': 'regional', 'base_cents': 600, 'per_unit_cents': 150, 'standard_days': 4},
    'remote': {'zone': 'remote', 'base_cents': 1000, 'per_unit_cents': 250, 'standard_days': 7},
}


def rate_for(zone):
    if zone not in RATES:
        raise HTTPException(404, 'Delivery zone not found')
    return RATES[zone]
