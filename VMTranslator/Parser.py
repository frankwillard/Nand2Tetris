import codeWriter

global currentLine
currentLine = 0
arithmetic = ["add", "sub", "neg", "eq", "lt", "gt", "and", "or", "not"]

def Parser(newfile):
  #Opens and reads the file
  myfile = open(newfile, "r")
  global data
  data = myfile.readlines()
  myfile.close()
  removeComments()

#Removes \n from each line and all comments- filters to just commands
def removeComments():
  n = 0
  global data
  for i in range(len(data)):
    if "//" in data[n]:
      comment = data[n].find("//")
      if comment == 0:
        data[n] = ""
      else:
        data[n] = data[n][0:comment]
    if "\n" in data[n]:
      newline = data[n].find("\n")
      data[n] = data[n][:newline]
    if data[n] == "":
      data.remove(data[n])
      n-=1
    n+=1



def commandType():
  global data
  global arith
  global push
  global pop
  arith = False
  push = False
  pop = False
  global components
  components = data[currentLine].split(" ")
  if data[currentLine] in arithmetic:
    codeWriter.writeArithmetic()
  elif "push" in data[currentLine] or "pop" in data[currentLine]:
    codeWriter.writePushPop()

def hasMoreCommands():
  #Checks if there are more commands
  global data
  global currentLine
  if len(data) > currentLine:
    return True
  else:
    return False


def advance():
  #increments current line
  global currentLine
  currentLine += 1

def command():
  global comm
  global components
  comm = components[0]
  return comm

def arg1():
  global arg1Out
  global components
  arg1Out = components[1]
  return arg1Out

def arg2():
  global arg2Out
  global components
  arg2Out = components[2]
  return arg2Out
