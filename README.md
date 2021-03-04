# melody-translation
Tools used for extracting Japanese scripts and reinserting the translation into Melody's 1996 game "Darkness."

Included files
[sjis.tbl] (required) This file is used during extraction. I couldn't find a clean SJIS->UTF-8 conversion due to the fact that the kanji order isn't the same, so instead a calculation is done on the kanji hex values used in the game to convert them over to the SJIS hex values. This is used as the key in a dictionary lookup to find the associated kanji.
[ascii.tbl] (required) This file is used during text insertion. The hex values used in this game are 1) not the same as normal ASCII and 2) are in reverse order. The ASCII letters are used as the keys in a dictionary lookup to find the associated hex value to insert into the game's data.
