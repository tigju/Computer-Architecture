"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 255
        self.reg = [0] * 8
        # self.reg[7] = 0xF4
        self.pc = 0


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, address):
        """ read from ram by specified address and returns stored value"""
        return self.ram[address]

    def ram_write(self, value, address):
        """ writes the value to a address specified into ram"""
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

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

            elif instruction == PRN:
                register_to_print = self.ram_read(self.pc+1)
                print(self.reg[register_to_print])
                self.pc += 2

            elif instruction == HLT:
                running = False
                self.pc += 1
                exit()
                
            else:
                print("Unknown opcode!")

