"""" 
Code For RISC V Assembler
Made by: Pratyaksh Kumar
         Parth Verma
         Sandeep
         Prateek Sharma
"""

def readFile(file):
    try:
        with open(file) as f:
            pass
    except:
        print(">>> The Input File Cannot Be Found ")
        