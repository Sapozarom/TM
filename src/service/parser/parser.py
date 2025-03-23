import sys
from typing import TYPE_CHECKING
from datetime import datetime

# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine

from src.model.game import Game

# if TYPE_CHECKING:
from src.model.player import Player


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
                    self.get_block_type()
                    block_active = False
                    self.block = []

                self.analyze_line(line)
            else:
                if block_active:
                    self.block.append(line)

            if self.line_number == 300:
                # print(self.game.number_of_players)
                print(self.game.print_game_setup())

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

    # ANALYZE CURRENT BLOCK SECTION
    def get_block_type(self):
        if len(self.block) > 0:

            block_type: str = self.block[0]

            if not block_type.find("Created new Game") == -1:
                self.block_create_game()

            # print(block_type)
        pass

    def block_create_game(self):
        print("New Game Created:")

        for record in self.block:
            find_value = record.find(": ")
            new_value = record[find_value + 2:-1]
            if not record.find("GameID:") == -1:
                self.game.game_id = str(new_value)
            elif not record.find("GameSeed:") == -1:
                self.game.game_seed = str(new_value)
            elif not record.find("IsCustom:") == -1:
                new_value = self.get_bool(new_value)
                print(f"IsCustom: {new_value}")
                self.game.is_custom = bool(new_value)
            elif not record.find("IsOnline:") == -1:
                self.game.is_online = bool(new_value)
            elif not record.find("IsDraft:") == -1:
                self.game.is_draft = bool(new_value)
            elif not record.find("IsRanked:") == -1:
                self.game.is_ranked = bool(new_value)
            elif not record.find("Variant:") == -1:
                self.game.variant = str(new_value)
            elif not record.find("Prelude Phase:") == -1:
                self.game.prelude_phase = bool(new_value)
            elif not record.find("TR63:") == -1:
                self.game.tr_63 = bool(new_value)
            elif not record.find("BoardType:") == -1:
                self.game.board_type = str(new_value)
            elif not record.find("Beginner Corp:") == -1:
                self.game.beginner_corp = bool(new_value)
            elif not record.find("Extension Cards:") == -1:
                # list check
                new_list = self.get_list_split_by_coma(new_value)
                self.game.extension_cards = new_list
            elif not record.find("Extension Corp:") == -1:
                # list check
                new_list = self.get_list_split_by_coma(new_value)
                self.game.extension_corps = new_list
            elif not record.find("Corp Separate Draw:") == -1:
                self.game.corp_separate_draw = bool(new_value)
            elif not record.find("GenerationLevel:") == -1:
                self.game.generation_level = int(new_value)
            elif not record.find("TemperatureLevel:") == -1:
                self.game.temperature_level = int(new_value)
            elif not record.find("OxygenLevel:") == -1:
                self.game.oxygen_level = int(new_value)
            elif not record.find("OceanLevel:") == -1:
                self.game.ocean_level = int(new_value)
            elif not record.find("VenusScale:") == -1:
                self.game.venus_scale = int(new_value)
            elif not record.find("Player ") == -1 and record.find(":") == -1:
                player_number = int(record[-3:-1])
                self.game.current_player_number = int(player_number)
                print(f"Current: {self.game.current_player}")
            elif not (record.find("Name:") == -1):
                if self.game.has_current_player:
                    self.game.current_player.name = str(new_value)
            elif not (record.find("AILevel:") == -1):
                if self.game.has_current_player:
                    self.game.current_player.ai_level = str(new_value)
            elif not (record.find("IsMe:") == -1):
                if self.game.has_current_player:
                    self.game.current_player.ai_level = str(new_value)
            elif not record.find("Is player replaced by AI:") == -1:
                self.game.is_player_replaced_by_aI = bool(new_value)
            elif not record.find("Is player order shuffled:") == -1:
                self.game.is_player_order_shuffled = bool(new_value)

    def get_bool(self, value: str):
        bool_value = False

        if value.find("True"):
            bool_value = True
        return bool_value

    def get_list_split_by_coma(self, value: str):
        new_list: list = []

        if value.find(","):
            # get_values = record[find_value]
            new_list = value.split(",")
        else:
            new_list.append(None)

        return new_list
