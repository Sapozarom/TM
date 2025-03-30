import sys
from typing import TYPE_CHECKING
from datetime import datetime
from src.lib.updateDbTables.updateDbTables import UpdateDbTables
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine

from src.model.game import Game

# if TYPE_CHECKING:
from src.model.player import Player


class Parser():

    file = open("logs/Player.log", "r")
    dbUpdater = UpdateDbTables()

    line_number = 0
    block_active = False
    game_in_progress = False

    finish_line = 400

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
            self.line_number += 1

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

            if self.line_number == self.finish_line:
                # print(self.game.number_of_players)
                # print(self.game.print_game_setup())
                # print(self.game.current_player.action_bank)

                # self.dbUpdater.create_new_game(self.game)

                print(f"finished on line {self.line_number}")
                break

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
                event_log = f"Current Player changed to {self.game.current_player_number}"
                self.create_event_record(timestamp, event_log)

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

            # find resource and value in text
            production_word_spot = event.find("production")
            resource = event[5:production_word_spot - 1]
            from_word_spot = event.find("from")
            to_word_spot = event.find(" to ")
            old_production_value = int(event[from_word_spot+5:to_word_spot])
            new_production_value = int(event[to_word_spot+3:])

            # update values
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

            # event log
            event_log = f"Player {self.game.current_player_number} {resource} production set to {new_production_value}"
            self.create_event_record(timestamp, event_log)

        # update basic resources quantity
        elif (operation_value == "[PlayerResources]" and
              (not event.find("Set MegaCredit quantity from") == -1
               or not event.find("Set Steel quantity from") == -1
               or not event.find("Set Titanium quantity from") == -1
               or not event.find("Set Plant quantity from") == -1
               or not event.find("Set Energy quantity from") == -1
               or not event.find("Set Heat quantity from") == -1)):

            # find resource and quantity in text
            quantity_word_spot = event.find("quantity")
            resource = event[5:quantity_word_spot - 1]
            from_word_spot = event.find("from")
            to_word_spot = event.find(" to ")
            old_quantity_value = int(event[from_word_spot+5:to_word_spot])
            new_quantity_value = int(event[to_word_spot+3:])

            # update quantity
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

            # event log
            event_log = f"Player {self.game.current_player_number} {resource} quantity set to {new_quantity_value}"
            self.create_event_record(timestamp, event_log)

        # adding action to action bank
        elif (operation_value == "[PlayerActionBank]" and not event.find("Adding action") == -1):
            # find action number
            open_bracket_pos = event.find("(")
            close_bracket_pos = event.find(")")
            action_number = int(event[open_bracket_pos + 1: close_bracket_pos])

            to_player_word_pos = event.find("to player")
            bank_word_pos = event.find("bank")
            player_number = int(event[to_player_word_pos + 9: bank_word_pos])

            action_name = event[close_bracket_pos + 2: to_player_word_pos - 1]

            # print(action_name)

            player_object = self.game.get_player_by_number(player_number)
            player_object.action_bank[action_number] = action_name

        # change game phase to PlayerSetup
        elif (operation_value == "[State machine]" and not event.find("GameSM enters PlayerSetup") == -1):
            # SAVE GAME STATE
            self.game.phase = "PLAYER_STEUP"
            self.game.current_player_number = 0


