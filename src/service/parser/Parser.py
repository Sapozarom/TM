import sys
from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from src.model.game import Game

# if TYPE_CHECKING:
#     from src.model.Player import Player


class Parser():

    file = open("logs/Player.log", "r")

    line_number = 1
    block_active = False
    game_in_progress = False

    # engine = create_engine("sqlite:///tmdb.db", echo=True)
    # session = Session(engine)

    # path to event log
    event_files_location = "eventLog/"
    event_log_file_path = ""

    # current active game object to which the data is colected
    game: Game

    block = []

    def read_lines(self):
        file = open("logs/Player.log", "r")

        block_active = False
        block = []
        for line in file:

            # analyze lines with timestamp as main commands
            if line.startswith("[") and line[1].isdigit() and line.endswith(": \n"):

                # start block
                block_active = True
                block.append(line)
            elif line.startswith("[") and line[1].isdigit():

                # stop block
                if block_active:
                    # print(block)
                    block_active = False
                    block = []

                self.analyze_line(line)
            else:
                if block_active:
                    block.append(line)

            if self.line_number == 300:
                # print(self.game.number_of_players)
                print(f"finished on line {self.line_number}")
                break

            self.line_number += 1

        # Close the file
        file.close()

    def analyze_line(self, line: str):

        # split line into meaningful pieces
        timestamp_brackets = line.find("]") + 1
        event_time = line[0:timestamp_brackets]

        type_bracket = line[timestamp_brackets:].find("]") + 1

        type_value = line[timestamp_brackets: timestamp_brackets +
                          type_bracket]

        operation_bracket = line[timestamp_brackets +
                                 type_bracket:].find("]") + 1

        operation_value = line[timestamp_brackets +
                               type_bracket: timestamp_brackets + type_bracket + operation_bracket]

        event = line[timestamp_brackets +
                     type_bracket + operation_bracket:]

        timestamp = self.get_timestamp_from_event_time(event_time)

        # start new game and create eventLog file
        if operation_value == "[Game Initialization]" and not event.find("Creating new Game") == -1 and not self.game_in_progress:

            self.game_in_progress = True

            # get timestamp

            # create new game object
            new_game = Game()
            new_game.phase = "GAME_INITIALIZATION"
            new_game.start = timestamp
            self.game = new_game

            # create event log path
            event_log_file_name = f"{timestamp}_game_event_log.txt"

            self.set_event_log_file_path(event_log_file_name)

            # event record
            message = "New Game Created"
            self.create_event_record(timestamp, message, "w")

            # print line parts
            self.print_line_parts(event_time, type_value,
                                  operation_value, event)
        # initialyze players
        elif operation_value == "[GameData]" and not event.find("TM_PlayerBoardData for player") == -1:

            # event record
            if event[-2].isnumeric():
                player_number = int(event[-2])
                self.game.add_player(player_number)
                message = f"Player {player_number} created"
            else:
                message = f"Something went wrong while creating player in line |{self.line_number}"

            self.create_event_record(timestamp, message)

    def get_timestamp_from_event_time(self, event_time):
        date = event_time[1:11]
        time = event_time[12:20]
        start_time = datetime.strptime(
            f"{date} {time}", "%Y-%m-%d %H:%M:%S")

        return int(datetime.timestamp(start_time))

    def print_line_parts(self, event_time, type_value, operation_value, event):
        print(f"Line: {self.line_number}")
        print(f"Timestamp: {event_time}")
        print(f"Type: {type_value}")
        print(f"Operation: {operation_value}")
        print(f"Event: {event}")

    def set_event_log_file_path(self, file_name):
        self.event_log_file_path = f"{self.event_files_location}{file_name}"

    def create_event_record(self, timestamp, message, mode="a"):
        f = open(f"{self.event_log_file_path}", mode)
        f.write(f"{timestamp} | {message}\n")
        f.close()
