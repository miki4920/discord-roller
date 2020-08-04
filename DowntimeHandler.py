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
        self.scheduled_day = None
        self.next_session = None

    def schedule_function(self, message):
        message_content = message.content[3:]
        if self.scheduled_day is None:
            raise NoScheduledDay()
        elif message.split(" ")[0] == "schedule":
            self.scheduled_day = message.split(" ")[1].lower().capitalize()
            if self.scheduled_day in self.schedule:
                return "Your session day has been set to: " + self.scheduled_day
            else:
                return "Your session day is not a day of the week, please use full day names."
        elif len(message_content) == 0:
            return self.schedule
        else:
            return 0
