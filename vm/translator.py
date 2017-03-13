from commands_codes import commands_codes


class Translator:
    byte_size = 4
    stack_size = 30

    def __init__(self, assembler_path, byte_path):
        assembler_file = open(assembler_path, 'r')
        self.assembler_code = assembler_file.readlines()
        assembler_file.close()
        self.byte_path = byte_path
        self.free_stack_address = 0
        self.variables_addresses = {}
        self.byte_line_index = 0
        self.initialized_addresses = {}
        self.initialized_mentions = []

    def write_byte_file(self):
        byte_file = open(self.byte_path, 'w+')
        for byte_line in self.byte_lines:
            for byte in byte_line:
                byte_file.write(hex(byte).ljust(6))
            byte_file.write('\n')
        byte_file.close()

    def process_mentioning(self):
        for mention in self.initialized_mentions:
            mentioned_address = self.initialized_addresses.get(mention[0])
            if mentioned_address:
                self.byte_lines[mention[1]][mention[2]] = mentioned_address * self.byte_size
            else:
                print "ERROR! Unknown token: " + mention[0]
                exit(-1)

    def translate_variable(self, tokens):
        variable_name = tokens[1]
        if tokens[2].startswith('\"') and tokens[2].endswith('\"'):
            byte_code = []
            variable_str = tokens[2][1:-1]
            for symbol in variable_str:
                byte_code += [[0, 1, 0, ord(symbol)]]
            byte_code += [[0, 1, 0, ord('\0')]]
            self.variables_addresses[variable_name] = self.free_stack_address
            self.free_stack_address += self.byte_size * len(byte_code)
            return byte_code
        else:
            variable_int = int(tokens[2])
            self.variables_addresses[variable_name] = self.free_stack_address
            self.free_stack_address += self.byte_size
            return [[0, 0, 0, variable_int]]

    def translate_initializations(self, tokens):
        initialized_name = tokens[1]
        self.initialized_addresses[initialized_name] = self.byte_line_index
        return [[0, 0, 0, 0]]

    def translate_command(self, tokens):
        byte_code_line = [0, 0, 0, 0]
        for i in range(1, len(tokens)):
            token_address = self.variables_addresses.get(tokens[i])
            if token_address is not None:
                byte_code_line[i] = token_address
            else:
                if tokens[i].isdigit():
                    byte_code_line[i] = int(tokens[i])
                else:
                    self.initialized_mentions += [(tokens[i], self.byte_line_index, i)]
        return [byte_code_line]

    def translate_line(self, assembler_line):
        tokens = assembler_line.strip().split(' ')
        command_code = commands_codes.get(tokens[0])
        if command_code is None:
            print "ERROR! No such command: ", tokens[0]
            exit(-1)
        if tokens[0] == 'LAB' or tokens[0] == 'FUN':
            byte_code = self.translate_initializations(tokens)
        elif tokens[0] == 'VAR':
            byte_code = self.translate_variable(tokens)
        else:
            byte_code = self.translate_command(tokens)
        for index in range(len(byte_code)):
            byte_code[index][0] = command_code
        return byte_code

    def translate(self):
        self.byte_lines = []
        for i in range(self.stack_size):
            empty_space = [0, 0, 0, 0]
            self.byte_lines += [empty_space]
            self.byte_line_index += 1
        self.free_stack_address = self.stack_size * self.byte_size
        for assembler_line in self.assembler_code:
            if assembler_line == '\n':
                continue
            byte_code = self.translate_line(assembler_line)
            self.byte_lines += byte_code
            self.byte_line_index += len(byte_code)
        # print self.initialized_addresses
        # print self.initialized_mentions
        self.process_mentioning()
        self.write_byte_file()

if __name__ == '__main__':
    translator = Translator('fib3.txt', 'bytecode_fib3.txt')
    translator.translate()

