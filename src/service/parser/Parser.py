import sys


class Parser():

    file = open("logs/Player.log", "r")
    line_number = 1
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
                print(block)
                block_active = False
                block = []

            timestamp_brackets = line.find("]") + 1
            timestamp = line[0:timestamp_brackets]

            type_bracket = line[timestamp_brackets:].find("]") + 1

            type_value = line[timestamp_brackets: timestamp_brackets +
                              type_bracket]

            operation_bracket = line[timestamp_brackets +
                                     type_bracket:].find("]") + 1

            operation_value = line[timestamp_brackets +
                                   type_bracket: timestamp_brackets + type_bracket + operation_bracket]

            action = line[timestamp_brackets +
                          type_bracket + operation_bracket:]
            print(f"Line: {line_number}")
            print(f"Timestamp: {timestamp}")
            print(f"Type: {type_value}")
            print(f"Operation: {operation_value}")
            print(f"Action: {action}")

        else:
            if block_active:
                block.append(line)

        if line_number == 300:

            break

        line_number += 1
    # Close the file
    # print(block)
    file.close()

    def read_lines(self):
        file = open("logs/Player.log", "r")
        line_number = 1
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
                    print(block)
                    block_active = False
                    block = []

                self.analyze_line(line)
            else:
                if block_active:
                    block.append(line)

            if line_number == 300:

                break

            line_number += 1
        # Close the file
        # print(block)
        file.close()

    def analyze_line(self, line: str):

        timestamp_brackets = line.find("]") + 1
        timestamp = line[0:timestamp_brackets]

        type_bracket = line[timestamp_brackets:].find("]") + 1

        type_value = line[timestamp_brackets: timestamp_brackets +
                          type_bracket]

        operation_bracket = line[timestamp_brackets +
                                 type_bracket:].find("]") + 1

        operation_value = line[timestamp_brackets +
                               type_bracket: timestamp_brackets + type_bracket + operation_bracket]

        event = line[timestamp_brackets +
                     type_bracket + operation_bracket:]
        print(f"Line: {self.line_number}")
        print(f"Timestamp: {timestamp}")
        print(f"Type: {type_value}")
        print(f"Operation: {operation_value}")
        print(f"Event: {event}")
