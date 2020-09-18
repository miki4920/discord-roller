from UtilityHandler import write_pickle, read_pickle, check_dir_existence, make_dir
from ErrorHandler import WrongCommandFormat


class DowntimeScheduler(object):
    def __init__(self):
        self.default_schedule = {"Days": {"Monday": None,
                                          "Tuesday": None,
                                          "Wednesday": None,
                                          "Thursday": None,
                                          "Friday": None,
                                          "Saturday": None,
                                          "Sunday": None},
                                 "Session Day": None}
        self.dir_path = "FileStorage/ServerSchedules/"
        self.days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    def load_schedule(self, message):
        path = self.dir_path + str(hash(message.guild))
        if check_dir_existence(path):
            schedule = read_pickle(path + "/schedule.pickle")
            return schedule
        else:
            make_dir(path)
            write_pickle(path + "/schedule.pickle", self.default_schedule)
            return self.default_schedule

    def save_schedule(self, message, schedule):
        path = self.dir_path + str(hash(message.guild))
        if check_dir_existence(path):
            write_pickle(path + "/schedule.pickle", schedule)
        else:
            make_dir(path)
            write_pickle(path + "/schedule.pickle", schedule)

    def find_days(self, message):
        message = [word.lower() for word in message]
        days = [day for day in message if day in self.days]
        return days[0].capitalize() if len(days) > 0 else None

    @staticmethod
    def find_schedule_users(schedule, message):
        user_dictionary = {None: None}
        for member in message.guild.members:
            if not member.bot:
                user_dictionary[member.id] = member.nick
        return user_dictionary

    @staticmethod
    def dictionary_to_string(schedule, id_to_nick):
        return_string = ""
        for day in schedule:
            return_string += f"{day}: {id_to_nick[schedule[day]] if schedule[day] is not None else 'Free'}\n"
        return return_string

    @staticmethod
    def slot_booked(schedule, message):
        for key in schedule:
            if schedule[key] == message.author.id:
                return key
        return None

    @staticmethod
    def check_permission(message):
        for role in message.author.roles:
            if role.name == "DM":
                return True
        return False

    def schedule_function(self, message):
        schedule = self.load_schedule(message)
        message_content = message.content.replace("!", "").lower().split(" ")
        day = self.find_days(message_content)
        id_to_nick = self.find_schedule_users(schedule["Days"], message)
        if len(message_content) == 1:
            return self.dictionary_to_string(schedule["Days"], id_to_nick)
        elif day is not None and "clear" not in message_content:
            schedule_day = schedule["Days"][day]
            booked_already = self.slot_booked(schedule["Days"], message)
            if schedule_day is None and (not booked_already or self.check_permission(message)):
                schedule["Days"][day] = message.author.id
                self.save_schedule(message, schedule)
                return f"Your day has been set to {day}"
            elif schedule_day is None and booked_already:
                return f"You have already booked a slot on {booked_already}"
            else:
                return f"The day has been already taken by {id_to_nick[schedule_day]}"
        elif "clear" in message_content:
            if day is None:
                if self.check_permission(message):
                    self.save_schedule(message, self.default_schedule)
                    return "Schedule has been cleared"
                else:
                    return "You don't have sufficient permission to clear the schedule"
            else:
                if message.author.id == schedule["Days"][day] or schedule["Days"][day] is None\
                        or self.check_permission(message):
                    schedule["Days"][day] = None
                    self.save_schedule(message, schedule)
                    return "The day has been cleared"
                return "You cannot delete a slot which doesn't belong to you"
        raise WrongCommandFormat(message_content)
