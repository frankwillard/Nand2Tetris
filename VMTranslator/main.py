#Frankie Willard
# Period 5

import Parser
import codeWriter

def main():
  #Takes in filename
  newfile = input("Which vm file do you want me to read (don't include .vm)? ")
  #Opens and reads file
  Parser.Parser(newfile + ".vm")
  codeWriter.codeWriter(newfile + ".asm")
  #While more commands, determine if A or C and add to finalOut array
  while Parser.hasMoreCommands():
    Parser.commandType()
    Parser.advance()
  codeWriter.vm.close()
  #Writes to hack file

main()