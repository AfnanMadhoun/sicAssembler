import codecs

#open file to read it
filename = open("sic.asm", "r")

#open file to read it
opfile = open("OPTAB.txt", "r")

#read  all input lines
assembly = filename.readlines()

#read opcode table 
optab = opfile.readlines()


#initialize symbol table, program name, program length and locctr
SYMTAB = {}
opttab = {}
littab = {}
litpool = {}

intfile = open("acode.mdt","w+")

#initialize a list of directives
directives = ["START", "END", "BYTE", "WORD", "RESB", "RESW", "BASE", "LTORG"]

#initialize instruction component
label = ""
op = ""
# comment = ""
# counter = 0


#create a .text files  
errorf = 0



#store opcode table in 2D list
for i, line in enumerate(optab):
    #read file from third line 
    if i>1:
        opttab[line[0:11].split(' ')[0]] = line[15:18].strip()

programname = ""
startaddress = 0
#read first input line

fline = assembly[0]
if fline[9:15].strip() == "START":
    programname =  fline[0:8].strip()
    startaddress = int(fline[16:35].strip(),16)
    locCount = startaddress

    #to save a fixed format in intermediate file 
    blanks = 6-len(str((locCount)))

    intfile.write(hex(locCount)[2:]+" "*blanks+fline)    #write line to intemediate file

    
else:
    locCount = 0


for i, line in enumerate(assembly):
    #read opcode
    op = line[9:15].strip()
    if op!= "END" and op != "START" and op != "BASE":

        #if this is not a comment line
        if line[0] != '.':
            #write line to intemediate file
            #check if that line is LTORG
            if(op == "LTORG"):
                intfile.write(" "*6+line)
            else :
                #to save a fixed format in intermediate file
                blanks = 6-len(str((locCount)))
                intfile.write(hex(locCount)[2:]+" "*blanks+line)
            
            #read label field
            label = line[0:8].strip()
            #if there is asymbol in label field
            if label != "":
                #serch SYMTAB for LABEL
                #if found
                if label in SYMTAB:
                    #set error flag
                    errorf = 1
                    print("MULTIPLE DECLARATION TO THE LABEL")
                    break
                #else insert [label, LOCCTR] into SYMTAB
                else:
                    SYMTAB[label] = hex(locCount)[2:]

            #found is a boolean to  determine if opcode exist in opcode table
            found = 0

            #search OPTAB for OPCODE
            #if found
            if op in opttab:
                found = 1
                #add 3 {instruction length} to LOCCTR
                locCount += 3
            #if not found
            operand = 0

            if found == 0 and op in directives:
                if op == "WORD":
                    #add 3 {instruction length}
                    locCount += 3
                elif op == "RESW":
                    operand = line[16:35].strip()
                    locCount += 3 * int(operand)
                elif op == "RESB":
                    operand = line[16:35].strip()
                    locCount += int(operand)
                elif op == "BYTE":
                    operand = line[16:35].strip()
                    #find the length of constant in bytes and add it to locCount
                    if operand[0] == 'X':
                        locCount += int((len(operand) - 3)/2)
                    elif operand[0] == 'C':
                        locCount += (len(operand) - 3)
                #place literals into a pool at some location in object program
                elif op == "LTORG":
                    for k in littab:
                        littab[k][2] = hex(locCount)[2:] 
                        blanks = 6-len(str((locCount)))
                        intfile.write(hex(locCount)[2:]+" "*blanks+"*"+" "*7+"="+k+"\n")
                        locCount += int(littab[k][1])
                    littab = {}
                    
            #check if line contain literal
            if line[16:17] == '=':
                literalList = []
                ifisExist = 1
                literal = line[17:35].strip()
                if literal[0]=='C':
                    hexCode = literal[2:-1].encode("utf-8").hex()
                elif literal[0]== 'X':
                    hexCode = literal[2:-1]
                else:
                    #set error flag
                    print("this is no valid literal ")
                #find literal in table literal

                if literal in litpool:
                    ifisExist = 0
                
                #if literal not exist in literal tabel 
                if ifisExist:
                    literalList=[hexCode,len(hexCode)/2, 0]
                    littab[literal]= literalList
                    litpool[literal]= literalList

if op == "END":
    intfile.write(" "*6+line)

#place literals into apool at the end of prog
if littab:
    for k in littab:
        littab[k][2] = hex(locCount)[2:]
        blanks = 6-len(str((locCount)))
        intfile.write(hex(locCount)[2:]+" "*blanks+"*"+" "*7+"="+k+"\n")
        locCount += int(littab[k][1])

#save (locCount - starting add ) as program length
programLength = 0
lastaddress=locCount
programLength = int(lastaddress) - int(startaddress)
#close file
filename.close()
opfile.close()
intfile.close()
print("The program name: ",programname)
print('\n'," ")
print("The program length is : ",hex(int(programLength))[2:].format(int(programLength)))
print('\n'," ")
print("Location counter : ",hex(int(locCount))[2:].format(int(locCount)))
print('\n'," ")

print("the symbol table is : ")
print(SYMTAB)
print('\n'," ")
print("the litral table is : ")
print(litpool)
