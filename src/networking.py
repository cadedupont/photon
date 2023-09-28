# Author: Thomas J. Buser
# Date Created: 30 August 2023
# Purpose: Module to handle UDP networking for the Photon laser tag system communication between the control console and the packs.

import socket
import threading

# CONSTANTS
START_GAME_CODE: int = 202
END_GAME_CODE: int = 221
RED_BASE_SCORED_CODE: int = 66
GREEN_BASE_SCORED_CODE: int = 148
BUFFER_SIZE: int = 1024

class Networking:
    def __init__(self) -> None:
        self.address: str = "127.0.0.1"
        self.transmit_port: int = 7500
        self.recieve_port: int = 7501
        self.transmit_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.transmit_socket.bind((self.address, self.transmit_port))
        self.recieve_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recieve_socket.bind((self.address, self.recieve_port))

    def transmit_start_game_code(self) -> None:
        pass

    def transmit_end_game_code(self) -> None:
        pass

    def transmit_player_hit(self, player_code: int) -> None:
        pass

    def red_base_scored(self) -> None:
        pass

    def green_base_scored(self) -> None:
        pass

    def player_hit(self) -> None:
        pass

    def run(self) -> None:
        while True:
            raw_message, return_address = self.recieve_socket.recvfrom(BUFFER_SIZE)
            print("Message: " + raw_message.decode())
            print("Return Address: " + str(return_address))
            self.recieve_socket.sendto(str.encode("Thanks and welcome."), return_address)


if __name__ == "__main__":
    network_mod: Networking = Networking()
    network_mod.run()
    


# Notes:
# Socket 7500 to broadcast, 7501 to recieve
# Transmit formats: single int (who was hit), int 202 (start game), int 221 (game over)
# Recieve formats: int:int (who hit who), int 66 (red base scored), int 148 (green base scored)
# Max 15 players per team, 30 in total.