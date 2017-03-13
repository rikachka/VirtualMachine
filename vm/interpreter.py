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
        byte_code_line = var_address // self.byte_size
        var_byte_line = self.byte_code[byte_code_line]
        if var_byte_line[1] == 0:
            variable_int = var_byte_line[3]
            return variable_int
        if var_byte_line[1] == 1:
            variable_str = ''
            while chr(var_byte_line[3]) != '\0':
                variable_str += chr(var_byte_line[3])
                byte_code_line += 1
                var_byte_line = self.byte_code[byte_code_line]
            return variable_str
        else:
            print("ERROR! Unknown type of the variable")


    def set_value(self, var_address, value):
        byte_code_line = var_address // self.byte_size
        self.byte_code[byte_code_line][3] = value

    def goto(self, label):
        self.line_index = label // self.byte_size

    def VAR(self, args):
        pass

    def INP(self, args):
        input_var = args[0]
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

    def E0(self, args):
        compared_var = args[0]
        label_name = args[1]
        if self.get_value(compared_var) == 0:
            self.goto(label_name)

    def LAB(self, args):
        pass

    def STOP(self, args):
        return True

    def interprete(self):
        commands_names = {elem[1]: elem[0] for elem in commands_codes.items()}
        while True:
            byte_line = self.byte_code[self.line_index]
            command_name = commands_names.get(byte_line[0])
            if command_name is None:
                print "ERROR! Unknown command"
                exit(-1)
            is_program_end = getattr(self, command_name)(byte_line[1:])
            if is_program_end:
                break
            self.line_index += 1

if __name__ == '__main__':
    translator = Interpreter('bytecode_fib2.txt')
    translator.interprete()