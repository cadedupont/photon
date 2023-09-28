import socket
import time

# CONSTANTS
START_GAME_CODE: int = 202
END_GAME_CODE: int = 221
RED_BASE_SCORED_CODE: int = 66
GREEN_BASE_SCORED_CODE: int = 148
BUFFER_SIZE: int = 1024
GAME_TIME_SECONDS: int = 3 # Seconds
BROADCAST_ADDRESS: str = "255.255.255.255"
TRANSMIT_PORT: int = 7501

def play_game() -> None:
    # Can check this periodically to see if the game should be over.
    start_time: time = time.time()
    print(time.time())
    time.sleep(GAME_TIME_SECONDS)
    print("Starting game now: " + str(start_time))

    transmit_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # recieve_socket: socket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)

    # Begin Game
    start_message: bytes = str.encode(str(START_GAME_CODE))
    transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    transmit_socket.sendto(start_message, (BROADCAST_ADDRESS, TRANSMIT_PORT))

    print("Starting game now: " + str(start_time))

play_game()