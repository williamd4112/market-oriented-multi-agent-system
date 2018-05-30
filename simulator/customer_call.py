
class CustomerCall(object):
    def __init__(self, start_pos, destination_pos, time):
        self.start_pos = start_pos
        self.destination_pos = destination_pos
        self.time = time

    def __repr__(self):
        return 'CustomerCall(time:{:.3f}, start_pos:({:.2f}, {:.2f}), dest_pos:({:.2f}, {:.2f}))'.format(self.time, self.start_pos[0], self.start_pos[1], 
                                                                                self.destination_pos[0], self.destination_pos[1])
