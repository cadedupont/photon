# Author: Thomas J. Buser
# Date Created: 15 September 2023
# Purpose: Module to handle game state including who hit who and what bases have been scored.

from typing import Dict

user = {
    "team" : "red",
    "user_id" : 0,
    "username" : "some_name",
    "points" : 0,
    "scored_base" : "red or green"
}

class GameState:
    #                         Dict[str, Dict[equipment_id, tuple(user_id, username)]]
    def __init__(self, users: Dict[str, Dict[int, tuple[int, str]]]) -> None:
        self.users = users
        self.red_team_score: int = 0
        self.green_team_score: int = 0
        self.red_base_score_valid: bool = True
        self.green_base_score_valid: bool = True
        self.red_base_scored: bool = False
        self.green_base_scored: bool = False

    def player_hit(self, equipment_hit_code: int, equipment_shooter_code: int):
        pass

    def red_base_hit(self, equipment_shooter_code: int):
        if self.red_base_hit_valid:
            self.red_base_hit = True
            # TODO: Attribute points to player and team
            self.red_base_hit_valid = False
        else:
            pass

    def green_base_hit(self, equipment_shooter_code: int):
        if self.green_base_hit_valid:
            self.green_base_hit = True
            # TODO: Attribute points to player and team
            self.green_base_hit_valid = False
        else:
            pass