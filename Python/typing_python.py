import sys
import getch
import math
import shutil
import random
import time
import copy


with open("program") as f:
    line = f.readlines()

lines = []
for v in line:
    lines.append(v.strip("\n"))

g_term_size = shutil.get_terminal_size()
g_term_lines= g_term_size.lines

g_sentence = lines[random.randint(0,len(lines))]
g_nnn = 80
g_counter = 0
g_sumlen = 0
g_sumtype = -1
g_ch = ""
g_change = {"!":"1",'"':"2","#":"3","$":"4","%":"5","&":"6","'":"7","(":"8",")":"9","=":"-","~":"^","`":"@","{":"[","+":";","*":":","}":"]","<":",",">":".","?":"/","\\":"_","Q":"q","W":"w","E":"e","R":"r","T":"t","Y":"y","U":"u","I":"i","O":"o","P":"p","A":"a","S":"s","D":"d","F":"f","G":"g","H":"h","J":"j","K":"k","L":"l","Z":"z","X":"x","C":"c","V":"v","B":"b","N":"n","M":"m"}
g_have_typed = { "1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0,"0":0,"-":0,"^":0,"|":0,"q":0,"w":0,"e":0,"r":0,"t":0,"y":0,"u":0,"i":0,"o":0,"p":0,"@":0,"[":0,"a":0,"s":0,"d":0,"f":0,"g":0,"h":0,"j":0,"k":0,"l":0,";":0,":":0,"]":0,"z":0,"x":0,"c":0,"v":0,"b":0,"n":0,"m":0,",":0,".":0,"/":0,"_":0}

''' ---- TEST comprehension ----
g_nonshift = ("1","2","3","4","5","6","7","8","9","0","-","^","|","q","w","e","r","t","y","u","i","o","p","@","[","a","s","d","f","g","h","j","k","l",";",":","]","z","x","c","v","b","n","m",",",".","/","_" )
g_shift = ("!",'"',"#","$","%","&","'","(",")","0","=","~","no","Q","W","E","R","T","Y","U","I","O","P","`","{","A","S","D","F","G","H","J","K","L","+","*","}","Z","X","C","V","B","N","M","<",">","?","no")
g_have_typed2 = {key:value for key, value in zip(g_shift, g_nonshift) if key != "no"}
'''

g_should_typed = copy.copy(g_have_typed)
g_total_ch = copy.copy(g_have_typed)
g_key_to_missed = {}
for k in g_have_typed:
    g_key_to_missed[k] = {}


def Drow(l_len_l):
    l_len_g = len(g_sentence)
    l_diff = l_len_g - l_len_l
    l_space_l = math.floor((g_nnn - l_len_g)/2)
    l_space_r = math.ceil((g_nnn - l_len_g)/2)

    drow = [" {} ".format("-"*g_nnn),
            "|{}|".format(" "*g_nnn),
            "|{}|".format(" "*g_nnn),
            "|{}{}{}{}|".format(" "*l_space_l, " "*l_len_l, g_sentence[l_len_l:], " "*l_space_r),
            "|{}{}^{}{}|".format(" "*l_space_l, g_sentence[:l_len_l], " "*(l_diff-1), " "*l_space_r),
            "|{}|".format(" "*g_nnn),
            " {} ".format("-"*g_nnn)]
    scroll = "\n"*(g_term_lines - 8 - 1)

    for v in drow:
        print(v)

    print(scroll)

def Result_Key(res, l_file):
    result = [
            " ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----",
            "| HZ | 1! | 2\" | 3$ | 4$ | 5% | 6& | 7\' | 8( | 9) | 0  | -= | ^~ | \\| | BK |",
            "|    |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |    |".format(res["1"],res["2"],res["3"],res["4"],res["5"],res["6"],res["7"],res["8"],res["9"],res["0"],res["-"],res["^"],res["|"]),
            " ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----",
            " ------ ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- -------",
            "| Tab  | Q  | W  | E  | R  | T  | Y  | U  | I  | O  | P  | @` | [{ | Enter |",
            "|      |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |       |".format(res["q"],res["w"],res["e"],res["r"],res["t"],res["y"],res["u"],res["i"],res["o"],res["p"],res["@"],res["["],),
            " ------ ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----|_      |",
            " ------- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----|      |",
            "| Caps  | A  | S  | D  | F  | G  | H  | J  | K  | L  | ;+ | :* | ]} |      |",
            "|       |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |      |".format(res["a"],res["s"],res["d"],res["f"],res["g"],res["h"],res["j"],res["k"],res["l"],res[";"],res[":"],res["]"],),
            " ------- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ------",
            " --------- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---------",
            "| Shift   | Z  | X  | C  | V  | B  | N  | M  | ,< | .> | /? | \\_ | Shift   |",
            "|         |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |{:3} |         |".format(res["z"],res["x"],res["c"],res["v"],res["b"],res["n"],res["m"],res[","],res["."],res["/"],res["_"],),
            " --------- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---------"
            ]

    for v in result:
        l_file.write("{}\n".format(v))

def Result_Sorted(l_dict, l_file):
    l_kvchange = {}
    for k,v in l_dict.items():
        if v in l_kvchange:
            l_kvchange[v].append(k)
        else:
            l_kvchange[v] = [k]
    l_sorted_key = sorted(l_kvchange, reverse=True)
    for v in l_sorted_key:
        l_file.write("{:3} : ".format(int(v)))
        for vv in l_kvchange[v]:
            l_file.write("{} ".format(vv))
        l_file.write("\n")
    l_file.write("\n")

start = int(time.time())
while g_ch != "\n":
    Drow(g_counter)
    g_ch = getch.getch()
    g_sumtype += 1
    if not g_ch == "\n":
        if g_sentence[g_counter] == g_ch:
            g_counter += 1
            g_sumlen += 1
            if g_ch != " ":
                if g_ch in g_change:
                    g_total_ch[g_change[g_ch]] += 1
                else:
                    g_total_ch[g_ch] += 1

        else:
            if g_ch != " " and g_sentence[g_counter] != " ":
                if g_sentence[g_counter] in g_change:
                    g_should_typed[g_change[g_sentence[g_counter]]] += 1
                else:
                    g_should_typed[g_sentence[g_counter]] += 1

                if g_ch in g_change:
                    g_have_typed[g_change[g_ch]] += 1

                    if g_sentence[g_counter] in g_change:
                        if g_ch in g_key_to_missed[g_change[g_sentence[g_counter]]]:
                            g_key_to_missed[g_change[g_sentence[g_counter]]][g_change[g_ch]] += 1
                        else:
                            g_key_to_missed[g_change[g_sentence[g_counter]]][g_change[g_ch]] = 1
                    else:
                        if g_ch in g_key_to_missed[g_sentence[g_counter]]:
                            g_key_to_missed[g_sentence[g_counter]][g_change[g_ch]] += 1
                        else:
                            g_key_to_missed[g_sentence[g_counter]][g_change[g_ch]] = 1
                else:
                    g_have_typed[g_ch] += 1

                    if g_sentence[g_counter] in g_change:
                        if g_ch in g_key_to_missed[g_change[g_sentence[g_counter]]]:
                            g_key_to_missed[g_change[g_sentence[g_counter]]][g_ch] += 1
                        else:
                            g_key_to_missed[g_change[g_sentence[g_counter]]][g_ch] = 1
                    else:
                        if g_ch in g_key_to_missed[g_sentence[g_counter]]:
                            g_key_to_missed[g_sentence[g_counter]][g_ch] += 1
                        else:
                            g_key_to_missed[g_sentence[g_counter]][g_ch] = 1

        if g_counter == len(g_sentence):
            g_sentence = lines[random.randint(0,len(lines))]
            g_counter = 0

end = int(time.time())
g_total_time = end - start
g_type_accurate = g_sumlen / g_total_time
g_correct_rate = g_sumlen / g_sumtype

with open("result.log", "w") as f:
    f.write("<Result>\n")
    f.write(f'Total Time : {g_total_time} sec\n')
    f.write(f'Total length : {g_sumlen}\n')
    f.write(f'Total Types : {g_sumtype}\n')
    f.write(f'Typing per Sec : {g_type_accurate:2.2f}\n')
    f.write(f'Correct Rate : {g_correct_rate*100:3.2f}%\n')

    f.write("\n--- Total Word ---\n")
    Result_Sorted(g_total_ch, f)

    f.write("\n--- Words that should have be typed ---\n")
    Result_Sorted(g_should_typed, f)
    Result_Key(g_should_typed, f)

    f.write("\n--- Words that have be typed ---\n")
    Result_Sorted(g_have_typed, f)
    Result_Key(g_have_typed, f)

    f.write("\n--- Word's relation between SHOULD and HAVE ---\n")
    for k,v in g_key_to_missed.items():
        if v:
            f.write(" -- [{}] --\n".format(k))
            Result_Sorted(v, f)

    f.write("\n--- Errors(should be typed) per Types ---\n")
    for key in g_should_typed:
        if g_total_ch[key]:
            f.write(f' {key} : {(g_should_typed[key]/g_total_ch[key])*100:3.1f}\n')

    f.write("\n - Lower than AVG -\n")
    for key in g_should_typed:
        if g_total_ch[key]:
            l_lower = g_should_typed[key]/g_total_ch[key]
            if l_lower+g_correct_rate > 1.0:
                f.write(f' {key} : {l_lower*100:3.1f}\n')

