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

    def find_days(self, message):
        message = message.split(" ")
        message = [word.lower().capitalize() for word in message]
        days = [day for day in message if day in self.schedule]
        return [days[0] if len(days) > 0 else None][0]

    def schedule_function(self, message):
        message_content = message.content[3:]
        day = self.find_days(message_content)
        if "schedule" in message_content.split(" "):
            self.scheduled_day = day
            if self.scheduled_day in self.schedule:
                return "Your scheduled day has been set to: " + self.scheduled_day
            else:
                return "Your scheduled day is not a day of the week, please use full day names."
        elif self.scheduled_day is None:
            return "You haven't set up schedule day yet, please use \"!dt schedule\" to schedule your day."
        elif len(message_content) == 0:
            return self.schedule
        else:
            self.schedule[day] = str(message.author.nick).split('#')[0]
            return f"Your day has been set to {day}"
