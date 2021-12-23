import Parser
segments = {"SP": "R0", "LCL": "R1", "ARG": "R2", "THIS": "R3", "THAT": "R4", "TEMP": "R5"}
global vm
global boolCount
#Necessary for arithmetic boolean- need assembly functions and cant have overlap
boolCount = 0

def codeWriter(newfile):
  #Opens file
  global vm
  vm = open(newfile, "w")
  #Initially sets SP (unnecessary)
  initialize = "@256\nD=A\n@R0\nM=D\n"
  #@300\nD=A\n@R1\nM=D\n@400\nD=A\n@R2\nM=D\n@3000\nD=A\n@R2\nM=D\n@3010\nD=A\n@R2\nM=D\n
  vm.write(initialize)
  # change return in functions to write
  #vm.writelines(finalOut)

def writeArithmetic():
  global vm
  comm = Parser.command()
  if "add" in comm:
    mainArith("+")
  if "and" in comm:
    mainArith("&")
  if "or" in comm:
    mainArith("|")
  if "sub" in comm:
    mainArith("-")
  if "neg" in comm:
    neg()
  if "not" in comm:
    arithNot()
  if "eq" in comm:
    arithBool("JNE")
  if "lt" in comm:
    arithBool("JGE")
  if "gt" in comm:
    arithBool("JLE")


def writePushPop():
  #Index is just arg2- dont need to pass right
  command = Parser.command()
  arg1 = Parser.arg1()
  arg2 = Parser.arg2()
  if "push" in command:
    if "local" in arg1:
      multiPush("LCL", arg2)
    if "arg" in arg1:
      multiPush("ARG", arg2)
    if "this" in arg1:
      multiPush("THIS", arg2)
    if "that" in arg1:
      multiPush("THAT", arg2)
    if "temp" in arg1:
      multiPush("TEMP", str(int(arg2) + 5))
    if "constant" in arg1:
      pushConst(arg2)
    if "pointer" in arg1:
      pushStaticPointer("3", arg2)
    if "static" in arg1:
      pushStaticPointer("16", arg2)
  if "pop" in command:
    if "local" in arg1:
      multiPop("LCL", arg2)
    if "arg" in arg1:
      multiPop("ARG", arg2)
    if "this" in arg1:
      multiPop("THIS", arg2)
    if "that" in arg1:
      multiPop("THAT", arg2)
    if "temp" in arg1:
      multiPop("TEMP", str(int(arg2) + 5))
    if "pointer" in arg1:
      popStaticPointer("3", arg2)
    if "static" in arg1:
      popStaticPointer("16", arg2)


def multiPush(segment, index):
  #addr = LCL + i
  #*SP=*addr
  #SP++
  push = "@" + segments[segment] + "\nD=M\n@" + index + "\nA=D+A\nD=M\n@R0\nA=M\nM=D\n@R0\nM=M+1\n"
  global vm
  vm.write(push)

def multiPop(segment, index):
  #addr = LCL + i
  # SP--
  # *addr = *SP
  pop = "@" + index + "\nD=A\n@" + segments[segment] + "\nD=M+D\n@R13\nM=D\n@R0\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"
  global vm
  vm.write(pop)
'''
def popTemp(index):
  #addr = 5 + i
  #SP--
  #*addr=*SP
  pop = "@5\nD=A\n@" + index + "\nD=D+A\n@R13\nM=D\n@R0\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n"
  global vm
  vm.write(pop)
'''

def pushStaticPointer(segnum, index):
  #*SP=THIS/THAT
  #SP++
  push = "@" + segnum + "\nD=A\n@" + index + "\nA=D+A\nD=M\n@R0\nA=M\nM=D\n@R0\nM=M+1\n"
  global vm
  vm.write(push)

def popStaticPointer(segnum, index):
  #SP--
  #THIS/THAT=*SP
  pop = "@R0\nM=M-1\n@" + segnum + "\nD=A\n@" + index + "\nD=D+A\n@R13\nM=D\n@R0\nA=M\nD=M\n@R13\nA=M\nM=D\n"
  global vm
  vm.write(pop)

def pushConst(index):
  #*SP=i
  #SP++
  push = "@" + index + "\nD=A\n@R0\nA=M\nM=D\n@R0\nM=M+1\n"
  global vm
  vm.write(push)

def mainArith(symbol):
  arith = "@R0\nAM=M-1\nD=M\nA=A-1\nM=M"+ symbol + "D\n"
  global vm
  vm.write(arith)

def neg():
  arith = "D=0\n@R0\nA=M-1\nM=D-M\n"
  global vm
  vm.write(arith)
 
def arithNot():
  arith = "@R0\nA=M-1\nM=!M\n"
  global vm
  vm.write(arith)

def arithBool(jump):
  global boolCount
  count = str(boolCount)
  arith =  "@R0\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@FALSE" + count +"\nD;" + jump + "\n@R0\nA=M-1\nM=-1\n@NEXT" + count + "\n0;JMP\n(FALSE" + count + ")\n@R0\nA=M-1\nM=0\n(NEXT" + count + ")\n"
  global vm
  vm.write(arith)
  boolCount+=1