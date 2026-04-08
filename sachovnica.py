from PIL import Image

img = Image.new('RGB', (200, 300), color = 'white')
pic = img.load()

for x in range(200):
    for y in range(300):
        if (x+y) % 2 == 0: 
            img.putpixel((x, y), (0, 0, 0))
img.show()
