from tkinter import filedialog
from tkinter import *
import pass1
file = Tk()
programname = "test"
programLength = 205
label=Label(text="enter the sic code ")
b=Button(text="see the symbol table ")
file.title("sic assembler with literal") 
file.geometry('600x600')
scrollbar = Scrollbar(file)
scrollbar.pack( side = RIGHT, fill = Y )
mylist = Listbox(file, yscrollcommand = scrollbar.set )   
text1 = open('SYMTAB.txt').read()
prognam = Label(file ,text = "Program Name :" + programname, font='time 18 bold italic', fg='green')
prognam.pack()
programLength = Label(file ,text = " Program Langth :" + str(programLength) , font='time 18 bold italic ', fg='green')
programLength.pack()
tit = Label(file, text=" Symbol Table :", font='time 18 bold italic underline')
tit.pack()
symbol = Text(file, height=120, width=120 ,font='time 18 bold italic'  )
symbol.configure(background = "silver")
symbol.pack()                 
symbol.insert(END,text1)
file.mainloop()