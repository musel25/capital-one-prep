class Registry:
    def __init__(self):
        self.datasets = {
            'visits': {'id': 'visits', 'name': 'Museum visits', 'rows': 240},
            'tickets': {'id': 'tickets', 'name': 'Support tickets', 'rows': 86},
        }
        self.jobs = {}
        self.keys = {}
