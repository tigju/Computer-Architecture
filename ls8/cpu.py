"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
ADD = 0b10100000
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 255
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0
        self.sp = 7


    def load(self, filename):
        """Load a program into memory."""
        address = 0
        if len(filename) > 1:
            try:
                with open(filename[1]) as my_file:
                    for line in my_file:
                        split_line = line.split('#')
                        
                        code_value = split_line[0].strip() ## removes white space and new line \n
                        # check that value before # is not empty
                        if code_value == "":
                            continue 
                        instruction = int(code_value, 2)
                        self.ram_write(address, instruction)
                        address += 1

            except FileNotFoundError:
                print(f'{filename[1]} file not found')
                sys.exit(2)
        else:
            print("File name as a second argument is missing. Ex.: python ls8.py filename")
            sys.exit(1)
        
        # space_for_stack = len(self.ram) - address
        # print(space_for_stack)

        # print(self.reg)

        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def ram_read(self, address):
        """ read from ram by specified address and returns stored value"""
        return self.ram[address]

    def ram_write(self, address, value):
        """ writes the value to a address specified into ram"""
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        
        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]

        #elif op == "SUB": etc
        else:
            raise Exception(f'Unsupported ALU operation {bin(op)}')

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            instruction = self.ram_read(self.pc)

            if instruction == LDI:
                reg_num = self.ram_read(self.pc+1)
                val = self.ram_read(self.pc+2)
                self.reg[reg_num] = val
                self.pc += 3

            elif instruction == MUL:
                reg_a = self.ram_read(self.pc+1)
                reg_b = self.ram_read(self.pc+2)
                self.alu(instruction, reg_a, reg_b)
                self.pc += 3

            elif instruction == PRN:
                register_to_print = self.ram_read(self.pc+1)
                print(self.reg[register_to_print])
                self.pc += 2

            elif instruction == PUSH:
                self.reg[self.sp] -= 1 # decrement stack pointer
                reg_index = self.ram[self.pc + 1] # get the register index from program (memory)
                # get the value from register index
                value_in_register = self.reg[reg_index]
                # add the value in stack at location self.reg[self.sp] decremented by 1
                self.ram[self.reg[self.sp]] = value_in_register
                self.pc += 2
                print(self.ram)

            elif instruction == POP:
                continue 
            
            elif instruction == HLT:
                running = False
                self.pc += 1
                exit()
                
            else:
                print("Unknown opcode!")
                sys.exit(1)

