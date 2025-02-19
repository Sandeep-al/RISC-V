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

        # giving instructions to their respective functions
        instruction = line.split()[0]
        if instruction in rTypeInstructions:
            pass
        elif instruction in stypeIntructions:
            pass
        elif instruction in btypeInstructions:
            pass
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