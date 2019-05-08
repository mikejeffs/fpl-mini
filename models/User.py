class User: # Should be User really, player implies Mo Salah.
    def __init__(self, id, team_name, user_name, game_weeks):
        self.id = id
        self.team_name = team_name
        self.user_name = user_name
        self.game_weeks = game_weeks

    def set_game_weeks(self, game_weeks):
        self.game_weeks = game_weeks

    def get_game_weeks(self):
        return self.game_weeks