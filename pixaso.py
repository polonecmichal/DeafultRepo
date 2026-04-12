import PIL
from PIL import Image

def forpremium(x, pixels,Ay,By,image):
    for y in range(Ay,By):
        pixels[x,y] = (0,0,0)
    image.show()
    exit(0)

def zadanie():
    Ax = int(input('zadaj x bodu A:'))
    Ay = int(input('zadaj y bodu A:'))
    Bx = int(input('zadaj x bodu B:'))
    By = int(input('zadaj y bodu b:'))
    return(Ax,Ay,Bx,By)

def volna(Ax, Bx, Ay, By, pixels, image):
    if Ay == By:
        return 0, Ay
    if Ax == Bx:
    # potrebuem iny for loop
        forpremium(Ax, pixels,Ay,By,image)

    if abs(Ax-Bx) > abs (Ay-By):
        check = 1
    else:
        check = 0
    if check == 1:
        a = (By-Ay)/(Bx-Ax)
        b = Ay - a*Ax
        a = int(round(a))
        b = int(round(b))
        print("predpis je y = " + str(a) + "x + " + str(b))
    else:
        a = (Bx-Ax)/(By-Ay)
        b = Ax - a*Ay
        a = int(round(a))
        b = int(round(b))
        print("predpis je x = " + str(a) + "y + " + str(b))
        return a, b

def main():
    #nacitam si obrazok
    image = PIL.Image.new("RGB",(200,200),"white")
    pixels = image.load()
    #zadame udaje bodov
    (Ax,Ay,Bx,By) = zadanie()
    print(Ax,Ay,Bx,By)
    predpisA, predpisB = volna(Ax, Bx, Ay, By, pixels, image)
    #kreslenie jupiiiiiiiiii
    if By >= 200:
        By = 199 
    if Bx >= 200:
        Bx = 199
    for y in range(Ay,By+1):
        for x in range(Ax,Bx+1):
            print(x, y)
            if y==predpisA*x+predpisB:
                pixels[x,y] = (0,0,0)
    image.show()
main()
