
class CustomerCall(object):
    def __init__(self, start_pos, destination_pos, time):
        self.start_pos = start_pos
        self.destination_pos = destination_pos
        self.time = time

    def __repr__(self):
        return 'CustomerCall(time:{}, start_pos:{}, dest_pos:{})'.format(self.time, self.start_pos, self.destination_pos)
