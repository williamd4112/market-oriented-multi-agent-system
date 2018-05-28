
class CustomerCall(object):
    def __init__(self, start_pos, destination_pos, distance, time):
        self.start_pos = start_pos
        self.destination_pos = destination_pos
        self.distance = distance
        self.time = time

    def __repr__(self):
        return '(time:{}, start_pos:{}, dest_pos:{}, distance:{})'.format(self.time, self.start_pos, self.destination_pos, self.distance)
