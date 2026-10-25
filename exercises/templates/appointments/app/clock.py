def minutes(value):
    hour, minute = value.split(':')
    return int(hour) * 60 + int(minute)


def clock_time(value):
    return f'{value // 60:02d}:{value % 60:02d}'


def slot(start, end):
    return {'start': clock_time(start), 'end': clock_time(end)}
