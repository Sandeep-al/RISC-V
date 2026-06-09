"""
Simulator Program Code by Pratyaksh, Sandeep, Parth and Prateek.
2022431,
"""

import sys


if len(sys.argv) <3:
    print(">>> ERROR: Input and Output Files Not Provided")
    exit()
inputPath = sys.argv[1]
outputPath = sys.argv[2]


with open(outputPath, 'w') as f:
    pass


instructionsOPCodeMapping = {
    'rType': ['0110011'],
    'iType': ['0000011', '0010011', '1100111'],
    'sType': ['0100011'],
    'bType': ['1100011'],
    'jType': ['1101111']
}


registerNames = ['00000', '00001', '00010', '00011', '00100', '00101', '00110', '00111','01000', '01001', '01010', '01011', '01100', '01101', '01110', '01111','10000', '10001', '10010', '10011', '10100', '10101', '10110', '10111', '11000', '11001', '11010', '11011', '11100', '11101', '11110', '11111']
registers = {key: 0 for key in registerNames }

pc = 0

memory = {}

for addr in range(0x0, 0x100, 4):
    memory[addr] = None

for addr in range(0x100, 0x180, 4):
    memory[addr] = 0

for addr in range(0x10000, 0x10080, 4):
    memory[addr] = 0





registers['00010'] = 380  # x2 = 380 


def to_32bit_signed(value):
    value = value & 0xFFFFFFFF
    return value if value <= 0x7FFFFFFF else value - 0x100000000


# Simulating R Type Instructions -> Parth
def executeRtype(instruction, lineNo):

    global registers
    funct7 = instruction[0:7]  
    rs2 = instruction[7:12]       
    rs1 = instruction[12:17]   
    funct3 = instruction[17:20]     
    rd = instruction[20:25]    
    opcode = instruction[25:32]  
   

    main_dict={
    ("0000000", "000", "0110011"): "add",
    ("0100000", "000", "0110011"): "sub",
    ("0000000", "010", "0110011"): "slt",
    ("0000000", "101", "0110011"): "srl",
    ("0000000", "110", "0110011"): "or",
    ("0000000", "111", "0110011"): "and"
    }
    
    if (rd not in registers) or (rs1 not in registers) or (rs2 not in registers):
        print("invalid register! please check the register at lineNo", lineNo)
        return False
    elif rd == "00000":
        print("Cannot update x0 at lineNo", lineNo)
        return  False       

    else:
        if (funct7, funct3, opcode) in main_dict:
            operation = main_dict[(funct7, funct3, opcode)]
            if operation == "add":
                if rd != "00000":
                    registers[rd] = to_32bit_signed(registers[rs1] + registers[rs2])
            elif operation == "sub":
                if rd != "00000":
                    registers[rd] = to_32bit_signed(registers[rs1] - registers[rs2])
            elif operation == "slt":
                if rd != "00000":
                    registers[rd] = to_32bit_signed(1 if registers[rs1] < registers[rs2] else 0)
            elif operation == "srl":
                if rd != "00000":
                    registers[rd] = to_32bit_signed(registers[rs1] >> registers[rs2])
            elif operation == "or":
                if rd != "00000":
                    registers[rd] = to_32bit_signed(registers[rs1] | registers[rs2])
            elif operation == "and":
                if rd != "00000":
                    registers[rd] = to_32bit_signed(registers[rs1] & registers[rs2])
            else:
                print("invalid operator! kindly correct the operator. at lineNo", lineNo)
                return False
        else:
            print("invalid R Type instruction, please change it. at lineNo", lineNo)
            return False
    return 

# Simulating S Type Instructions -> Pratyaksh
def executeSType(instruction, lineNo):
    global memory
    # converting to integers
    rs2 = instruction[7:12]
    rs1 = instruction[12:17]
    funct3 = instruction[17:20]

    imm11to5 = int(instruction[0:7], 2)
    imm4to0 = int(instruction[20:25], 2)
    imm = (imm11to5 << 5) | imm4to0
    
    if (imm >> 11) & 1:
        imm -= 1 << 12

    
    # Illegal Funct3
    if funct3 != '010':
        print("Illegal Funct3 in S Type, at Line No ", lineNo)
        return False
    
    # Illegal Register Namings
    if (rs1 not in registerNames) or (rs2 not in registerNames):
        print("Illgal Register Names in S Type at Line No", lineNo)
        return False

    address = registers[rs1] + imm 
    
    # print(f"Decoded rs1: x{rs1} = {registers[rs1]}, rs2: x{rs2} = {registers[rs2]}, imm: {imm}, Address: {address}")

    if address %4 != 0:
        print("Address Not A Multiple Of 4 Any Longer, Exiting, at line no", lineNo)
        return False
    
    # print(f"DEBUG: Storing value {registers[rs2]} at {hex(address)} (Base Reg: {rs2}, Offset: {imm})")

   
    
    memory[address] = registers[rs2]

# Simulating J Type Instructions -> Pratyaksh
def executeJType(instruction):
    global pc
    global registers
    rd = instruction[-12:-7]  
    imm20 = instruction[0]
    imm10_1 = instruction[1:11]
    imm11 = instruction[11]
    imm19_12 = instruction[12:20]
    imm = int(imm20 + imm19_12 + imm11 + imm10_1 + '0' , 2)

    if imm & (1 << 20):
        imm -= (1 << 21)

    registers[rd] = pc + 4
    pc = pc + imm



