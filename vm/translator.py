from commands_codes import commands_codes


class Translator:
    byte_size = 4
    stack_size = 32

    def __init__(self, assembler_path, byte_path):
        assembler_file = open(assembler_path, 'r')
        self.assembler_code = assembler_file.readlines()
        assembler_file.close()
        self.byte_path = byte_path
        self.variables_addresses = {}
        self.byte_line_index = 0
        self.labels_addresses = {}
        self.labels_transitions = []

    def write_byte_line(self, file, byte_code):
        for byte in byte_code:
            file.write(hex(byte).ljust(5))
        file.write('\n')

    def process_labels(self):
        for transition in self.labels_transitions:
            label_address = self.labels_addresses.get(transition[0])
            if label_address:
                self.byte_lines[transition[1]][transition[2]] = label_address * self.byte_size
            else:
                print "ERROR! Unknown token: " + transition[0]
                exit(-1)

    def translate_variable(self, assembler_line):
        tokens = assembler_line.split(' ')
        variable_address = int(tokens[0][1:-1])
        variable_name = tokens[2]
        variable_value = int(tokens[4])
        self.variables_addresses[variable_name] = variable_address
        return [0, 0, 0, variable_value]

    def translate_command(self, assembler_line):
        tokens = assembler_line.strip().split(' ')
        byte_code = [0, 0, 0, 0]
        command_code = commands_codes.get(tokens[0])
        if command_code is None:
            print "ERROR! No such command: ", tokens[0]
            exit(-1)
        byte_code[0] = command_code
        if tokens[0] == 'LAB':
            label_name = tokens[1]
            self.labels_addresses[label_name] = self.byte_line_index
            return byte_code
        for i in range(1, len(tokens)):
            token_address = self.variables_addresses.get(tokens[i])
            if token_address is not None:
                byte_code[i] = token_address
            else:
                if tokens[i].isdigit():
                    byte_code[i] = int(tokens[i])
                else:
                    self.labels_transitions += [(tokens[i], self.byte_line_index, i)]
        return byte_code

    def translate(self):
        byte_file = open(self.byte_path, 'w+')
        self.byte_lines = []
        for assembler_line in self.assembler_code:
            if assembler_line == '\n':
                continue
            elif assembler_line.find(':') > 0:
                byte_code = self.translate_variable(assembler_line)
            else:
                byte_code = self.translate_command(assembler_line)
            self.byte_lines += [byte_code]
            self.byte_line_index += 1
        for i in range(self.stack_size):
            empty_space = [0, 0, 0, 0]
            self.byte_lines += [empty_space]
        self.process_labels()
        for byte_line in self.byte_lines:
            self.write_byte_line(byte_file, byte_line)
        byte_file.close()

if __name__ == '__main__':
    translator = Translator('fib.txt', 'bytecode_fib.txt')
    translator.translate()

