"""" 
Code For RISC V Assembler
Made by: Pratyaksh Kumar -> Main Program Skeleton, readFile(), processFile(), errorHandling(), writeBinary(), collectLabels() and arguments. 
         Parth Verma 
         Sandeep
         Prateek Sharma
"""
# importing sys to get arguments
import sys

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
registerMap = {
    "zero": "00000", "ra": "00001", "sp": "00010", "gp": "00011",
    "t0": "00101", "t1": "00110", "t2": "00111",
    "s0": "01000", "s1": "01001", "a0": "01010", "a1": "01011",
    "a2": "01100", "a3": "01101", "a4": "01110", "a5": "01111",
    "s2": "10000", "s3": "10001", "s4": "10010", "s5": "10011",
}        
# Function S-type
def processSType(num):
    opcode = "0100011"
    funct3 = "010"
    rs2 = registerMap.get(num[1], "00000")
    imm = format(int(num[2]), '012b')
    rs1 = registerMap.get(num[3], "00000")
    high= imm[:7]
    low=imm[7:]
    return high + rs2 + rs1 + funct3 + low + opcode

# Function B-type
def processBType(num, pc, labelsDict):
    opcode = "1100011"
    funct3 = "000" if num[0] == "beq" else "001"
    rs1 = registerMap.get(num[1], "00000")
    rs2 = registerMap.get(num[2], "00000")
    if num[3] not in labelsDict:
        return ("ERROR: Unknown labelsDict ",num[3])
    set = labelsDict[num[3]] - pc
    imm = format(set, '013b')
    Bimm = imm[0] + imm[2:8] + imm[8:12] + imm[1]
    return Bimm[:7] + rs2 + rs1 + funct3 + Bimm[7:] + opcode

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
            pass
        elif instruction in stypeIntructions:
            binary = processSType(num)
            toWrite.append(binary)
        elif instruction in btypeInstructions:
            binary = processBType(num, pc, labelsDict)
            toWrite.append(binary)
        elif instruction in itypeInstructions:
            pass
        elif instruction in jtypeInstructions:
            pass
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