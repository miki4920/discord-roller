import datetime


class DowntimeScheduler(object):
    def __init__(self):
        self.schedule = {"Monday": None,
                         "Tuesday": None,
                         "Wednesday": None,
                         "Thursday": None,
                         "Friday": None,
                         "Saturday": None,
                         "Sunday": None}

    def schedule(self, message):
        if len(message) == 0:
            return self.schedule
        else:
            return 0
