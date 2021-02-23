#with open('test.txt', 'r') as fp:
#    hex_list = ["{:02x}".format(ord(c)) for c in fp.read()]
#print(hex_list)

import ast
import io
import codecs

#Variables
#Where to start in file
start_point = "0xA35254" #hex
#String Hex Values
begin_hex = start_point
end_hex = ""
hex_counter = start_point
#Dictionary
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
ctrlstr = 0
#Game to UTF offset (UTF8 あ = 12354, Game あ = 7d5f / 32095)
hiragana_start = 32095 #7d
hiragana_offset = 19741
katakana_start = 31934 #7c　ト 31896; 19408
katakana_offset = 19484
kanji_start = 29065 #SJIS
kanji_offset = -7405

start_offset = ""
offset = ""
conv_chr = ""
#The list of replacements

file = open('sjis.tbl', mode="r", encoding="shift-jis")

contents = file.read()
table = ast.literal_eval(contents)

file.close()

#Open file and start reading hex
#with open('EVE-text_top.PCK', 'r', encoding="utf-8_sig") as f:
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

    #Find beginning of control strings
    #FF CF FF = End of line
    #FF EF FF = Beginning of line
    #if ch_hex == "bd" and len(hexstr) == 0:
        #Hit a 15 byte control string
        #print("Control String")
        #ctrlstr = 15
        #ch_hex = ""
        #continue
    

    #print("Read a character:", ch_hex)
    #print(chr(int(ch_hex, 16)))
    
    hexstr = hexstr + ch_hex
    
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
          
        #print(hexstr)
        #print(int(hexstr, 16))
        #convert into UTF
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


        for sjis, kanji in table.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
          if sjis == hex(conv_chr)[2:6].upper():
            #print("Converted character: ", kanji)
            txtstr = txtstr + kanji

        
        hexstr = ""
    

