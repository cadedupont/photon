# Author: Thomas J. Buser
# Date Created: 30 August 2023
# Purpose: Module to handle UDP networking for the Photon laser tag system communication between the control console and the packs.

import socket
import time

from game_logic import GameState

# CONSTANTS
START_GAME_CODE: int = 202
END_GAME_CODE: int = 221
RED_BASE_SCORED_CODE: int = 53
GREEN_BASE_SCORED_CODE: int = 43
BUFFER_SIZE: int = 1024
GAME_TIME_SECONDS: int = 360 # Seconds
BROADCAST_ADDRESS: str = "255.255.255.255"
RECIEVE_ALL_ADDRESS: str = "127.0.0.1"
TRANSMIT_PORT: int = 7501
RECIEVE_PORT: int = 7500

class Networking:
    def __init__(self) -> None:
        # Using python BSD socket interface
        self.transmit_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recieve_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recieve_socket.bind((RECIEVE_ALL_ADDRESS, RECIEVE_PORT))

    def transmit_equipment_code(self, equipment_code: str) -> None:
        # This is using the python BSD interface. The 1 enables broadcast at the syscall level and privledged process.
        self.transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.transmit_socket.sendto(str.encode(str(equipment_code)), (BROADCAST_ADDRESS, TRANSMIT_PORT))
    
    def transmit_start_game_code(self) -> None:
        # TODO : Eventually add error checking
        self.transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.transmit_socket.sendto(str.encode(str(START_GAME_CODE)), (BROADCAST_ADDRESS, TRANSMIT_PORT))

    def transmit_end_game_code(self) -> None:
        # TODO : Eventually add error checking
        self.transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.transmit_socket.sendto(str.encode(str(END_GAME_CODE)), (BROADCAST_ADDRESS, TRANSMIT_PORT))

    def transmit_player_hit(self, player_code: int) -> None:
        self.transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.transmit_socket.sendto(str.encode(str(player_code)), (BROADCAST_ADDRESS, TRANSMIT_PORT))

    def run_game(self, current_game_state: GameState, game_time: int) -> None:
        start_time: int = int(time.time())
        # Game time needs to be in seconds
        while int(time.time()) < (start_time + game_time):
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
           

if __name__ == "__main__":
    network_mod: Networking = Networking()
    game: GameState = GameState()
    network_mod.transmit_start_game_code() # test start game method
    network_mod.run_game(game)
    network_mod.transmit_end_game_code() # test end game method
    

# TODO: Check whether the equipment ID's are actually being transmitted correctly when they are input by the UI.

# Notes:
# Socket 7500 to broadcast, 7501 to recieve
# Transmit formats: single int (who was hit), int 202 (start game), int 221 (game over)
# Recieve formats: int:int (who hit who), int 53 (red base scored), int 43 (green base scored)
# Recieving (equipment id of player transmitting:equipment id of player hit)
# Max 15 players per team, 30 in total.