class User:
    equipment_id: int
    user_id: int
    username: str
    game_score: int
    has_hit_base: bool

    # Constructor, pass in equipment ID, user ID, and username from player entry GUI
    def __init__(self, equipment_id: int = -1, user_id: int = -1, username: str = "NO_USERNAME") -> None:
        self.equipment_id = equipment_id
        self.user_id = user_id
        self.username = username
        self.game_score = 0
        self.has_hit_base = False

    # String representation of User object
    def __str__(self) -> str:
        return f"Username: {self.username}\nEquipment ID: {self.equipment_id}\nUser ID: {self.user_id}\nGame Score: {self.game_score}\nHas Hit Base: {self.has_hit_base}\n\n"
    