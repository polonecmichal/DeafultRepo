import tkinter as tk
win = tk.Tk()
win.title('moj syn Wolfgang')
canvas = tk.Canvas(win, width = 400, height = 400, bg = 'white')
canvas.pack()
#tvorba sektorov
canvas.create_line(200, 0,200,400)
canvas.create_line(0, 200,400,200)
#sektor 1
a = 0
b = 0
for a in range (0,200,20):
    canvas.create_line(a, 0,200,200)    
    a += 20
for b in range (0,200,20):
    canvas.create_line(b, 0,0,200)
    b += 20
#sektor 2
for x in range(0, 200,20):
    for y in range(200,400,20):
        canvas.create_rectangle(0,200,x+20,y+20)
for x in range(0, 200,20):
    for y in range(200,400,20):
        canvas.create_rectangle(x,y,x+20,y+20, fill = 'red')
        if (x//20 + y//20) % 2 == 0:
            canvas.create_rectangle(x,y,x+20,y+20, fill = 'blue')
#sektor 3
for x in range(200,400,20):
    for y in range(200,400,20):
        canvas.create_rectangle(x,y,x+20,y+20)
#sektor 4
    canvas.create_oval(200,0,400,200)
    canvas.create_oval(220,20,380,180)
win.mainloop()

