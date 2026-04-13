#nacitas suradnice
#konrolujes pripad pomaly alebo rychlo rastucej usecky
#vpoctas predpis

import PIL
from PIL import Image


check = 10 
a = ''
b = ''
x = ''
y = ''

a1 = int(input("zadaj x suradnice bodu A: "))
a2 = int(input("zadaj x suradnice bodu B: "))

b1 = int(input("zadaj y suradnice bodu A: "))
b2 = int(input("zadaj y suradnice bodu B: "))

img = Image.new('RGB', (100, 100), color = 'white')
pic = img.load

(w,h) = img.size

if abs(a1-a2) > abs(b1-b2):
    print("usecka je pomala")
    check = check + 1
else:
    print("usecka je rychla")
    check = check - 1

def volna(a1, a2, b1, b2, check):
    if check > 10:
        a = (b2-b1)/(a2-a1)
        b = b1 - a*a1
        print("predpis je y = " + str(a) + "x + " + str(b))
    else:
        a = (a2-a1)/(b2-b1)
        b = a1 - a*b1
        a = int(round(a))
        b = int(round(b))
        print("predpis je x = " + str(a) + "y + " + str(b))
        return a, b

a,b = volna(a1, a2, b1, b2, check)
    
#kreslime jupiiiiiiiiiiiiiiiiiiiii
def pixaso(a, b, img, a1, b1, a2, b2):
    for x in range(a1,b1 ):
        print(x,',', end='')
        for y in range(a2, b2):
            print(y)
            if y == a*x+b: # and x*y == a-b:
               img.putpixel((x,y), (0,0,0,255))
               print("jakub volna")
 #           print(x, "kl", y, "hahdfsaugh", a*x+b, "pipk", (a-b)/(y+1) )
    return img

print(a,b)
pixaso(a, b, img, a1, b1, a2, b2)
img.show()
