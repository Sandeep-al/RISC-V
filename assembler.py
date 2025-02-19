"""" 
Code For RISC V Assembler
Made by: Pratyaksh Kumar -> Main Program Skeleton, readFile(), processFile(), errorHandling(), writeBinary(), collectLabels() and arguments. 
         Parth Verma 
         Sandeep
         Prateek Sharma       s
"""
# importing sys to get arguments
import sys

import Itype as sandeep
if len(sys.argv) != 3:
    print(">>> ERROR: Input and Output Files Not Provided")
    exit()



rTypeInstructions = ['add', 'sub', 'slt', 'srl', 'or', 'and']
itypeInstructions = ['lw', 'addi', 'jalr']
stypeIntructions = ['sw']
btypeInstructions = ['beq', 'bne']
jtypeInstructions = ['jal']

# array to hold all binary before finally writing them
toWrite = []

def writeBinary(outputPath):
    global toWrite
    with open(outputPath, "w") as f:
        for line in toWrite:
            f.write(line + "\n")
    return 0

def collectLabels(lines):
    pc = 0x00000000
    labelsDict = {}
    for line in lines:
        if ":" in line:
            labelsDict[ line.split(":")[0] ] = pc
        pc += 0x00000004
    return labelsDict

def errorHandling(lineNo, errorType):
    errorTypes = {
        0: ">>> ERROR: The Program Does Not Contain A Virtual Halt.",
        1: f">>> ERROR: Typo in Instruction at Line {lineNo}.",
        2: f">>> ERROR: Unknown Label Mentioned at Line {lineNo}",
        3: f">>> ERROR: Typo in Register Naming at Line {lineNo}"
    }

    with open(outputPath, "w") as f:
        f.write(errorTypes[errorType])
    exit()

def readFile(file):
    flagVirtualHalt = False

    # try block to load file and raise error if it doesn't exist.
    try:
        with open(file) as f:
            lines = []
            for line in f.readlines():
                if line.strip() != "":
                    
                    line = line.split("\n")[0]
                    if line == "beq zero,zero,0":
                        flagVirtualHalt = True

                    lines.append(line)

        # flag to check if a virtual halt is present in the program or not, will raise error if not!
        if flagVirtualHalt == False:
            errorHandling( None, 0)
            return 0
        
        return lines
    except:
        print(">>> The Input File Cannot Be Found ")
        return 0
#R type instructions
def rType(line):
    rs_dict = {
    "zero": "00000",
    "x0": "00000",
    "ra": "00001",
    "x1": "00001",
    "x2": "00010",
    "sp": "00010",
    "x3": "00011",
    "gp": "00011",
    "x4": "00100",
    "tp": "00100",
    "x5": "00101",
    "t0": "00101",
    "x6": "00110",
    "t1": "00110",
    "x7": "00111",
    "t2": "00111",
    "x8": "01000",
    "s0": "01000",
    "fp": "01000",
    "x9": "01001",
    "s1": "01001",
    "x10": "01010",
    "a0": "01010",
    "x11": "01011",
    "a1": "01011",
    "x12": "01100",
    "a2": "01100",
    "x13": "01101",
    "a3": "01101",
    "x14": "01110",
    "a4": "01110",
    "x15": "01111",
    "a5": "01111",
    "x16": "10000",
    "a6": "10000",
    "x17": "10001",
    "a7": "10001",
    "x18": "10010",
    "s2": "10010",
    "x19": "10011",
    "s3": "10011",
    "x20": "10100",
    "s4": "10100",
    "x21": "10101",
    "s5": "10101",
    "x22": "10110",
    "s6": "10110",
    "x23": "10111",
    "s7": "10111",
    "x24": "11000",
    "s8": "11000",
    "x25": "11001",
    "s9": "11001",
    "x26": "11010",
    "s10": "11010",
    "x27": "11011",
    "s11": "11011",
    "x28": "11100",
    "t3": "11100",
    "x29": "11101",
    "t4": "11101",
    "x30": "11110",
    "t5": "11110",
    "x31": "11111",
    "t6": "11111",
}
    main_dict = {'add':["0000000","000","0110011"], 'sub':["0100000","000","0110011"], 'slt':["0000000","010","0110011"], 'srl':["0000000","101","0110011"], 'or':["0000000","110","0110011"], 'and':["0000000","111","0110011"]}

    # handling lines with labels
    if ":" in line:
        line = line.split(":")[1].strip()
    list_of_line = line.replace(",", " ").split()
    # giving instructions to their respective functions
    instruction = list_of_line[0]
    instruction = line.split()[0]
    string_of_binary = (
    main_dict[instruction][0] + rs_dict[list_of_line[3]] +
    rs_dict[list_of_line[2]] + main_dict[instruction][1] +
    rs_dict[list_of_line[1]] + main_dict[instruction][2]
)
    return string_of_binary
     
