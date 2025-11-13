import random

class CPU:
    def __init__(self):
        self.registers = [0] * 16
        self.program_counter = 0x200
        self.index_register = 0
        self.stack = [0] * 16
        self.stack_pointer = 0
        self.delay_timer = 0
        self.sound_timer = 0

    def update_timers(self):
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1

    def fetch(self, memory):
        instruction = (memory[self.program_counter] << 8) | memory[self.program_counter + 1]
        self.program_counter += 2
        return instruction

    def decode(self, instruction):
        first_nibble = (instruction & 0xF000) >> 12
        x_register = (instruction & 0x0F00) >> 8
        y_register = (instruction & 0x00F0) >> 4
        last_nibble = instruction & 0x000F
        last_byte = instruction & 0x00FF
        address = instruction & 0x0FFF
        opcode = ''

        if first_nibble == 0x0:
            if last_byte == 0xE0:
                opcode = '00E0'
            elif last_byte == 0xEE:
                opcode = '00EE'

        elif first_nibble == 0x1:
            opcode = '1NNN'

        elif first_nibble == 0x2:
            opcode = '2NNN'

        elif first_nibble == 0x3:
            opcode = '3XNN'

        elif first_nibble == 0x4:
            opcode = '4XNN'

        elif first_nibble == 0x5:
            opcode = '5XY0'

        elif first_nibble == 0x6:
            opcode = '6XNN'

        elif first_nibble == 0x7:
            opcode = '7XNN'

        elif first_nibble == 0x8:
            if last_nibble == 0x0:
                opcode = '8XY0'
            elif last_nibble == 0x1:
                opcode = '8XY1'
            elif last_nibble == 0x2:
                opcode = '8XY2'
            elif last_nibble == 0x3:
                opcode = '8XY3'
            elif last_nibble == 0x4:
                opcode = '8XY4'
            elif last_nibble == 0x5:
                opcode = '8XY5'
            elif last_nibble == 0x6:
                opcode = '8XY6'
            elif last_nibble == 0x7:
                opcode = '8XY7'
            elif last_nibble == 0xE:
                opcode = '8XYE'

        elif first_nibble == 0x9:
            opcode = '9XY0'

        elif first_nibble == 0xA:
            opcode = 'ANNN'

        elif first_nibble == 0xB:
            opcode = 'BNNN'

        elif first_nibble == 0xC:
            opcode = 'CXNN'

        elif first_nibble == 0xD:
            opcode = 'DXYN'

        elif first_nibble == 0xE:
            if last_byte == 0x9E:
                opcode = 'EX9E'
            elif last_byte == 0xA1:
                opcode = 'EXA1'

        elif first_nibble == 0xF:
            if last_byte == 0x07:
                opcode = 'FX07'
            elif last_byte == 0x0A:
                opcode = 'FX0A'
            elif last_byte == 0x15:
                opcode = 'FX15'
            elif last_byte == 0x18:
                opcode = 'FX18'
            elif last_byte == 0x1E:
                opcode = 'FX1E'
            elif last_byte == 0x29:
                opcode = 'FX29'
            elif last_byte == 0x33:
                opcode = 'FX33'
            elif last_byte == 0x55:
                opcode = 'FX55'
            elif last_byte == 0x65:
                opcode = 'FX65'

        else:
            opcode = 'UNKNOWN'
            print(f'Unknown opcode: {instruction}')


        return {
            'opcode': opcode,
            'x_register': x_register,
            'y_register': y_register,
            'last_byte': last_byte,
            'address': address,
            'last_nibble': last_nibble
        }

    def execute(self, decoded_instruction, memory, display, keys):
        opcode = decoded_instruction['opcode']
        VX = decoded_instruction['x_register']
        VY = decoded_instruction['y_register']
        last_byte = decoded_instruction['last_byte']
        address = decoded_instruction['address']
        last_nibble = decoded_instruction['last_nibble']

        if opcode == '00E0': # Clear the display
            display.clear()

        elif opcode == '00EE':  # Return from subroutine
            self.stack_pointer -= 1
            self.program_counter = self.stack[self.stack_pointer]

        elif opcode == '1NNN':  # Jump to address NNN
            self.program_counter = address

        elif opcode == '2NNN':  # Call subroutine at NNN
            self.stack[self.stack_pointer] = self.program_counter
            self.stack_pointer += 1
            self.program_counter = address

        elif opcode == '3XNN':  # Skip next instruction if VX == NN
            if self.registers[VX] == last_byte:
                self.program_counter += 2

        elif opcode == '4XNN':  # Skip next instruction if VX != NN
            if self.registers[VX] != last_byte:
                self.program_counter += 2

        elif opcode == '5XY0':  # Skip next instruction if VX == VY
            if self.registers[VX] == self.registers[VY]:
                self.program_counter += 2

        elif opcode == '6XNN':  # Set VX to NN
            self.registers[VX] = last_byte

        elif opcode == '7XNN':  # Add NN to VX
            self.registers[VX] = (self.registers[VX] + last_byte) & 0xFF

        elif opcode == '8XY0':  # Set VX to VY
            self.registers[VX] = self.registers[VY]

        elif opcode == '8XY1':  # Set VX to VX OR VY
            self.registers[VX] |= self.registers[VY]

        elif opcode == '8XY2':  # Set VX to VX AND VY
            self.registers[VX] &= self.registers[VY]

        elif opcode == '8XY3':  # Set VX to VX XOR VY
            self.registers[VX] ^= self.registers[VY]

        elif opcode == '8XY4':  # Add VY to VX (with carry)
            result = self.registers[VX] + self.registers[VY]
            self.registers[0xF] = 1 if result > 0xFF else 0
            self.registers[VX] = result & 0xFF

        elif opcode == '8XY5':  # Set VX to VX - VY
            result = self.registers[VX] - self.registers[VY]
            self.registers[0xF] = 0 if result < 0 else 1
            self.registers[VX] = result & 0xFF

        elif opcode == '8XY6':  # Shift VX right by 1
            self.registers[0xF] = self.registers[VX] & 0x1
            self.registers[VX] >>= 1

        elif opcode == '8XY7':  # Set VX to VY - VX
            self.registers[0xF] = 1 if self.registers[VY] >= self.registers[VX] else 0
            self.registers[VX] = (self.registers[VY] - self.registers[VX]) & 0xFF

        elif opcode == '8XYE':  # Shift VX left by 1
            self.registers[0xF] = (self.registers[VX] & 0x80) >> 7
            self.registers[VX] = (self.registers[VX] << 1) & 0xFF

        elif opcode == '9XY0':  # Skip next instruction if VX != VY
            if self.registers[VX] != self.registers[VY]:
                self.program_counter += 2

        elif opcode == 'ANNN':  # Set I to address NNN
            self.index_register = address

        elif opcode == 'BNNN':  # Jump to address NNN + V0
            self.program_counter = address + self.registers[0x0]

        elif opcode == 'CXNN':  # Set VX to random byte AND NN
            random_value = random.randint(0, 255)
            self.registers[VX] = random_value & last_byte

        elif opcode == 'DXYN':  # Draw sprite at position VX, VY with N bytes of sprite data
            x = self.registers[VX]
            y = self.registers[VY]
            height = last_nibble
            if height == 0:
                height = 16

            sprite_data = []
            for i in range(height):
                sprite_data.append(memory[self.index_register + i])

            collision = display.draw_sprite(x, y, sprite_data, height)
            self.registers[0xF] = 1 if collision else False

        elif opcode == 'EX9E':  # Skip next instruction if key with the value of VX is pressed
            key = self.registers[VX]
            if keys[key]:
                self.program_counter += 2

        elif opcode == 'EXA1':  # Skip next instruction if key with the value of VX is not pressed
            key = self.registers[VX]
            if not keys[key]:
                self.program_counter += 2

        elif opcode == 'FX07':  # Set VX to the value of the delay timer
            self.registers[VX] = self.delay_timer

        elif opcode == 'FX0A':  # Wait for a keypress and store the result in VX
            if any(keys):
                for i in range(16):
                    if keys[i]:
                        self.registers[VX] = i
                        break
            else:
                self.program_counter -= 2

        elif opcode == 'FX15':  # Set delay timer to VX
            self.delay_timer = self.registers[VX]

        elif opcode == 'FX18':  # Set sound timer to VX
            self.sound_timer = self.registers[VX]

        elif opcode == 'FX1E':  # Add VX to I
            self.index_register += self.registers[VX]

        elif opcode == 'FX29':  # Set I to the location of the sprite for the character in VX
            self.index_register = self.registers[VX] * 5

        elif opcode == 'FX33':  # Store BCD representation of VX at addresses I, I+1, and I+2
            value = self.registers[VX]
            memory[self.index_register] = value // 100
            memory[self.index_register + 1] = (value // 10) % 10
            memory[self.index_register + 2] = value % 10

        elif opcode == 'FX55':  # Store registers V0-VX at memory location I
            for i in range(VX + 1): memory[self.index_register + i] = self.registers[i]

        elif opcode == 'FX65':  # Fill registers V0-VX with values stored at memory location I
            for i in range(VX + 1): self.registers[i] = memory[self.index_register + i]

        elif opcode == 'UNKNOWN':
            pass

    def cycle(self, memory, display, keys):
        instruction = self.fetch(memory)
        decoded_instruction = self.decode(instruction)
        self.execute(decoded_instruction, memory, display, keys)