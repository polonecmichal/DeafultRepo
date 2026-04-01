# preloz text z textoveho suboru na sedu farbu (kazde dve pismena su jedna farba)
from PIL import Image
import math

TXT_FILE = r"C:\Users\misko\Downloads\ciernobiely_obrazok_1.txt"
OUTPUT_FILE = r"C:\Users\misko\Downloads\ciernobiely_obrazok_1.png"


def preloz_text_na_sedu_farbu(text):
    hex_chars = ''.join([c for c in text if c.lower() in '0123456789abcdef'])
    farby = []
    for i in range(0, len(hex_chars), 2):
        dvojica = hex_chars[i:i+2]
        if len(dvojica) != 2:
            break
        hodnota = int(dvojica, 16)
        farby.append((hodnota, hodnota, hodnota))
    return farby


def main():
    with open(TXT_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        raw_text = f.read()
    pixely = preloz_text_na_sedu_farbu(raw_text)

    pixel_count = len(pixely)
    width = int(math.sqrt(pixel_count))
    if width * width < pixel_count:
        width += 1
    height = (pixel_count + width - 1) // width


    image_width, image_height = 265, 154
    image = Image.new('RGB', (image_width, image_height))
    total_pixels = image_width * image_height
    if pixel_count < total_pixels:
        data = pixely + [(255, 255, 255)] * (total_pixels - pixel_count)
    else:
        data = pixely[:total_pixels]
    image.putdata(data)
    image.save(OUTPUT_FILE)
    image.show()
    print(f"Obrazok ulozeny do {OUTPUT_FILE} ({image_width}x{image_height}, pixely={pixel_count})")

if __name__ == '__main__':
    main()