# Simulating I Type Instructions -> Sandeep
def bintodecimal(x):
    
    return int(x, 2)
 
def signextender(x):
    if x[0] == '1': 
        return '1' * (32 - len(x)) + x  
    else:
        return '0' * (32 - len(x)) + x  




def executeItype(x, lineNo):
    op = x[25:32]
    rd = x[20:25] 
    funct3 = x[17:20]  
    rs1 = x[12:17]  
    imm = x[0:12]

    # print("\n ----------------- IN I TYPE --------------")
    # print(f"op: {op}")
    # print(f"rd: {rd}")  
    # print(f"funct3: {funct3}")
    # print(f"rs1: {rs1}")
    # print(f"imm: {imm}")
    global pc
    global registers



    if op=="0000011":  #lw word


        imm=signextender(imm)
        rs1 = registers[rs1]

        
        hx=int(imm,2)+rs1


        if hx in memory:
            registers[rd] = memory[hx]
        else:
            print("Memory not found, at lineNo", lineNo)
            print(hex(hx))
        pc=pc+4

    

    elif op=="0010011":
        imm=signextender(imm)
        rs1=registers[rs1]
        
        hx=int(imm,2)+rs1
        registers[rd] = to_32bit_signed(hx)
        pc=pc+4


    
    elif op == "1100111":  # jalr

        if rd != "00000":  
            registers[rd] = pc + 4

        
        imm = int(signextender(imm), 2)
        temp_pc = registers[rs1] + imm


        temp_pc = (registers[rs1] + imm) & 0xFFFFFFFF
        pc = temp_pc & ~1



    
    # print(" ----------------- OUT I TYPE -------------- \n")


# Simulating B Type Instructions -> Prateek
def executeBtype(instruction):
    global pc
    global registers
    funct3 = instruction[17:20]
    rs1 = instruction[12:17]
    rs2 = instruction[7:12]
    imm12 = instruction[0]
    imm10_5 = instruction[1:7]
    imm4_1 = instruction[20:24]
    imm11 = instruction[24]
    imm = int(imm12 + imm11 + imm10_5 + imm4_1 + '0', 2)

    if imm & (1 << 12):
        imm -= 1 << 13

    # print(imm)
    if funct3 == '000' and rs1 == '00000' and rs2 == '00000' and imm == 0:
        return False

    if funct3 == '000':  # BEQ
        if registers[rs1] == registers[rs2]:
            pc += imm
        else:
            pc += 4
            
    elif funct3 == '001':
        if registers[rs1] != registers[rs2]:
            pc += imm
            

        else:
            pc += 4
            
    return True


def readFile(file):
    
    try:
        with open(file) as f:
            lines = []
            for line in f.readlines():
                if line.strip() != "":   
                    line = line.split("\n")[0]
                    lines.append(line)
        return lines
    except:
        print(">>> The Input File Cannot Be Found ")
        return 0

def writeAfterEachExecution():
    global outputPath

    
    toWrite = f"0b{bin(pc)[2:].zfill(32)} "
    # toWrite = f"{pc} "

    
    for key in registers:
        value = registers[key]
        
        if value > 0x7FFFFFFF: 
            value -= (1 << 32)  
        toWrite += f"0b{bin(value & 0xFFFFFFFF)[2:].zfill(32)} "
        # toWrite += f"{value} "

    # Write the output to the file
    with open(outputPath, "a") as f:
        f.write(toWrite + "\n")

def finalWrite():
    linesToWrite = []
    for address in {k: v for k, v in memory.items() if k >= 65536}:
        linesToWrite.append(
            f"0x{address:08X}:0b{bin(memory[address])[2:].zfill(32)}\n"
            # f"0x{address:08X}:{memory[address]}\n"
        )

    with open(outputPath, "a" ) as f:
        f.writelines(linesToWrite)

def processInstructions(lines):
    global pc 
    # print(registers)

    
    while pc < len(lines) * 4:

        instruction = lines[pc // 4]
        lineNo = lines.index(instruction)
        
        opcode = instruction[-7:]

        if opcode in instructionsOPCodeMapping['rType']:
            # print("R TYPE")

            executeRtype(instruction, lineNo)
            pc += 4
            writeAfterEachExecution()
            # print(registers)
            
        elif opcode in instructionsOPCodeMapping['iType']:
            # print("I TYPE")
            executeItype(instruction, lineNo)
            writeAfterEachExecution()
            # print(registers)
        elif opcode in instructionsOPCodeMapping['sType']:
            # print("S TYPE")
            executeSType(instruction, lineNo)
            pc += 4
            writeAfterEachExecution()
            # print(registers)
           
        elif opcode in instructionsOPCodeMapping['bType']:
            # print("B TYPE")
            if executeBtype(instruction) == False:
                writeAfterEachExecution()
                # print(registers)
                break
            else:
                writeAfterEachExecution()
                # print(registers)
            


        elif opcode in instructionsOPCodeMapping['jType']:
            # print("J Type")
            executeJType(instruction)
            writeAfterEachExecution()
            # print(registers)
        else:
            pass
        # print("pc", pc)

        

    finalWrite()
    # print(registers)
processInstructions(readFile(inputPath))