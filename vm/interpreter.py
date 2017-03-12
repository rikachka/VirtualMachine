from commands_codes import commands_codes


class Interpreter:
    number_base = 16
    byte_size = 4

    def __init__(self, byte_path):
        self.byte_code = self.read_byte_file(byte_path)
        self.line_index = 0

    def read_byte_file(self, byte_path):
        byte_file = open(byte_path, 'r')
        byte_code = byte_file.readlines()
        byte_code = [[int(elem, self.number_base) for elem in line.strip().split(' ') if elem != ''] for line in byte_code]
        byte_file.close()
        return byte_code

    def get_value(self, var_address):
        return self.byte_code[var_address // self.byte_size][3]

    def set_value(self, var_address, value):
        self.byte_code[var_address // self.byte_size][3] = value

    def goto(self, label):
        self.line_index = label

    def INP(self, args):
        input_var = args[0]
        print "Input: ",
        self.set_value(input_var, int(input()))

    def OUT(self, args):
        output_var = args[0]
        print self.get_value(output_var)

    def MOV(self, args):
        to_var = args[0]
        from_var = args[1]
        self.set_value(to_var, self.get_value(from_var))

    def SUM(self, args):
        to_var = args[0]
        from_var = args[1]
        self.set_value(to_var, self.get_value(to_var) + self.get_value(from_var))

    def DIF(self, args):
        to_var = args[0]
        from_var = args[1]
        self.set_value(to_var, self.get_value(to_var) - self.get_value(from_var))

    def NE0(self, args):
        compared_var = args[0]
        label_name = args[1]
        if self.get_value(compared_var) != 0:
            self.goto(label_name)

    def LAB(self, args):
        pass

    def interprete(self):
        commands_names = {elem[1]: elem[0] for elem in commands_codes.items()}
        while True:
        # for byte_line in self.byte_code:
            byte_line = self.byte_code[self.line_index]
            if byte_line[0] == 0:
                continue
            command_name = commands_names.get(byte_line[0])
            if command_name is None:
                print "ERROR! Unknown command"
                exit(-1)
            is_program_end = getattr(self, command_name)(byte_line[1:])
            if is_program_end:
                break
            self.line_index += 1
        for byte_line in self.byte_code:
            print byte_line

if __name__ == '__main__':
    translator = Interpreter('bytecode_fib.txt')
    translator.interprete()