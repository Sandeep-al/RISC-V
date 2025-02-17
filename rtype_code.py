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
    list_of_line = line.replace(",", "").split()
    # giving instructions to their respective functions
    instruction = list_of_line[0]
    '''instruction = line.split()[0]'''
    string_of_binary = (
    main_dict[instruction][0] + rs_dict[list_of_line[3]] +
    rs_dict[list_of_line[2]] + main_dict[instruction][1] +
    rs_dict[list_of_line[1]] + main_dict[instruction][2]
)
    return string_of_binary
print(rType("add x1 x2 x3"))