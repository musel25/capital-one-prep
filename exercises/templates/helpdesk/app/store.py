class Store:
    def __init__(self):
        self.tickets = {
            't-101': {'id': 't-101', 'subject': 'Printer cannot connect', 'status': 'open'},
            't-102': {'id': 't-102', 'subject': 'Monitor flickers', 'status': 'open'},
            't-103': {'id': 't-103', 'subject': 'New starter access', 'status': 'new'},
        }
        self.comments = [
            {'ticket_id': 't-102', 'sequence': 2, 'author': 'Sam', 'body': 'The cable was replaced.'},
            {'ticket_id': 't-101', 'sequence': 3, 'author': 'Jo', 'body': 'The printer is on the guest network.'},
        ]
        self.transitions = [
            {'ticket_id': 't-101', 'sequence': 1, 'actor': 'Mina', 'previous': 'new', 'current': 'open'},
        ]
        self.sequence = 3

    def next_sequence(self):
        self.sequence += 1
        return self.sequence
