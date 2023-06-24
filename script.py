#
#  Generate a HTML file with all printable Unicode characters grouped by script
#
#  MIT (C) 2023 René Oudeweg
#

import unicodedata
import unicscript
import re, itertools, sys

all_chars = (chr(i) for i in range(sys.maxunicode))
categories = {'Cc'}
control_chars = ''.join(c for c in all_chars if unicodedata.category(c) in categories)
# or equivalently and much more efficiently
control_chars = ''.join(map(chr, itertools.chain(range(0x00,0x20), range(0x7f,0xa0))))
control_char_re = re.compile('[%s]' % re.escape(control_chars))

def remove_control_chars(s):
    return control_char_re.sub('', s)
    
def group_characters_by_script():
    character_groups = {}
    for codepoint in range(sys.maxunicode):
        char = chr(codepoint)
        script = unicscript.script_cat(char)
        if script not in character_groups:
            character_groups[script] = []
        character_groups[script].append(char)
    return character_groups

character_groups = group_characters_by_script()

# Creating an HTML file
Func = open("uniscripts.html","w") 

# Adding input data to the HTML file
Func.write("<html>\n<head>\n<title> \nUnicode Scripts \
           </title>\n</head> <body><h1>All printable Unicode characters</h1>")
              
# Print character groups
for script, characters in character_groups.items():
    print(f"Script: {script}")
    Func.write("Script: " + script[0] + "[" + script[1] + "]")
    s = "".join(characters)
    s = remove_control_chars(s)
    try: 
        print("Characters:" + s)
        Func.write("<br>"+ s+"<br><br>")
    except UnicodeEncodeError:
        Func.write("<br><br>")
        continue
    print()

Func.write("</body></html>")
# Saving the data into the HTML file
Func.close()


     
