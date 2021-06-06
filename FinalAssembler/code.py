import Parser
#dests = {"null": "000", "M":"001","D":"001","MD":"011","A":"100","AM":"101","AD":"110","AMD":"111"}
#jumps = {"null": "000", "JGT":"001","JEQ":"001","JGE":"011","JLT":"100","JNE":"101","JLE":"110","JMP":"111"}
comps = {"0":"101010",
        "1":"111111",
        "-1":"111010",
        "D":"001100",
        "A":"110000",
        "M":"110000",
        "!D":"001101",
        "-A":"110011",
        "-M":"110011",
        "D+1":"011111",
        "A+1":"110111",
        "M+1":"110111",
        "D-1":"001110",
        "A-1":"110010",
        "M-1":"110010",
        "D+A":"000010",
        "D+M": "000010",
        "D-A":"010011",
        "D-M":"010011",
        "A-D":"000111",
        "M-D":"000111",
        "D&A":"000000",
        "D&M": "000000",
        "D|A":"010101",
        "D|M":"010101"}

def AInstruction():
  # Gets binary value of A Instruction
  binnumber = str(bin(int(Parser.translateAInstruction()))).lstrip("0b")
  # Adds 0s if necessary to make it long enough
  if len(binnumber) < 15:
    n = 15 - len(binnumber)
    binnumber = "0"*n + binnumber
  return binnumber

def comp():
  # If M is in it, set a bit to true, use dictionary for rest
  asmcomp = str(Parser.comp())
  a="0"
  if "M" in asmcomp:
    a="1"
  return a + comps[asmcomp]

def dest():
  #Sets destination bits to be true depending on if A, M, and/or D
  asmdest = str(Parser.dest())
  d1=d2=d3="0"
  if "A" in asmdest:
    d1="1"
  if "D" in asmdest:
    d2="1"
  if "M" in asmdest:
    d3="1"    
  return d1 + d2 + d3

def jump():
  # Sets jump bits to be true based on different patterns
  asmjump = str(Parser.jump())
  j1=j2=j3="0"
  if "L" in asmjump:
    j1="1"
  if "G" in asmjump:
    j3="1"
  if "E" in asmjump and "N" not in asmjump:
    j2="1"
  if "NE" in asmjump:
    j1=j3="1"
  if "M" in asmjump:
    j1=j2=j3="1"
  return j1 + j2 + j3

