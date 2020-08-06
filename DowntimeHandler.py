from FileHandler import write_file, read_file, check_dir_existence, make_dir


class DowntimeScheduler(object):
    def __init__(self):
        self.default_schedule = {"Days": {"Monday": None,
                                          "Tuesday": None,
                                          "Wednesday": None,
                                          "Thursday": None,
                                          "Friday": None,
                                          "Saturday": None,
                                          "Sunday": None},
                                 "Reset Day": None}
        self.dir_path = "FileStorage/ServerSchedules/"
        self.days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    def load_schedule(self, message):
        path = self.dir_path + str(hash(message.guild))
        if check_dir_existence(path):
            schedule = read_file(path + "/schedule.pickle")
            return schedule
        else:
            make_dir(path)
            write_file(path + "/schedule.pickle", self.default_schedule)
            return self.default_schedule

    def save_schedule(self, message, schedule):
        path = self.dir_path + str(hash(message.guild))
        if check_dir_existence(path):
            write_file(path + "/schedule.pickle", schedule)
        else:
            make_dir(path)
            write_file(path + "/schedule.pickle", schedule)

    def find_days(self, message):
        message = [word.lower() for word in message]
        days = [day for day in message if day in self.days]
        return days[0].lower().capitalize() if len(days) > 0 else None

    @staticmethod
    def dictionary_to_string(dictionary):
        schedule = dictionary["Days"]
        return_string = ""
        for day in schedule:
            return_string += f"{day}: {schedule[day] if schedule[day] is not None else 'Free'}\n"
        return return_string

    def schedule_function(self, message):
        schedule = self.load_schedule(message)
        message_content = message.content.replace("!", "").split(" ")
        day = self.find_days(message_content)
        if message_content[0] == "dt" and len(message_content) == 1:
            return self.dictionary_to_string(schedule)
        elif day is not None and len(message_content) == 2:
            schedule_day = schedule["Days"][day]
            if schedule_day is None:
                schedule["Days"][day] = message.author.nick
                self.save_schedule(message, schedule)
                return f"Your day has been set to {day}"
            else:
                return f"The day has been already taken by {schedule_day}"
        elif len(message_content) > 1 and message_content[1] == "clear":
            if len(message_content) == 2:
                for role in message.author.roles:
                    if role.name == "DM":
                        self.save_schedule(message, self.default_schedule)
                        return "Schedule has been cleared"
                else:
                    return "You don't have sufficient permission to clear the schedule"
            elif day is not None:
                if message.author.nick == schedule["Days"][day] or schedule["Days"][day] is None:
                    schedule["Days"][day] = None
                    self.save_schedule(message, schedule)
                    return "The day has been cleared"
                return "You cannot delete a slot which doesn't belong to you"
