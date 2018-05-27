
class CustomerCall(object):
    def __init__(self, start_pos, destination_pos, distance):
        self.start_pos = start_pos
        self.destination_pos = destination_pos
        self.distance = distance

    def __repr__(self):
        return '({}, {}, {})'.format(self.start_pos, self.destination_pos, self.distance)
