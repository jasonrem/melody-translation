##########
# Import #
##########

import ast

###############
#  Variables  #
###############

#Where to start reading in the file
start_point = "0xA35254" #hex

#String Hex Values
begin_hex = start_point #The hex address of where a string begins
end_hex = "" #The hex address of where a string ends
hex_counter = start_point #Incrementing counter

#SJIS dictionary
table = {}

#Starting and Ending Point for Reading
start_index = 0
end_index = 1

#Initial character read where processing occurs
ch_hex = ""

#Hex String
hexstr = ""

#Text String
txtstr = ""

#Control String counter
ctrlstr = 0 # no longer used?

#Game hex values to UTF offsets (UTF8 あ = 12354, Game あ = 7d5f / 32095)
hiragana_start = 32095 #7d
hiragana_offset = 19741

katakana_start = 31934 #7c　ト 31896; 19408
katakana_offset = 19484

kanji_start = 29065 #SJIS
kanji_offset = -7405

start_offset = ""
offset = ""
conv_chr = ""

########
# Code #
########

#The list of SJIS kanji replacements

file = open('sjis.tbl', mode="r", encoding="shift-jis")

contents = file.read()
table = ast.literal_eval(contents)

file.close()

#Open file and start reading hex
with open('EVE.PCK', 'rb') as f:
  seek_offset = int(start_point, 16)
  f.seek(seek_offset)

  while True:
    #Begin reading file
    c = f.read(1)
    hex_counter = hex((int(hex_counter, 16) + 1)) #Increment hex
    #If end of file
    if not c:
      print("End of file")
      print(hexstr)
      break

    # If we're in a control string, just skip ahead
    if ctrlstr > 0:
      ctrlstr= ctrlstr-1
      continue

    #Begin processing read character
    ch_hex = "{:02x}".format(ord(c))
    
    hexstr = hexstr + ch_hex

    #If we're in a control string, just loop until it breaks to the next line of dialogue
    #NEEDS REWORKING; lines are missed
    if len(hexstr) >= 4:
        if hexstr[:4] == "ffcf":
          if end_hex == "": end_hex = hex((int(hex_counter, 16) - 3))          
          if hexstr[-4:] == "efff":
            with open('script_export.txt','a', encoding='utf-8') as scriptdump:
              scriptdump.write(begin_hex + ",")
              scriptdump.write(end_hex + ",")
              scriptdump.write(txtstr)
              scriptdump.write("\n")
              scriptdump.flush()
              scriptdump.close()
            print(begin_hex)
            print(end_hex)
            print(txtstr)
            txtstr = ""
            hexstr = ""
            begin_hex = hex_counter
            end_hex = ""
            continue
          else:
            continue
          
        #Convert into UTF
          
        #Determine character set
        if hexstr[:2] == "7d": # hiragana
          if int(hexstr, 16) <= hiragana_start:
            offset = hiragana_offset
            start_offset = hiragana_start
          else: # To address alphanumerics
            start_offset = 32176 #7db0 = 0 full width
            offset = -33120 #FF10 = 0 full width
          conv_chr = int(hexstr, 16) - (offset - ((start_offset  - int(hexstr, 16)) * 2))
          #print("Converted character: ", chr(int(conv_chr)))
          txtstr = txtstr + chr(int(conv_chr))
        elif hexstr[:2] == "7c": # katakana
          #ラ行 advancing by one, ン rendering as ヴ
          if int(hexstr, 16) >= 31872: #7c80 is skipped
            offset = katakana_offset
          else: # To fix ム and beyond skip ahead one
            offset = katakana_offset + 1
          start_offset = katakana_start
          conv_chr = int(hexstr, 16) - (offset - ((start_offset  - int(hexstr, 16)) * 2))
          #print("Converted character: ", chr(int(conv_chr)))
          txtstr = txtstr + chr(int(conv_chr))
        else: # SJIS kanji
          start_offset = kanji_start
          offset = kanji_offset
          conv_chr = int(hexstr, 16) - (offset - ((start_offset  - int(hexstr, 16)) * 2))

        #When character is a kanji
        for sjis, kanji in table.items():
          if sjis == hex(conv_chr)[2:6].upper():
            txtstr = txtstr + kanji

        
        hexstr = ""
