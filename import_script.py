##########
# Import #
##########

import ast

###############
#  Variables  #
###############

#Where to start writing in file
write_point = "" #hex; ex. 0xA35254

# The list and string
hexList = [] 
EngTrans = "" 

#ASCII lookup dictionary
table = {}

########
# Code #
########

#Load up ASCII conversion dictionary
fileASCII = open("ascii.tbl", mode="r", encoding="utf-8")
contents = fileASCII.read()
table = ast.literal_eval(contents)
fileASCII.close()

# Read file of translation strings.
fileText = open("textstrings.txt", mode="r", encoding="utf-8")
for line in fileText:
  # Split hex write address and text, assign to variables
  line = line.replace("\n", "")
  write_point, EngTrans = line.split("|")

  # Translate string into hex values
  for chr in EngTrans: 
    hexList.append(table[chr])

  # Write Hex Values
  with open('EVE.PCK', 'r+b') as fileWrite:
    fileWrite.seek(int(write_point, 16))
    for i in hexList:
      fileWrite.write(bytes((int(i,16),)))
  hexList.clear()
  
fileWrite.close()
fileText.close()
print("Translation Inserted")
