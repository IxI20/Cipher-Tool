import string,os,shutil
"""a = alphabet, string holding all characters to use in operations
   k = key, used in cipher operations
   e = encode, boolean value to determine if value should be encoded or decoded
   i_txt = input string
   o_txt = output string
   """
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"
MENU_COL = "\033[1;37;44m" 

def align_text(i_txt):
    t_width=shutil.get_terminal_size().columns
    return f"{i_txt:^{t_width}}"

def invalid_input(referer,msg="Invalid input, press enter to retry",*args,**kwargs):
    input(align_text(RED+align_text(msg)+RESET))
    return referer(*args,**kwargs)

def title(i_txt):
    bar="="*shutil.get_terminal_size().columns
    print(MENU_COL+align_text(bar))
    print(align_text(i_txt))
    print(align_text(bar)+RESET+"\n")

def wrap_output(i_txt,strip=" "):
    t_width=shutil.get_terminal_size().columns
    if len(i_txt) > t_width: i_txt=i_txt.replace(strip,"\n")
    i_txt=i_txt.replace("_"," ")
    return align_text(i_txt)

def alphabet_builder(a):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        title(i_txt="Alphabet Builder")
        print(f"\n{align_text(a)}\n")
        print(align_text("Add each portion of alphabet in order"))
        print(wrap_output(i_txt="1.Space 2.Lower_case 3.Upper_case 4.Special_characters 5.Reset_alphabet 6.Finish"))
        match input("Select : "):
            case "1":
                if " " in a: invalid_input(a=a,referer=alphabet_builder,msg="Space already in alphabet, press enter to retry")
                else: a += " "
            case "2":
                if string.ascii_lowercase in a: invalid_input(a=a,referer=alphabet_builder,msg="Lowercase already in alphabet, press enter to retry")
                else: a += string.ascii_lowercase
            case "3":
                if string.ascii_uppercase in a: invalid_input(a=a,referer=alphabet_builder,msg="Uppercase already in alphabet, press enter to retry")
                else: a += string.ascii_uppercase
            case "4":
                if string.punctuation in a: invalid_input(a=a,referer=alphabet_builder,msg="Special characters already in alphabet, press enter to retry")
                else: a += string.punctuation
            case "5":
                a =""
            case "6":
                menu(a=a)
            case _:
                invalid_input(a=a,referer=alphabet_builder)

def rot_cipher(a,k,e=False,i_txt=""):
    o_txt = ""
    for i in i_txt:
        if i not in a: o_txt += i
        else: 
            if e: o_txt += a[(a.find(i)+k) % len(a)]
            else: o_txt += a[(a.find(i)-k) % len(a)]
    o_txt = o_txt.replace(" ","_")
    return o_txt

def vig_cipher(a,k,e,i_txt):
    o_txt = ""
    key_length = len(k)
    for i in range(len(i_txt)):
        char = i_txt[i]
        if char not in a: o_txt += char
        char_index = a.find(char)
        key_value = a.find(k[i % key_length]) 
        if e: new_index = (char_index + key_value) % len(a)
        else: new_index = (char_index - key_value) % len(a)
        o_txt += a[new_index]
    return o_txt

def xor_cipher(k,e,i_txt): # input for decode is unicode / output for encode is unicode
    o_txt = ""
    if e:
        for i,c in enumerate(i_txt): # goes through each character in string holding index(i) & character(c) 
            char=ord(c) # returns unicode value representing character
            index = i%len(k)  # cyclic index, wraps around if i is greater than len(key(k))
            choosen_key = ord(k[index]) # key character choosen based on index and converted to unicode value representing character
            o_txt += f"{char ^ choosen_key} " 
    else: 
        split_i=i_txt.split(" ")
        for i,d in enumerate(split_i):
            char = int(d)
            index = i % len(k)
            choosen_key = ord(k[index])
            o_txt += chr(char^choosen_key) 
    return o_txt

def code_dialogue(c,e,a=""):

    if c == "1": 
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            if e: title(i_txt="ROT Cipher Encoder")
            else: title(i_txt="ROT Cipher Decoder")
            try:
                k = int(input(align_text("Key value")+"\n"))
                if e: i_txt = input(align_text("Clear text")+"\n")
                else: i_txt = input(align_text("Cipher text")+"\n")
                o_txt = rot_cipher(a=a,k=k,e=e,i_txt=i_txt)
                break
            except ValueError: invalid_input(c=c,e=e,a=a,referer=code_dialogue,msg="Key must be an integer, press enter to retry")

    elif c=="2": #key must be in alphabet
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            if e: title(i_txt="Vigenere cipher Encoder")
            else: title(i_txt="Vigenere cipher Decoder")
            try:
                k = str(input(align_text("Key")+"\n"))
                if e: i_txt = input(align_text("Clear text")+"\n")
                else: i_txt = input(align_text("Cipher text")+"\n")
                o_txt = vig_cipher(a=a,k=k,e=e,i_txt=i_txt)
                break
            except ValueError: invalid_input(c=c,e=e,a=a,referer=code_dialogue,msg="Key must be an string, press enter to retry")

    elif c=="3":
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            if e: title(i_txt="XOR Cipher Encoder")
            else: title(i_txt="XOR Cipher Decoder")
            try:
                k = input(align_text("key")+"\n")
                if e: i_txt = input(align_text("Clear text")+"\n")
                else: 
                    i_txt = input(align_text("Cipher text")+"\n")
                    if set(string.ascii_letters+string.punctuation) & set(i_txt): raise ValueError 
                o_txt = xor_cipher(k=k,e=e,i_txt=i_txt)
                break
            except ValueError: invalid_input(c=c,e=e,a=a,referer=code_dialogue,msg="cipher must be space seperated unicodes, press enter to retry")

    if e: print("\n\n"+wrap_output(i_txt=f"Clear_text_:_{i_txt}    Cipher_text_:_{o_txt}",strip="    ")+"\n\n")
    else: print("\n\n"+wrap_output(f"Cipher_text_:_{i_txt}    Clear text : {o_txt}",strip="    ")+"\n\n")
    
    input(GREEN+align_text("Operation Completed, press enter to return")+RESET)
    menu()
    
def code_menu(a,e):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        if e: title(i_txt="Encoder Menu")
        else: title(i_txt="Decoder Menu")
        print(wrap_output(i_txt="1.ROT_cipher 2.Vigenere_cipher 3.XOR_cipher 4.Exit")+"\n") # doesnt align because it's one string
        c = input("Select : ")
        match c:
            case "1":
                code_dialogue(c=c,e=e,a=a)
            case "2":
                code_dialogue(c=c,e=e,a=a)
            case "3":
                code_dialogue(c=c,e=e)
            case "4":
                menu()
            case _:
                invalid_input(referer=code_menu,a=a,e=e)

def menu(a=string.ascii_letters):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        title(i_txt="Cipher Tool")
        print(wrap_output(i_txt="1.Encode 2.Decode 3.Modify_alphabet 4.Quit")+"\n")
        match input("Select : "):
            case "1":
                e=True
                code_menu(a=a,e=e)
            case "2":
                e=False
                code_menu(a=a,e=e)
            case "3":
                alphabet_builder(a=a)
            case "4":
                print(f"\n{GREEN}"+align_text("Thank you for using Cipher Tool!")+f"\n{GREEN}")
                exit(0)
            case _:
                invalid_input(referer=menu)

menu()
