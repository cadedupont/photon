# Author: Thomas J. Buser
# Date Created: 30 August 2023
# Purpose: Module to handle UDP networking for the Photon laser tag system communication between the control console and the packs.

import socket
import time
from typing import Dict, List
from user import User

from game_logic import GameState

# CONSTANTS
START_GAME_CODE: int = 202
END_GAME_CODE: int = 221
RED_BASE_SCORED_CODE: int = 53
GREEN_BASE_SCORED_CODE: int = 43
BUFFER_SIZE: int = 1024
GAME_TIME_SECONDS: int = 360 # Seconds
BROADCAST_ADDRESS: str = "127.0.0.1"
RECIEVE_ALL_ADDRESS: str = "0.0.0.0"
TRANSMIT_PORT: int = 7501
RECIEVE_PORT: int = 7500

class Networking:
    def __init__(self) -> None:
        pass
    
    def set_sockets(self) -> bool:
        # Using python BSD socket interface
        # Error Checking
        try:
            self.transmit_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.recieve_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.recieve_socket.bind((RECIEVE_ALL_ADDRESS, RECIEVE_PORT))
            return True
        except Exception as e:
            print(e)
            return False

    def close_sockets(self) -> bool:
        # Close transmit and receive sockets
        try:
            self.transmit_socket.close()
            self.recieve_socket.close()
            return True
        except Exception as e:
            print(e)
            return False

    def transmit_equipment_code(self, equipment_code: str) -> bool:
        # This is using the python BSD interface. The 1 enables broadcast at the syscall level and privledged process.
        # Error Checking for transmitting equipment code
        try:
            self.transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.transmit_socket.sendto(str.encode(str(equipment_code)), (BROADCAST_ADDRESS, TRANSMIT_PORT))
            return True
        except Exception as e:
            print(e)
            return False
    
    def transmit_start_game_code(self) -> bool:
        # Error Checking for transmitting start game code
        try:
            self.transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.transmit_socket.sendto(str.encode(str(START_GAME_CODE)), (BROADCAST_ADDRESS, TRANSMIT_PORT))
            return True
        except Exception as e:
            print(e)
            return False
            
    def transmit_end_game_code(self) -> bool:
        # Error Checking for transmitting end game code
        try:
            self.transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.transmit_socket.sendto(str.encode(str(END_GAME_CODE)), (BROADCAST_ADDRESS, TRANSMIT_PORT))
            return True
        except Exception as e:
            print(e)
            return False

    def transmit_player_hit(self, player_code: int) -> bool:
        # Error Checking for transmitting player hit code
        try:
            self.transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.transmit_socket.sendto(str.encode(str(player_code)), (BROADCAST_ADDRESS, TRANSMIT_PORT))
            return True
        except Exception as e:
            print(e)
            return False

    def run_game(self, current_game_state: GameState) -> None:
        start_time: int = int(time.time())
        # Game time needs to be in seconds
        while int(time.time()) < (start_time + GAME_TIME_SECONDS):
            raw_message, return_address = self.recieve_socket.recvfrom(BUFFER_SIZE)
            decoded_message: str = raw_message.decode("utf-8")
            message_components: [str] = decoded_message.split(":")
            # By the design spec the messages are never more than two small integers seperated by a colon
            left_code: int = int(message_components[0])
            right_code: int = int(message_components[1])
            if right_code == 53:
                current_game_state.red_base_hit(left_code)
            elif right_code == 43:
                current_game_state.green_base_hit(left_code)
            elif right_code != 53 and right_code != 43 and right_code <= 100:
                # 100 was the bound mentioned in class for a reasonable limit of equipment ids
                current_game_state.player_hit(left_code, right_code)
                # Broadcasting back out who was hit so their pack will deactivate for the set time interval
                self.transmit_player_hit(right_code)
                # TODO: Remove after debugging
                # print("Codes Recieved: Left Code is " + str(left_code) + " Right Code is " + str(right_code))
            else:
                print("Invalid codes: Left Code is " + str(left_code) + " Right Code is " + str(right_code))
        self.transmit_end_game_code()
        self.transmit_end_game_code()
        self.transmit_end_game_code()
           

if __name__ == "__main__":
    network_mod: Networking = Networking()
    users: Dict[str, List[User]] = {
        "green" : [],
        "red" : []
    }
    users["green"].append(User(1, 10, 10, "John Conner"))
    users["green"].append(User(2, 20, 20, "Sarah Conner"))
    users["red"].append(User(3, 30, 30, "James Conner"))
    users["red"].append(User(4, 40, 40, "Someone Conner"))
    game: GameState = GameState(users)
    network_mod.set_sockets()
    network_mod.transmit_start_game_code() # test start game method
    network_mod.run_game(game)
    network_mod.transmit_end_game_code() # test end game method
    network_mod.close_sockets()
    

# TODO: Check whether the equipment ID's are actually being transmitted correctly when they are input by the UI.

# Notes:
# Socket 7500 to broadcast, 7501 to recieve
# Transmit formats: single int (who was hit), int 202 (start game), int 221 (game over)
# Recieve formats: int:int (who hit who), int 53 (red base scored), int 43 (green base scored)
# Recieving (equipment id of player transmitting:equipment id of player hit)
# Max 15 players per team, 30 in total.