# asdasd
# asdasd
# asdasd

    # create proper timestamp from log string
    # example: [2025-02-22T15:36:33.9801591Z]


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
            timestamp_brackets = self.block[0].find("]") + 1
            event_time = self.block[0][0:timestamp_brackets]
            timestamp = self.get_timestamp_from_event_time(event_time)

            if not block_type.find("Created new Game") == -1:
                self.block_create_game(timestamp)

    def block_create_game(self, timestamp):
        print("New Game Created:")

        for record in self.block:
            # find value in text
            find_value = record.find(": ")
            new_value = record[find_value + 2:-1]
            parameter = record[:find_value]

            # change current player
            if not record.find("Player ") == -1 and record.find(":") == -1:
                player_number = int(record[-3:-1])
                self.game.current_player_number = int(player_number)

                # event log record
                event_log = f"Current Player changed to {player_number}"
                self.create_event_record(timestamp, event_log)

            # default values
            event_log = None
            player_param = False
            param = None

            # switch through diferent parameters
            match parameter:
                case "GameID":
                    self.game.game_id = str(new_value)
                    param = "GameID"
                case "GameSeed":
                    self.game.game_seed = str(new_value)
                    param = "GameSeed"
                case "IsCustom":
                    param = "IsCustom"
                    self.game.is_custom = self.get_bool_from_string(new_value)
                case "IsOnline":
                    param = "IsOnline"
                    self.game.is_online = self.get_bool_from_string(new_value)
                case "IsDraft":
                    param = "IsDraft"
                    self.game.is_draft = self.get_bool_from_string(new_value)
                case "IsRanked":
                    param = "IsRanked"
                    self.game.is_ranked = self.get_bool_from_string(new_value)
                case "Variant":
                    param = "Variant"
                    self.game.variant = str(new_value)
                case "Prelude Phase":
                    param = "Prelude Phase"
                    self.game.prelude_phase = self.get_bool_from_string(
                        new_value)
                case "TR63":
                    param = "TR63"
                    self.game.tr_63 = self.get_bool_from_string(new_value)
                case "BoardType":
                    param = "BoardType"
                    self.game.board_type = str(new_value)
                case "Beginner Corp":
                    param = "Beginner Corp"
                    self.game.beginner_corp = self.get_bool_from_string(
                        new_value)
                case "Extension Cards":
                    param = "Extension Cards"
                    new_list = self.get_list_split_by_coma(new_value)
                    self.game.extension_cards = new_list
                case "Extension Corp":
                    param = "Extension Corp"
                    new_list = self.get_list_split_by_coma(new_value)
                    self.game.extension_corps = new_list
                case "Corp Separate Draw":
                    param = "Corp Separate Draw"
                    self.game.corp_separate_draw = self.get_bool_from_string(
                        new_value)
                case "GenerationLevel":
                    param = "GenerationLevel"
                    self.game.generation_level = int(new_value)
                case "TemperatureLevel":
                    param = "TemperatureLevel"
                    self.game.temperature_level = int(new_value)
                case "OxygenLevel":
                    param = "OxygenLevel"
                    self.game.oxygen_level = int(new_value)
                case "OceanLevel":
                    param = "OceanLevel"
                    self.game.ocean_level = int(new_value)
                case "VenusScale":
                    param = "VenusScale"
                    self.game.venus_scale = int(new_value)
                case "Name":
                    param = "Name"
                    player_param = True
                    if self.game.has_current_player:
                        self.game.current_player.name = str(new_value)
                case "AILevel":
                    param = "AILevel"
                    player_param = True
                    if self.game.has_current_player:
                        self.game.current_player.ai_level = str(new_value)
                case "IsMe":
                    param = "IsMe"
                    player_param = True
                    if self.game.has_current_player:
                        self.game.current_player.ai_level = str(new_value)
                case "Is player replaced by AI":
                    param = "Is player replaced by AI"
                    self.game.is_player_replaced_by_aI = self.get_bool_from_string(
                        new_value)
                case "Is player order shuffled":
                    param = "Is player order shuffled"
                    self.game.is_player_order_shuffled = self.get_bool_from_string(
                        new_value)

            # create event log message
            if player_param:
                event_log = f"Player {self.game.current_player_number} parameter change {param} = {new_value}"
            elif not param is None:
                event_log = f"Game parameter change  {param} = {new_value}"

            if not event_log == None:
                self.create_event_record(timestamp, event_log)

    def get_list_split_by_coma(self, value: str):
        new_list: list = []

        if value.find(","):
            # get_values = record[find_value]
            new_list = value.split(",")
        else:
            new_list.append(None)

        return new_list

    def get_bool_from_string(self, string: str):
        bool_value = False

        if not string.find("True") == -1:
            bool_value = True

        return bool_value
