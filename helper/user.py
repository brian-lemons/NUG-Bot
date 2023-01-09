from helper import database

class User:
    def __init__(self, user_id=None) -> None:

        def get_user_info(info_to_retrieve: str):
            user_info = database.get_data_by_id(user_id, info_to_retrieve, "users", "user_id")
            return user_info

        #user_id, default_nuggets, user_name, default_seeds, default_trees, default_plots, default_plot_price

        #Basic Info
        self.id = user_id
        self.nuggets = get_user_info("nuggets")
        self.user_name = get_user_info("user_name")
        self.seeds = get_user_info("seeds")
        self.trees = get_user_info("trees")
        self.plots = get_user_info("plots")
        self.plot_price = get_user_info("plot_price")

    #Setters
    def set_nuggets(self, value, user_id):
        sql = "UPDATE users SET nuggets=? WHERE user_id=?"
        data_tuple = (value, user_id)
        database.custom_excute(sql, data_tuple)

    def set_plot_amount(self, value, user_id):
        sql = "UPDATE users SET plots=? WHERE user_id=?"
        data_tuple = (value, user_id)
        database.custom_excute(sql, data_tuple)

    def set_plot_price(self, user_id):

        #Calculate the cost of the next plot
        m = 500
        b = 100
        if self.plots == 0:
            cost = 500
        else:
            cost = m * self.plots + b

        sql = "UPDATE users SET plot_price=? WHERE user_id=?"
        data_tuple = (cost, user_id)
        database.custom_excute(sql, data_tuple)

    def set_seeds(self, value, user_id):
        sql = "UPDATE users SET seeds=? WHERE user_id=?"
        data_tuple = (value, user_id)
        database.custom_excute(sql, data_tuple)

    def set_tree_amount(self, value, user_id):
        sql = "UPDATE users SET trees=? WHERE user_id=?"
        data_tuple = (value, user_id)
        database.custom_excute(sql, data_tuple)

    def create_new_user(user_id, user_name):
        default_nuggets = 0
        default_seeds = 0
        default_trees = 0
        default_plots = 0
        default_plot_price = 500

        user_info = (user_id, default_nuggets, user_name, default_seeds, default_trees, default_plots, default_plot_price)

        database.add_to_database(user_id, "user_id", user_info, "users")