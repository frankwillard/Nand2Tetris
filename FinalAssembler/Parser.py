currentLine=0
A=False
symbols = {"R0": "0", "R1": "1","R2":"2","R3":"3","R4":"4","R5":"5","R6":"6","R7":"7", "R8": "8", "R9": "9","R10":"10","R11":"11","R12":"12","R13":"13","R14":"14","R15":"15", "SCREEN":"16384","KBD":"24576", "SP":"0","LCL":"1","ARG":"2","THIS":"3","THAT":"4"}

def Parser(newfile):
  #Opens and reads the file
  myfile = open(newfile, "r")
  global data
  data = myfile.readlines()


def removeWhiteSpace():
  n = 0
  global data
  for i in range(len(data)):
    #Remove spaces/whitespace
    data[n] = "".join(data[n].split())
    #Remove comments from line- if entire line is comment, remove the line
    if "//" in data[n]:
      comment = data[n].find("//")
      if comment == 0:
        data[n] = ""
      else:
        data[n] = data[n][0:comment]
    if data[n] == "":
      data.remove(data[n])
      n-=1
    n+=1



def fixLabels():
  #Adds label and instruction number to symbol table and removes the line
  n=0
  for i in range(len(data)):
    if "(" in data[n]:
      left = data[n].find("(")
      right= data[n].find(")")
      label = data[n][left+1:right]
      if label not in symbols:
        symbols[label] = str(n)
        data.remove(data[n])
        n-=1
    n+=1

def fixVariables():
  # If they use a variable for address, adds variable and next available address to symbol table
  nextAddr = 16
  for i in range(len(data)):
    if "@" in data[i]:
      var = data[i].lstrip("@")
      if not var.isdigit():
        if var not in symbols:
          symbols[var] = str(nextAddr)
          nextAddr+=1
        data[i] = "@" + symbols[var]

def categorize():
  # Determines if A Instruction or C Instruction
  global A
  if "@" in data[currentLine]:
    A=True
    translateAInstruction()
  else:
    A=False
    translateCInstruction()

def translateAInstruction():
  #Removes "@", uses number or label's associated instruction number from symbol table
  addr = data[currentLine].lstrip("@")
  if not addr.isdigit():
    addr = symbols[addr]
  return addr

def translateCInstruction():
  #Breaks line into dest, comp, jump
  command = data[currentLine]
  equal = command.find('=')
  semi = command.find(';')
  end = len(command)
  #If there's no jump
  if semi < 0:
    semi = end
  global destOut
  # For jump only commands with no dest
  if equal < 0:
    destOut = ""
  else:
    destOut = command[0:equal]
  global compOut
  compOut = command[equal+1:semi]
  global jumpOut
  jumpOut = command[semi+1:end]


def hasMoreCommands():
  #Checks if there are more commands
  if len(data) > currentLine:
    return True
  else:
    return False


def advance():
  #increments current line
  global currentLine
  currentLine += 1


def comp():
  global compOut
  return compOut

def dest():
  global destOut
  return destOut

def jump():
  global jumpOut
  return jumpOut
