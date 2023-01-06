from helper import database 
from datetime import datetime, timedelta


class Cooldown:
    def __init__(self, days=0, hours=0, minutes=0) -> None:
        self.days = days
        self.hours = hours
        self.minutes = minutes

    def update_user_timer(self, user_id, timer_name: str):
        current_time = datetime.now()

        #Check if data exists
        does_timer_exist = self.does_timer_exist(user_id, timer_name)

        if does_timer_exist is True:
            #Update
            sql = "UPDATE usertimers SET time=? WHERE user_id=? and timer_name=?"
            data_tuple = (current_time, user_id, timer_name)
            database.custom_excute(sql, data_tuple)
        else:
            #Create new
            data_tuple = (user_id, current_time, timer_name)
            database.add_to_database_without_keycheck(data_tuple, "usertimers")

        
    def check_if_on_cooldown(self, user_id, timer_name)->bool:
        current_time = datetime.now()

        #Check if data exists
        does_timer_exist = self.does_timer_exist(user_id, timer_name)

        if does_timer_exist is True:
            sql = "SELECT time FROM usertimers WHERE user_id=? and timer_name=?"
            bindings = [user_id, timer_name]
            timestamp_fetch = database.complex_query_fetchall(sql, bindings)
            print(timestamp_fetch)
            timestamp_list = database.convert_tuple_data_into_list(timestamp_fetch)
            print(timestamp_list)
            timestamp_str = timestamp_list[0]

            my_format = '%Y-%m-%d %H:%M:%S.%f'
            timestamp = datetime.strptime(timestamp_str, my_format)

            if self.days > 0:
                if current_time - timestamp > timedelta(days=self.days):
                    return True
                else:
                    return False
                    
            elif self.hours > 0:
                if current_time - timestamp > timedelta(hours=self.hours):
                    return True
                else:
                    return False

            elif self.minutes > 0:
                if current_time - timestamp > timedelta(minutes=self.minutes):
                    return True
                else:
                    return False
        else:
            return True

    def does_timer_exist(self, user_id, timer_name):
        #Check if data exists
        sql = "SELECT * FROM usertimers WHERE user_id=? and timer_name=?"
        bindings = [user_id, timer_name]
        timer_list = database.complex_query_fetchall(sql, bindings)
        print(user_id, timer_name)

        if len(timer_list) > 0:
            return True
        else:
            return False

    def get_cooldown_text(self, user_id, timer_name):
        if self.does_timer_exist(user_id, timer_name) is False:
            cooldown_text = "Collect your Nuggets!"
            return cooldown_text

        is_cooldown_active = self.check_if_on_cooldown(user_id, timer_name)
        print(is_cooldown_active)
        if is_cooldown_active == True:
            cooldown_text = "Nugget Collection Ready!"
            return cooldown_text

        current_time = datetime.now()
        sql = "SELECT time FROM usertimers WHERE user_id=? and timer_name=?"
        bindings_list = [user_id, timer_name]

        timestamp_fetch = database.complex_query_fetchall(sql, bindings_list)
        timestamp_list = database.convert_tuple_data_into_list(timestamp_fetch)
        timestamp_str = timestamp_list[0]


        my_format = '%Y-%m-%d %H:%M:%S.%f'

        timestamp = datetime.strptime(timestamp_str, my_format)
        
        if self.days > 0:
            remaining_time = timedelta(days=self.days) - (current_time - timestamp)
            days = remaining_time.total_seconds() / 86400
            hours = (remaining_time.total_seconds() % 86400) / 3600
            minutes = (remaining_time.total_seconds() % 3600) / 60
        elif self.hours > 0:
            # Calculate the remaining time in hours and minutes
            days = 0
            print(self.hours)
            print(self.minutes)
            remaining_time = timedelta(hours=self.hours) - (current_time - timestamp)
            print(remaining_time)
            hours = remaining_time.total_seconds() / 3600
            print(hours)
            minutes = (remaining_time.total_seconds() % 3600) / 60
            print(minutes)
            
        elif self.minutes > 0:
            days = 0
            hours = 0
            remaining_time = timedelta(minutes=self.minutes) - (current_time - timestamp)
            minutes = remaining_time.total_seconds() / 60

        #Round the times  
        if days < 1:
            days = round(days)
            
        else:
            days = 0

        if hours < 1:
            hours = 0
        else:
            hours = round(hours)
        
        if minutes < 1:
            minutes = 0
        else:
            minutes = round(minutes)
            

        print(days, hours, minutes)

        #Print only required text
        if days >= 1:

            # Print the remaining time in days hours and minutes
            cooldown_text = f"{days} days and {hours} hours and {minutes} minutes."
            return cooldown_text

        elif hours >= 1:
            # Print the remaining time in hours and minutes
            cooldown_text = f"{hours} hours and {minutes} minutes."

            return cooldown_text

        elif minutes >= 1:
            cooldown_text = f"{minutes} minutes."

            return cooldown_text

        else:
            cooldown_text = "PENDING"
            return cooldown_text
