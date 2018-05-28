from util.timeline import TimeLine, TimeLineEvent

if __name__ == '__main__':
    timeline = TimeLine()
    timeline.add_event(TimeLineEvent(0, 10, 'E0'))
    timeline.add_event(TimeLineEvent(11, 12, 'E1'))    
    timeline.add_event(TimeLineEvent(25, 30, 'E2'))
    timeline.add_event(TimeLineEvent(30, 33, 'E3'))

    assert (timeline.is_valid(TimeLineEvent(-2, 0, 'E')) == True)
    assert (timeline.is_valid(TimeLineEvent(-2, 5, 'E')) == False)
    assert (timeline.is_valid(TimeLineEvent(0, 5, 'E')) == False)
    assert (timeline.is_valid(TimeLineEvent(0, 11, 'E')) == False)
    assert (timeline.is_valid(TimeLineEvent(2, 5, 'E')) == False)
    assert (timeline.is_valid(TimeLineEvent(15, 30, 'E')) == False)
    assert (timeline.is_valid(TimeLineEvent(15, 20, 'E')) == True)
    assert (timeline.is_valid(TimeLineEvent(33, 35, 'E')) == True)
    assert (timeline.is_valid(TimeLineEvent(34, 35, 'E')) == True)

    print(timeline)

