##########
# Import #
##########

import ast
import io
import codecs

###############
#  Variables  #
###############

#Where to start writing in file
start_point = "0xA35254" #hex

# The list and string
hexList = []
EngTrans = "This is a test sentence. "

#ASCII lookup dictionary
table = {}

########
# Code #
########

#Load up ASCII conversion dictionary
file = open("ascii.tbl", mode="r", encoding="utf-8")
contents = file.read()
table = ast.literal_eval(contents)
file.close()

#BEGIN WRITING LOOP LOGIC
#Step 1: Read file line by line
#Step 2: Split hex writing location from string using pipe (done in XL)
#Step 3: Assign hex addr and string to associated variables
#Step 4: Translate string into hex list
#Step 5: Seek write location in file and write hex string
#Step 6: Repeat until EOF


#STEP 4: Translate string into hex values
for chr in EngTrans:
  hexList.append(table[chr])

print(hexList)

#STEP 5: Write Hex Values
#with open('test.txt', 'r+b') as f:
#  for i in hexList:
#    f.write(bytes((int(i,16),)))
