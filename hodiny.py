import datetime as dt
import math 
import tkinter as tk


win = tk.Tk()
win.title('hodiny')
s1 = 400
s2 = 400
kratka_ruc = 75
dlha_ruc = 150
polomer_hodin = dlha_ruc + 25
polomer_cisla = dlha_ruc + 5
hrubka_h = 3
hrubka_m = 1
hrubka_s = 0.5

canvas = tk.Canvas(win, width=800, height=800, bg='white')
canvas.pack() 
canvas.create_oval(s1 - polomer_hodin, s2 - polomer_hodin, s1 + polomer_hodin, s2 + polomer_hodin, outline='black', width=2, fill = 'indianred')
line1 = canvas.create_line(0,0,1,1, fill='black', width=hrubka_m)
line2 = canvas.create_line(0,0,1,1, fill='medium spring green', width=hrubka_s)
line3 = canvas.create_line(0,0,1,1, fill='black', width=hrubka_h)



def draw():
    for i in range(12):
        uhol = math.radians(i * 30 - 90)
        x = s1 + polomer_cisla * math.cos(uhol)
        y = s2 + polomer_cisla * math.sin(uhol)
        canvas.create_text(x, y, text=str(i if i != 0 else 12), font=('Comic sans MS', 15, 'bold'))
    rucicky()

def rucicky():
    cas = dt.datetime.now()
    uhol_minuta = math.radians(cas.minute * 6 - 90)
    uhol_sekunda = math.radians(cas.second * 6 - 90)
    uhol_hodina = math.radians((cas.hour * 30 + cas.minute * 0.5) - 90)
    canvas.coords(line1, s1, s2, s1 + dlha_ruc * math.cos(uhol_minuta), s2 + dlha_ruc * math.sin(uhol_minuta))
    canvas.coords(line2, s1, s2, s1 + dlha_ruc * math.cos(uhol_sekunda), s2 + dlha_ruc * math.sin(uhol_sekunda))
    canvas.coords(line3, s1, s2, s1 + kratka_ruc * math.cos(uhol_hodina), s2 + kratka_ruc * math.sin(uhol_hodina))
    update()
    

def update():
    canvas.after(1000, rucicky)


draw()
win.mainloop()