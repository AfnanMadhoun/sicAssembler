import codecs

<<<<<<< HEAD
from tkinter import filedialog
from tkinter import *
=======

>>>>>>> 94be05024ba0a29aa5aeeda9265f538566e42d55
    
intfile = open("acode.mdt","w+") #Open text file for write 
symFile = open("SYMTAB.txt","w+")
#litFile = open("Literal.txt","w+")


SYMTAB = {}
littab = {}
litpool = {}


dire = ["START", "BYTE", "RESB" , "WORD" , "RESW", "LTORG", "END"]

label = ""
op = ""
error = 0
<<<<<<< HEAD

#Store OBTAB.txt in opttab list 
opttab = {}
opfile = open("OPTAB.txt", "r")
for line in opfile:
    opttab[line[0:9].split(' ')[0]] = line[10:15].strip()

=======

#Store OBTAB.txt in opttab list 
opttab = {}
opfile = open("OPTAB.txt", "r")
for line in opfile:
    opttab[line[0:9].split(' ')[0]] = line[10:15].strip()

>>>>>>> 94be05024ba0a29aa5aeeda9265f538566e42d55
#ini. START address and program name
programname = ""
startaddress = 0
filename = open("sic.asm", "r") 
assembly = filename.readlines()
fline = assembly[0]         #Store first line 
if fline[9:15].strip() == "START":
    programname =  fline[0:8].strip()
    startaddress = int(fline[16:35].strip(),16)
    locCount = startaddress

    #Write first line to int. file 
    space = 10-len(str((locCount)))
    intfile.write(hex(locCount)[2:]+" "*space+fline)
    intfile.flush()

else:
    locCount = 0


for i, line in enumerate(assembly):
    op = line[9:15].strip()
    if(op!= "END" and op != "START"):
        
        if line[0] != '.':  
            if(op == "LTORG"): 
                intfile.write(" "*10+line)
            else :
                space = 10-len(str((locCount)))
                intfile.write(hex(locCount)[2:]+" "*space+line)
            
            label = line[0:8].strip()
            if label != "":
                if label in SYMTAB: #Check MULTIPLE DECLARATION error 
                    error = 1
                    print("There is MULTIPLE DECLARATION in the LABEL :"+" "+label)
                    break
                else: #If there is no MULTIPLE DECLARATION error 
                    SYMTAB[label] = hex(locCount)[2:]
<<<<<<< HEAD
                    symFile.write(SYMTAB[label]+" "*6)
=======
                    symFile.write(SYMTAB[label]+" "*10)
>>>>>>> 94be05024ba0a29aa5aeeda9265f538566e42d55
                    symFile.write(line[0:7].strip())
                    symFile.write("\n")
            #Chech it the opcode is in OBTAB 
            found = 0 
            if op in opttab:
                found = 1
                locCount += 3
            else:
                operand = 0

            if (found == 0 and op in dire):
                if op == "WORD":
                    locCount += 3
                elif op == "RESW":
                    operand = line[16:35].strip()
                    locCount += 3 * int(operand)
                elif op == "RESB":
                    operand = line[16:35].strip()
                    locCount += int(operand)
                elif op == "BYTE":
                    operand = line[16:35].strip()
                    if operand[0] == 'X':
                        locCount += int((len(operand)-3)/2)
                    elif operand[0] == 'C':
                        locCount += (len(operand)-3)

                #Literals pool 
                elif op == "LTORG":
                    for i in littab:
                        littab[i][2] = hex(locCount)[2:] 
                        space = 10-len(str((locCount)))
                        intfile.write(hex(locCount)[2:]+" "*space+"*"+" "*7+"="+i+"\n")
                        locCount += int(littab[i][1])
                    littab = {}
            #Check if there is literal
            literalList = []
            if line[16:17] == '=':
                exist = 1
                literal = line[17:35].strip()
                if literal[0]=='C':
                    hexco = literal[2:-1].encode("utf-8").hex()
                elif literal[0]== 'X':
                    hexco = literal[2:-1]
                else:
                    print("NOT Valid Literal : "+" "+line[16:35].strip())

                #Check if the literal is in literal table
                if literal in litpool:
                    exist = 0
                
                else:
                    literalList=[hexco,len(hexco)/2, 0]
                    littab[literal]= literalList
                    litpool[literal]= literalList
                    #Write on literal file
                    
                    
if op == "END":
    intfile.write(" "*10+line)

if littab:   #Repalce the literal pool 
    for i in littab:
        littab[i][2] = hex(locCount)[2:]
        space = 10-len(str((locCount)))
        intfile.write(hex(locCount)[2:]+" "*space+"*"+" "*7+"="+i+"\n")
        locCount += int(littab[i][1])
opfile.close()
intfile.close()
filename.close()


programLength = 0
lastaddress=locCount
programLength = int(lastaddress) - int(startaddress)
<<<<<<< HEAD
proglen = hex(int(programLength))[2:].format(int(programLength))
loc = hex(int(locCount))[2:].format(int(locCount))

# print("The symbol table is : ")
# print(SYMTAB)
# print('\n')

# print("The literal table is : ")
# print(litpool)
# print('\n')

# print("The program name is: ",programname)
# print("Location counter is : ",hex(int(locCount))[2:].format(int(locCount)))
# print("The program length is : ",proglen)
# print('\n')



######### gui part 

file = Tk()
file.title("sic assembler with literal") 
file.geometry('600x600')
text1 = open('SYMTAB.txt').read()
prognam = Label(file ,text = "Program Name :" + programname, font='time 18 bold italic', fg='green')
prognam.pack()
programLength = Label(file ,text = " Program Langth :" + str(proglen) , font='time 18 bold italic ', fg='green')
programLength.pack()
programLength = Label(file ,text = " Location Counter :" + str(loc) , font='time 18 bold italic ', fg='green')
programLength.pack()
tit = Label(file, text=" Symbol Table:", font='time 18 bold italic underline')
tit.pack()
symbol = Text(file, height=120, width=120 ,font='time 18 bold italic'  )
# symbol.configure(background = "silver")
symbol.insert(END,SYMTAB)
symbol.pack()

lit = Label(file, text=" Literal  :", font='time 18 bold italic underline')
lit.pack()
liter = Text(file, height=120, width=120 ,font='time 18 bold italic'  )
liter.insert(END,littab)
liter.pack()


file.mainloop()

=======

print('\n')

print("The program name is: ",programname)
print("Location counter is : ",hex(int(locCount))[2:].format(int(locCount)))
print("The program length is : ",hex(int(programLength))[2:].format(int(programLength)))
print('\n')

print("The symbol table is : ")
print(SYMTAB)
print('\n')

print("The literal table is : ")
print(litpool)
print('\n')
>>>>>>> 94be05024ba0a29aa5aeeda9265f538566e42d55


