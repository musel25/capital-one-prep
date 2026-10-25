from .catalog import product


def line_discount(subtotal_cents, percent):
    return subtotal_cents * percent // 100


def preview(request):
    lines = []
    for item in request.lines:
        subtotal = product(item.sku)['unit_cents'] * item.quantity
        discount = line_discount(subtotal, request.discount_percent)
        lines.append({'sku': item.sku, 'quantity': item.quantity, 'subtotal_cents': subtotal,
                      'discount_cents': discount, 'total_cents': subtotal - discount})
    return {'lines': lines, **{field: sum(line[field] for line in lines)
                              for field in ('subtotal_cents', 'discount_cents', 'total_cents')}}
