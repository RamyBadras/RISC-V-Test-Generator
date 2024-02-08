import random

def generate_instruction(count = 30, MemorySize = 400, skipJalrNJal = False, skipStore = False, skipLoad = False):

    # All riscV instructions
    generated_instructions = []
    generated_instructions_binary = []
    initialized_registers = []
    initialized_registers.append("x0")


    instructions = ["add", "addi", "and", "andi", "auipc","beq",
                    "bge", "bgeu", "blt", "bltu", "bne", "jal", "jalr", 
                    "lb", "lbu", "lh", "lhu", "lui", "lw", "or", "ori", "sb", "sh", "sll", "slli", "slt",
                        "slti", "sltiu", "sltu", "sra", "srai", "srl", "srli", "sub", "sw", "xor", "xori"]
    # All riscV instructions with 3 operands
    three_operand = ["add", "and", "or", "slt", "sltu", "sll", "sra", "srl", "sub", "xor"]
    # All riscV instructions with 2 operands
    two_operand = ["addi", "andi", "beq", "bge", "bgeu", "blt", "bltu", "bne", "jalr", 
                    "lb", "lbu", "lh", "lhu", "lw", "ori", "sb", "sh", "slti", "sltiu", "sw", "xori", "slli", "srai", "srli"]
    # All riscV instructions with 1 operand
    one_operand = ["jal", "lui", "auipc"]

    registers = [ "x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7", 
                    "x8", "x9", "x10", "x11", "x12", "x13", "x14", "x15", 
                    "x16", "x17", "x18", "x19", "x20", "x21", "x22", "x23", 
                        "x24", "x25", "x26", "x27", "x28", "x29", "x30", "x31"]

    opcodes_dict = {"add": "0110011", "addi": "0010011", "and": "0110011", "andi": "0010011", 
                    "auipc": "0010111", "beq": "1100011", "bge": "1100011", "bgeu": "1100011",
                    "blt": "1100011", "bltu": "1100011", "bne": "1100011", "jal": "1101111",
                    "jalr": "1100111",  "srai": "0010011", "srl": "0110011", "srli": "0010011",
                    "sub": "0110011", "sw": "0100011", "xor": "0110011", "xori": "0010011",
                    "lb": "0000011", "lbu": "0000011", "lh": "0000011", "lhu": "0000011",
                    "lui": "0110111", "lw": "0000011", "or": "0110011", "ori": "0010011",
                    "sb": "0100011", "sh": "0100011", "sll": "0110011", "slli": "0010011",
                    "slt": "0110011", "slti": "0010011", "sltiu": "0010011", "sltu": "0110011",
                    "sra": "0110011", "fence": "0001111", "ecall": "1110011", "ebreak": "1110011"}
    
    funct3_dict = {"add": "000", "addi": "000", "and": "111", "andi": "111",
                   "auipc": "000", "beq": "000", "bge": "101", "bgeu": "111",
                    "blt": "100", "bltu": "110", "bne": "001", "jal": "000",
                    "jalr": "000", "srai": "101", "srl": "101", "srli": "101",
                    "sub": "000", "sw": "010", "xor": "100", "xori": "100",
                    "lb": "000", "lbu": "100", "lh": "001", "lhu": "101",
                    "lui": "000", "lw": "010", "or": "110", "ori": "110",
                    "sb": "000", "sh": "001", "sll": "001", "slli": "001",
                    "slt": "010", "slti": "010", "sltiu": "011", "sltu": "011",
                    "sra": "101", "fence": "000", "ecall": "000", "ebreak": "000"} 


    while(len(generated_instructions) < count-4):

        i = len(generated_instructions)

        instruction = random.choice(instructions)

        rd = random.choice(registers)

        if len(initialized_registers) > 1:
            rs1 = random.choice(initialized_registers)
            rs2 = random.choice(initialized_registers)
        else:
            rs1 = random.choice(registers)
            rs2 = random.choice(registers)

        if instruction in three_operand:
            if rs1 not in initialized_registers or rs2 not in initialized_registers:
                continue
            else:
                generated_instructions_binary.append(binaryInstruction(funct3_dict, opcodes_dict, instruction, int(rs1[1:]), int(rs2[1:]), int(rd[1:])))
                instruction += " " + rd + ", " + rs1 + ", " + rs2
                initialized_registers.append(rd)

        elif instruction in two_operand:

            # Branching instructions
            if instruction == "beq" or instruction == "bge" or instruction == "bgeu" or instruction == "blt" or instruction == "bltu" or instruction == "bne":
                if rs1 not in initialized_registers or rs2 not in initialized_registers:
                    continue
                else:
                    offset = 4*random.randint(-(i), count-i-1)
                    generated_instructions_binary.append(binaryInstruction(funct3_dict, opcodes_dict, instruction, int(rs1[1:]), int(rs2[1:]), 0, offset))
                    instruction += " " + rs1 + ", " + rs2 + ", " + str(offset)
            
            # Load instructions
            elif instruction == "lb" or instruction == "lbu" or instruction == "lh" or instruction == "lhu" or instruction == "lw":
                if rs1 not in initialized_registers or skipLoad:
                    continue
                else:
                    offset = random.randint(-(MemorySize/2), MemorySize/2)
                    generated_instructions_binary.append(binaryInstruction(funct3_dict, opcodes_dict, instruction, int(rs1[1:]), 0, int(rd[1:]), offset))
                    instruction += " " + rd + ", " + rs1 + ", " + str(offset)
                    initialized_registers.append(rd)

            # Store instructions
            elif instruction == "sb" or instruction == "sh" or instruction == "sw":
                if rs1 not in initialized_registers or rs2 not in initialized_registers or skipStore:
                    continue
                else:
                    offset = random.randint(-(MemorySize/2), MemorySize/2)
                    generated_instructions_binary.append(binaryInstruction(funct3_dict, opcodes_dict, instruction, int(rs1[1:]), int(rs2[1:]), 0, offset))
                    instruction += " " + rs2 + ", " + rs1 + ", " + str(offset)

            # JALR instruction
            elif instruction == "jalr":
                if rs1 not in initialized_registers or skipJalrNJal:
                    continue
                else:
                    offset = random.randint(-(MemorySize/2), MemorySize/2)
                    generated_instructions_binary.append(binaryInstruction(funct3_dict, opcodes_dict, instruction, int(rs1[1:]), 0, int(rd[1:]), offset))
                    instruction += " " + rd + ", " + rs1 + ", " + str(offset)
                    initialized_registers.append(rd)


            # Shifting instructions
            elif instruction == "slli" or instruction == "srai" or instruction == "srli":
                if rs1 not in initialized_registers:
                    continue
                else:
                    shamt = random.randint(0, 31)
                    generated_instructions_binary.append(binaryInstruction(funct3_dict, opcodes_dict, instruction, int(rs1[1:]), 0, int(rd[1:]), shamt))
                    instruction += " " + rd + ", " + rs1 + ", " + str(shamt)
                    initialized_registers.append(rd)

            else:
                if rs1 not in initialized_registers:
                    continue
                else:
                    immediate = random.randint(-1023, 1023)
                    generated_instructions_binary.append(binaryInstruction(funct3_dict, opcodes_dict, instruction, int(rs1[1:]), 0, int(rd[1:]), immediate))
                    instruction += " " + rd + ", " + rs1 + ", " + str(immediate)
                    initialized_registers.append(rd)


        elif instruction in one_operand:

            if instruction == "auipc" or instruction == "lui":
                immediate = random.randint(0, 1048575)
                generated_instructions_binary.append(binaryInstruction(funct3_dict, opcodes_dict, instruction, 0, 0, int(rd[1:]), immediate))
                instruction += " " + rd + ", " + str(immediate)
                initialized_registers.append(rd)

            elif instruction == "jal" or skipJalrNJal:
                if i > 5:
                    offset = 4*random.randint(-(i), count-i-1)    
                    generated_instructions_binary.append(binaryInstruction(funct3_dict, opcodes_dict, instruction, 0, 0, int(rd[1:]), offset))
                    instruction += " " + rd + ", " + str(offset)
                    initialized_registers.append(rd)
                else:
                    continue

            else: 
                immediate = random.randint(0, 31)
                generated_instructions_binary.append(binaryInstruction(funct3_dict, opcodes_dict, instruction, 0, 0, int(rd[1:]), immediate))
                instruction += " " + rd + ", " + str(immediate)
                initialized_registers.append(rd)


        generated_instructions.append(instruction)

    # Final additions and Ebreak.
    generated_instructions.append("ebreak")
    generated_instructions_binary.append(binaryInstruction(funct3_dict = funct3_dict, opcodes_dict = opcodes_dict ,instruction = "ebreak"))
    generated_instructions.append("addi x1, x0, -1")
    generated_instructions_binary.append(binaryInstruction(funct3_dict, opcodes_dict, instruction = "addi", rs1 = 0, rs2 = 0, rd = 1, imm = -1))

    index = random.randint(0, len(generated_instructions)-1)
    generated_instructions.insert(index, "fence")
    generated_instructions_binary.insert(index, binaryInstruction(funct3_dict=funct3_dict, opcodes_dict=opcodes_dict, instruction = "fence"))

    index = random.randint(0, len(generated_instructions)-1)
    generated_instructions.insert(index, "ecall")
    generated_instructions_binary.insert(index, binaryInstruction(funct3_dict=funct3_dict, opcodes_dict=opcodes_dict ,instruction = "ecall"))

    print("Generated instructions: ", len(generated_instructions))
    print(initialized_registers)
    return generated_instructions, generated_instructions_binary

