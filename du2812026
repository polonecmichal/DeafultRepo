#prevod obsahu spravy do inej abeedy pomocou kluca
#zaklad je verejny
#sifrovanie symetricke - pouzivame ten isty kluc na sifrovanie aj desifrovanie
#sifrovanie asymetricke - pouzivame par klucov, verejny a sukromny, verejny sa pouziva na sifrovanie a sukromny na desifrovanie
#steganografia - ukryvanie spravy v inom texte, obrazku, zvuku
# sprava'ahoj' 
# > priradenie ciselnej hodnoty z ascii 
# > prevedenie na bity (7) 
# > skontrolovat ci dlyka kodovania je 7 bitov 
# > 11011000 
# > 7 pixeov na znak > treba urcit jednu farbu z rgb toho pixelu do ktorej budeme kodovat 
# > modra 
# > prevedies hodnotu farby do 2 sustavy 
# > zmenime posledny bit

import PIL
from PIL import Image
import pip
x = input("Desifrovat alebo sifrovat? (d/s): ") 
def picture_shreder(bs, obr):
    pixels = obr.load()
    for i in range(len(bs)):
        x = i % obr.size[0]
        y = i // obr.size[0]
        blue_bin = bin(pixels[x, y][2])[2:-1:]# ta 2 odtrhne 0b, -1 odtrhne posledny bit
        blue_bin = blue_bin + bs[i]
        new_blue = int(blue_bin, 2)
        pixels[x,y] = (pixels[x,y][0], pixels[x,y][1], new_blue)
    obr.save('jupi.png')

def bin_to_sprava(bin_sprava):
    output = ""
    for i in range(0, len(bin_sprava), 7):
        char_bin = bin_sprava[i:i+7]
        if len(char_bin) < 7:
            break
        char_dec = int(char_bin, 2)
        char = chr(char_dec)
        if char == '#':
            break
        output += char
    return output

if x == 's': 
    sprava = input("Zadaj správu: ")
    obr_path = input("Cesta k vstupnemu obrazku: ").strip('"')
    obr = Image.open(obr_path)
    def sprava_to_bin(sprava, obr):
        sprava += '#'
        output = "" 
        for char in sprava:
            temp =  bin(ord(char))[2::]
            if len(temp) < 7:
                pocet = 7 - len(temp)
                temp = '0' * pocet + temp
            output += temp
        return output
    bin_sprava = sprava_to_bin(sprava, obr)
    picture_shreder(bin_sprava, obr)
    print("Obrazok ulozeny ako jupi.png")

elif x == 'd':
    cesta = input("Zadej cestu k obrázku: ").strip('"')
    obr_sprava = Image.open(r"" + cesta)
    max_bits = obr_sprava.size[0] * obr_sprava.size[1]
    def bulharsko(bs_len):
        pixels = obr_sprava.load()
        output = ""
        for i in range(bs_len):
            x = i % obr_sprava.size[0]
            y = i // obr_sprava.size[0]
            blue = pixels[x, y][2]
            blue_bin = bin(blue)[2::]
            if len(blue_bin) < 8:
                blue_bin = '0' * (8 - len(blue_bin)) + blue_bin
            output += blue_bin[-1]
            if len(output) % 7 == 0:
                char_bin = output[-7:]
                char_dec = int(char_bin, 2)
                char = chr(char_dec)
                if char == '#':
                    return output
        return output
    bin_message = bulharsko(max_bits)
    print(bin_to_sprava(bin_message))
