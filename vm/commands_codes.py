commands_codes = {'VAR': 0x00,  # variable
                  'INP': 0x01,
                  'OUT': 0x02,
                  'MOV': 0x03,
                  'PUSH': 0x10,
                  'POP': 0x11,
                  'PAD': 0x12,  # push current address
                  'SUM': 0x20,  # sum
                  'DIF': 0x21,  # difference
                  'NE0': 0x30,  # not equal (if not equal, go by label)
                  'E0':  0x31,  # equal (if equal, go by label)
                  'LAB': 0x40,  # label
                  'STOP': 0x41, # exit
                  'FUN': 0x51,  # function
                  'RET': 0x52,  # function return
                  'CALL': 0x53, # call function
                  }