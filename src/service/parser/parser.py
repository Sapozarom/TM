import sys
# from typing import TYPE_CHECKING
from datetime import datetime

# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine

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
    event_log_file_path: str
    # current active game object to which the data is colected
    game: Game

    block = []

    def read_lines(self):
        file = open("logs/Player_basic.log", "r")

        block_active = False

        for line in file:

            # analyze lines with timestamp as main commands
            if line.startswith("[") and line[1].isdigit() and line.endswith(": \n"):

                # start block
                block_active = True
                self.block.append(line)
            elif line.startswith("[") and line[1].isdigit():

                # block finalization
                if block_active:
                    # print(self.block)
                    self.analyze_block()
                    block_active = False
                    self.block = []

                self.analyze_line(line)
            else:
                if block_active:
                    self.block.append(line)

            if self.line_number == 300:
                # print(self.game.number_of_players)
                print(self.game.players[0])
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
            event_log = "New Game Created"
            self.create_event_record(timestamp, event_log, "w")

            # print line parts
            self.print_line_parts(event_time, type_value,
                                  operation_value, event)
        # initialyze players
        elif operation_value == "[GameData]" and not event.find("TM_PlayerBoardData for player") == -1:

            if event[-2].isnumeric():
                player_number = int(event[-2])
                self.game.add_player(player_number)

                event_log = f"Player {player_number} created"
            else:
                event_log = f"Something went wrong while creating player in line |{self.line_number}"

            self.create_event_record(timestamp, event_log)

        # update terraforming rating
        elif operation_value == "[TM_PlayerBoardData]" and not event.find("Set terraforming rating") == -1:

            if self.game.phase == "GAME_INITIALIZATION" and self.game.current_player_number < self.game.number_of_players:
                self.game.current_player_number += 1

                # find old value
                at_spot = event.find(" at")
                with_spot = event.find("with")
                old_tr_value = int(event[at_spot+3: with_spot])

                # find new value
                value_spot = event.find("value")
                new_value = int(event[value_spot+5:])

                self.game.current_player.terraforming_rating = new_value

                event_log = f"Player {self.game.current_player_number} terraforming rating was set to {new_value}"
                self.create_event_record(timestamp, event_log)

        # update basic resource production
        elif (operation_value == "[PlayerResources]" and
              (not event.find("Set MegaCredit production from") == -1
               or not event.find("Set Steel production from") == -1
               or not event.find("Set Titanium production from") == -1
               or not event.find("Set Plant production from") == -1
               or not event.find("Set Energy production from") == -1
               or not event.find("Set Heat production from") == -1)):

            production_word_spot = event.find("production")
            resource = event[5:production_word_spot - 1]
            from_word_spot = event.find("from")
            to_word_spot = event.find(" to ")
            old_production_value = int(event[from_word_spot+5:to_word_spot])
            new_production_value = int(event[to_word_spot+3:])

            match resource:
                case "MegaCredit":
                    self.game.current_player.mega_credit_prod = new_production_value
                case "Steel":
                    self.game.current_player.steel_prod = new_production_value
                case "Titanium":
                    self.game.current_player.titaniu_prod = new_production_value
                case "Plant":
                    self.game.current_player.plant_prod = new_production_value
                case "Energy":
                    self.game.current_player.energy_prod = new_production_value
                case "Heat":
                    self.game.current_player.heat_prod = new_production_value

            event_log = f"Player {self.game.current_player_number} {resource} production set to {new_production_value}"
            self.create_event_record(timestamp, event_log)

        elif (operation_value == "[PlayerResources]" and
              (not event.find("Set MegaCredit quantity from") == -1
               or not event.find("Set Steel quantity from") == -1
               or not event.find("Set Titanium quantity from") == -1
               or not event.find("Set Plant quantity from") == -1
               or not event.find("Set Energy quantity from") == -1
               or not event.find("Set Heat quantity from") == -1)):

            quantity_word_spot = event.find("quantity")
            resource = event[5:quantity_word_spot - 1]
            from_word_spot = event.find("from")
            to_word_spot = event.find(" to ")
            old_quantity_value = int(event[from_word_spot+5:to_word_spot])
            new_quantity_value = int(event[to_word_spot+3:])

            match resource:
                case "MegaCredit":
                    self.game.current_player.mega_credit = new_quantity_value
                case "Steel":
                    self.game.current_player.steel = new_quantity_value
                case "Titanium":
                    self.game.current_player.titanium = new_quantity_value
                case "Plant":
                    self.game.current_player.plant = new_quantity_value
                case "Energy":
                    self.game.current_player.energy = new_quantity_value
                case "Heat":
                    self.game.current_player.heat = new_quantity_value

            event_log = f"Player {self.game.current_player_number} {resource} quantity set to {new_quantity_value}"
            self.create_event_record(timestamp, event_log)

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

    # update event log
    def create_event_record(self, timestamp, message, mode="a"):
        f = open(f"{self.event_log_file_path}", mode)
        f.write(f"{timestamp} | {message}\n")
        f.close()

    def analyze_block(self):
        if len(self.block) > 0:

            block_type = self.block[0]
            print(block_type)
            # print(block_type)
        pass
