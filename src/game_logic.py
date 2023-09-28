# Author: Thomas J. Buser
# Date Created: 15 September 2023
# Purpose: Module to handle game state including who hit who and what bases have been scored.

class Player:
    def __init__(self, input_id: int, input_equipment_id: int) -> None:
        self.id: int = input_id
        self.equipment_id: int = input_equipment_id
        self.score: int = 0

    def player_hit(self, hit_by: int) -> None:
        # TODO: Implement logic for if the player is hit
        pass

    def player_score_player(self, hit: int) -> None:
        # TODO: Implement logic for when the player hits another player
        pass

    def get_score(self) -> int:
        return self.score

class GameState:
    def __init__(self) -> None:
        self.players: list[Player] = []
        self.red_tower_scored: bool = False
        self.green_twoer_scored: bool = False

    def register_player(self, player_id: int, equipment_id: int) -> None:
        self.players.append(Player(player_id, equipment_id))