def getBinary(number, bits):
    if number < 0:
        positive_binary = bin(abs(number))[2:].zfill(bits)
        inverted_bits = ''.join('1' if bit == '0' else '0' for bit in positive_binary)
        twos_complement = bin(int(inverted_bits, 2) + 1)
        return twos_complement[2:].zfill(bits)
    else:
        return bin(number)[2:].zfill(bits)

def binaryInstruction(funct3_dict = "000", opcodes_dict = "0000000", instruction = "", rs1 = 0, rs2 = 0, rd = 0, imm = 0):
    if  instruction == "ebreak":
        return str("00000000000100000000000001110011")
    elif instruction == "fence":
        return str("00000000000000000000000000001111")
    elif instruction == "ecall":
        return str("00000000000000000000000001110011")
    elif instruction == "lui" or "auipc":
        return str(getBinary(imm, 20) + getBinary(rd, 5) + opcodes_dict[instruction])
    elif instruction == "jal":
        immediate = getBinary(imm, 20)
        return str(immediate[20] + immediate[1:10] + immediate[11] + immediate[12:19], getBinary(rd, 5), opcodes_dict[instruction])
    elif instruction == "jalr":
        return str(getBinary(imm, 12) + getBinary(rs1, 5) + funct3_dict[instruction] + getBinary(rd, 5) + opcodes_dict[instruction])
    elif instruction == "beq" or instruction == "bge" or instruction == "bgeu" or instruction == "blt" or instruction == "bltu" or instruction == "bne":
        return str(getBinary(imm, 12) + getBinary(rs2, 5) + getBinary(rs1, 5) + funct3_dict[instruction] + opcodes_dict[instruction])
    elif instruction == "lb" or instruction == "lbu" or instruction == "lh" or instruction == "lhu" or instruction == "lw":
        return str(getBinary(imm, 12) + getBinary(rs1, 5) + funct3_dict[instruction] + getBinary(rd, 5) + opcodes_dict[instruction])
    elif instruction == "sb" or instruction == "sh" or instruction == "sw":
        immediate = getBinary(imm, 12)
        return str(immediate[5:11] + getBinary(rs2, 5) + getBinary(rs1, 5) + funct3_dict[instruction] + opcodes_dict[instruction])
    elif instruction == "addi" or instruction == "slti" or instruction == "sltui" or instruction == "xori" or instruction == "ori" or instruction == "andi":
        return str(getBinary(imm, 12) + getBinary(rs1, 5) + funct3_dict[instruction] + getBinary(rd, 5) + opcodes_dict[instruction])
    elif instruction == "srai":
        return str("0100000" + getBinary(imm, 5) + getBinary(rs1, 5) + funct3_dict[instruction] + getBinary(rd, 5) + opcodes_dict[instruction])
    elif instruction == "slli" or instruction == "srli":
        return str("0000000" + getBinary(imm, 5) + getBinary(rs1, 5) + funct3_dict[instruction] + getBinary(rd, 5) + opcodes_dict[instruction])
    elif instruction == "sub" or instruction == "sra":
        return str("0100000" + getBinary(rs2, 5) + getBinary(rs1, 5) + funct3_dict[instruction] + getBinary(rd, 5) + opcodes_dict[instruction])
    else:
        return str("0000000" + getBinary(rs2, 5) + getBinary(rs1, 5) + funct3_dict[instruction] + getBinary(rd, 5) + opcodes_dict[instruction])
    

if __name__ == "__main__":

    ''' Jal and Jalr have very unpredictable outputs as it could output 
    Jalr x12, x5, 100, where x5 might have an unreasonable value, so i added option to omit Jal and Jalr
    Similarly for Load and Store since this program doesn't mind loading from a negative address...'''

    instructions , binary_instructions = generate_instruction(50, skipJalrNJal=False, skipStore=False, skipLoad=False)
    hex_instructions = [] 

    for instruction in binary_instructions:
        hex_instructions.append(hex(int(instruction, 2))[2:].zfill(8))

    for instruction in instructions:
        print(instruction)

    for instruction in binary_instructions:
        print(instruction)

    for instruction in hex_instructions:
        print(instruction)

    # Destination of Hex file.
    output_file = '/'

    with open(output_file, 'w') as file:
    # Iterate through the array in reverse order
        for hex_value in hex_instructions:
            reversed = hex_value[6:8] + " " + hex_value[4:6] + " "  + hex_value[2:4] + " "  + hex_value[0:2]
            file.write(reversed.upper() + '\n')

    print(f"Values written to '{output_file}'")