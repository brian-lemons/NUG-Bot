from helper import database
from helper import user
from operator import itemgetter

import random

def get_leaderboard()->str:
    print("here")
    #Grab the data
    sql = "SELECT user_name, nuggets FROM users ORDER BY nuggets ASC"
    info = database.complex_query_fetchall(sql)
    users_names = database.convert_tuple_data_into_list(info)
    nuggets = database.convert_tuple_data_into_list(info, 1)
    users_and_nuggets = zip(users_names, nuggets)

            
    #Convert data to list
    leaderboard_list = []
    for name, value in users_and_nuggets:
        user_tuple = (name,value)
        leaderboard_list.append(user_tuple)
            
    leaderboard = dict(leaderboard_list)

    #sort
    sorted_leaderboard = sorted(leaderboard.items(), key=itemgetter(1))
    sorted_leaderboard_dict = dict(sorted_leaderboard)

    leaderboard_text = ""
    position = 0
    position = len(sorted_leaderboard_dict) + 1


    for key, value in sorted_leaderboard_dict.items():
        position -= 1
        new_text = str(position) + ". " + key + " (" + str(value) + ") \n"
        leaderboard_text = new_text + leaderboard_text

    print(leaderboard_text)

    return leaderboard_text

def collect_daily_nuggets(user_id)->str:
    nugget_amount = random.randrange(25, 500)
    default_seed_amount = 1

    player = user.User(user_id)
    print(user_id)

    #Set new nugget amount
    current_nuggets = int(player.nuggets)
    new_nuggets = current_nuggets + nugget_amount

    player.set_nuggets(new_nuggets, user_id)

    #Refresh the user
    player = user.User(user_id)

    if nugget_amount <= 300:
        current_seeds = int(player.seeds)
        new_seeds = current_seeds + default_seed_amount
        player.set_seeds(new_seeds, user_id)
        #Refresh the user
        player = user.User(user_id)
        return_text=f"You've found: {str(nugget_amount)} nuggets! You now have: {str(current_nuggets)} nuggets! Oh, and take this seed I found as well. Might grow into something new!"

        return return_text
    else:
        return_text=f"You've found: {str(nugget_amount)} nuggets! You now have: {str(player.nuggets)} nuggets!"
        return return_text

    

def refresh_user_info(user_id, user_name):
  if database.check_if_data_exists(user_id, "users", "user_id") is False:
    user.User.create_new_user(user_id, user_name)