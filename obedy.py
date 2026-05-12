import random
import math 
import tkinter as tk
import os

id = ''

win = tk.Tk()
win.title('vyberobedov')
canvas = tk.Canvas(win, width=800, height=800, bg='white')
g = canvas.create_rectangle(5,200,200,400, fill='green')
r = canvas.create_rectangle(205,200,400,400, fill='red')
b = canvas.create_rectangle(405,200,600,400, fill='blue')
o = canvas.create_rectangle(605,200,798,400, fill='orange')

if os.path.exists('objednavky.txt'):
    objednavky = open('objednavky.txt', 'w')
else:
    objednavky = open('objednavky.txt', 'x')

label = tk.Label(win, text='Zadaj kod studenta :', font=('Papyrus', 20))
label.pack()

id = tk.Entry(win, width=20)
id.insert(0, "")
id.pack()

def idgrab():
    if id.get() == '' or not id.get().isalpha():
        return ''
    print(id.get())
    return id.get()
canvas.pack()

def interakcia(event):
    global kod_student
    if idgrab() == '':
        return
    closest = canvas.find_closest(event.x, event.y)[0]
    if r == closest:
        kod_student = idgrab() + ' cervena'
    elif g == closest:
        kod_student = idgrab() + ' zelena'
    elif b == closest:
        kod_student = idgrab() + ' modra'
    elif o == closest:
        kod_student = idgrab() + ' oranzova'
    objednavky.write(kod_student + '\n')


canvas.bind('<Button-1>', interakcia)
canvas.mainloop()
objednavky.close()
win.mainloop()
