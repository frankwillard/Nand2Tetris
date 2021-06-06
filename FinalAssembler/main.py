'''
Frankie Willard
Elements of Computer Systems
Mr. Estep Pd 5
'''
import code
import Parser
# import time

# start = time.time()

def main():
  #Takes in filename
  newfile = input("Which asm file do you want me to read (don't include .asm)? ")
  #Opens and reads file
  Parser.Parser(newfile + ".asm")
  #Removes whitespace/fixes labels
  firstPass()
  #Fixes variables
  secondPass()
  global finalOut
  finalOut = []
  #While more commands, determine if A or C and add to finalOut array
  while Parser.hasMoreCommands():
    Parser.categorize()
    if Parser.A:
      global binnum
      binnum = str(code.AInstruction())
      addA()
    else:
      global comp
      comp = str(code.comp())
      global dest
      dest = str(code.dest())
      global jump
      jump = str(code.jump())
      addC()
    Parser.advance()
  #Writes to hack file
  hack = open(newfile + ".hack", "w")
  hack.writelines(finalOut)


def addA():
  global finalOut
  finalOut.append("0" + binnum + "\n")
  #return "0" + binnum

def addC():
  global comp
  global dest
  global jump
  global finalOut
  finalOut.append("111" + comp + dest + jump + "\n")
  #return "111" + comp + dest + jump #C instruction

def firstPass():
  Parser.removeWhiteSpace()
  Parser.fixLabels()

def secondPass():
  Parser.fixVariables()

#Runs program with mult file
main()

# elapsed = (time.time() - start)
# print ("Assembled in %s seconds" % (elapsed))