register = {"zero": "00000", "ra": "00001", "sp": "00010", "gp": "00011",
    "t0": "00101", "t1": "00110", "t2": "00111",
    "s0": "01000", "s1": "01001", "a0": "01010", "a1": "01011",
    "s2": "01010",  
    "s3": "01100", "s4": "01101", "s5": "01110", 
    "s6": "01111"}

def Btype(line, labelsDict, pc, counter):
    elements=line.replace(",",  " ").split()
    instr=elements[0]   
    rs1=elements[1]     
    rs2=elements[2]    
    target=elements[3]  
    if target.startswith("0x") or target.isdigit():
        try:
            if target.startswith("0x"):
                value=int(target,16)  
            else:
                value=int(target)     
        except Exception as e:  
            errorHandling(counter, 4)
            return None
        offset=value
    else:
        if target not in labelsDict:  
            errorHandling(counter, 2)
            return None
        offset=labelsDict[target]-pc
    imm=format((offset >> 1) & 0xFFF, '012b') 
    opcode="1100011"  
    func3DICT={"beq": "000", "bne": "001", "blt": "100"}  
    if instr not in func3DICT:  
        errorHandling(counter, 1)
        return None
    funct3 = func3DICT[instr]
    binaryInstr = (imm[0]+imm[2:8]+register[rs2]+register[rs1]+funct3+imm[8:12]+imm[1]+opcode)
    return binaryInstr

def Stype(line, counter):
    opcode='0100011'   
    funct3='010'         
    elements=line.replace(",",   ' ').split()
    if len(elements)!=3:   
        errorHandling(counter, 1)
        return None
    regSRC=elements[1]       
    offset=elements[2]    
    offset=int(offset.split("(")[0])  
    base=offset.split("(")[1][:-1]   
    imm=format(offset & 0xFFF, '012b')   
    binary=(imm[:7]+register.get(base, '00000')+register.get(regSRC, '00000')+funct3+imm[7:]+opcode)
    return binary

def processFile(lines):
    # two passes, one for collecting labels and another for processing instructions.
    
    # first pass, collecting labels.
    labelsDict = collectLabels(lines)

    # second pass, processing labels.
    counter = 1
    pc = 0x00000000
    for line in lines:
        # handling lines with labels
        if ":" in line:
            line = line.split(":")[1].strip()
        num = line.replace(",", "").split()
        instruction = num[0]
        # giving instructions to their respective functions
        instruction = line.split()[0]
        if instruction in rTypeInstructions:
            output=rType(line)
            toWrite.append(output)
            pass
        elif instruction in stypeIntructions:
            binary = Stype(line, counter)
            if binary is None:
                errorHandling(counter, 1)
            toWrite.append(binary)
        elif instruction in btypeInstructions:
            binary = Btype(line, labelsDict, pc, counter)
            if binary is None:
                errorHandling(counter, 1)
            toWrite.append(binary)
        elif instruction in itypeInstructions:
            toWrite.append((sandeep.breakinstruction(line,labelsDict,pc,counter)))
        elif instruction in jtypeInstructions:
            toWrite.append((sandeep.breakinstruction(line,labelsDict,pc,counter)))
        else:
            errorHandling(counter, 1)
        
        counter+= 1
        pc += 0x00000004

    
    # Writing Binary To Output File
    writeBinary(outputPath)
    print(f">>> {inputPath} processed as {outputPath}")


inputPath = sys.argv[1]
outputPath = sys.argv[2]


processFile(readFile(inputPath))