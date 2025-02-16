dict1={"lw":["0000011","010"],"addi":["0010011","000"],"jalr":["1100111","000"]
       ,"jal":["1101111"]}
rs_dict = {
    "00000": ["x0", "zero"],
    "00001": ["x1", "ra"],
    "00010": ["x2", "sp"],
    "00011": ["x3", "gp"],
    "00100": ["x4", "tp"],
    "00101": ["x5", "t0"],
    "00110": ["x6", "t1"],
    "00111": ["x7", "t2"],
    "01000": ["x8", "s0", "fp"],
    "01001": ["x9", "s1"],
    "01010": ["x10", "a0"],
    "01011": ["x11", "a1"],
    "01100": ["x12", "a2"],
    "01101": ["x13", "a3"],
    "01110": ["x14", "a4"],
    "01111": ["x15", "a5"],
    "10000": ["x16", "a6"],
    "10001": ["x17", "a7"],
    "10010": ["x18", "s2"],
    "10011": ["x19", "s3"],
    "10100": ["x20", "s4"],
    "10101": ["x21", "s5"],
    "10110": ["x22", "s6"],
    "10111": ["x23", "s7"],
    "11000": ["x24", "s8"],
    "11001": ["x25", "s9"],
    "11010": ["x26", "s10"],
    "11011": ["x27", "s11"],
    "11100": ["x28", "t3"],
    "11101": ["x29", "t4"],
    "00000": ["x0", "zero"],
    "00001": ["x1", "ra"],
    "00010": ["x2", "sp"],
    "00011": ["x3", "gp"],
    "00100": ["x4", "tp"],
    "00101": ["x5", "t0"],
    "00110": ["x6", "t1"],
    "00111": ["x7", "t2"],
    "01000": ["x8", "s0", "fp"],
    "01001": ["x9", "s1"],
    "01010": ["x10", "a0"],
    "01011": ["x11", "a1"],
    "01100": ["x12", "a2"],
    "01101": ["x13", "a3"],
    "01110": ["x14", "a4"],
    "01111": ["x15", "a5"],
    "10000": ["x16", "a6"],
    "10001": ["x17", "a7"],
    "10010": ["x18", "s2"],
    "10011": ["x19", "s3"],
    "10100": ["x20", "s4"],
    "10101": ["x21", "s5"],
    "10110": ["x22", "s6"],
    "10111": ["x23", "s7"],
    "11000": ["x24", "s8"],
    "11001": ["x25", "s9"],
    "11010": ["x26", "s10"],
    "11110": ["x30", "t5"],
    "11111": ["x31", "t6"],
}


def decimaltobin(n,x):
    if n<0:
        n=2**x+n    
    return format(n, f'0{str(x)}b')
    

def breakinstruction(i,labelsDict,pc):
    if i[0:2]=="lw":
        a="lw"
        i=i[3:]
        i.strip()
        i=i.split(",")
        rd=i[0]
        i=i[1].split("(")
        imm=int(i[0])
        rs1=i[1][0:2]
        

    elif i[0:4]=="addi":
         a="addi"
         i=i[5:]
         i.strip()
         i=i.split(",")
         rd=i[0]
         imm=int(i[2])
         rs1=i[1]
        
    elif i[0:4]=="jalr":
        a="jalr"
        i=i[5:]
        i.strip()
        i=i.split(",")
        rd=i[0]
        imm=int(i[2])
        rs1=i[1]

    elif i[0:3]=="jal":
        a="jal"
        i=i[4:]
        i.strip()
        i=i.split(",")
        rd=i[0]
        
        imm=i[1]
        if imm in labelsDict:
            imm=labelsDict[imm]-pc
            
        else:
             imm=int(imm)
        
        return Jtypeinstructions(a,imm,rd)
    return Itypeinstructions(a,imm,rd,rs1)    
def Itypeinstructions(op,imm,rd,rs1):
    for j,i in rs_dict.items():
            if rs1 in i:
                a=j
                break
    for j,i in rs_dict.items():
            if rd in i:
                b=j
                break
    
    x=f'{decimaltobin(imm,12)} {a} {dict1[op][1]} {b} {dict1[op][0]}'
    return x

def Jtypeinstructions(op,imm,rd):
    for j,i in rs_dict.items():
            if rd in i:
                b=j
                break
    x=f'{decimaltobin(imm,20)} {b} {dict1[op][0]}'
    return x




