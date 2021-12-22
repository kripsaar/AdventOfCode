from os import unlink


enhancement_map = ""

neighbors = [(-1, -1), (0, -1), (1, -1),
             (-1,  0), (0,  0), (1,  0),
             (-1,  1), (0,  1), (1,  1)]

def pad_image(image: str, filler_pixel: str = "."):
    old_row_length = len(image.splitlines()[0].strip())
    unlit_row = filler_pixel * (old_row_length + 4)
    new_image = unlit_row + "\n" + unlit_row
    for row in image.splitlines():
        new_row = "\n" + (filler_pixel * 2) + row + (filler_pixel * 2)
        new_image += new_row
    new_image += "\n" + unlit_row + "\n" + unlit_row
    return new_image

def parse_input(filename: str):
    global enhancement_map
    image = ""
    with open(filename, mode="r") as input:
        enhancement_map, image = [item.strip() for item in input.read().split("\n\n")]
    return image

def translate(pixel: str) -> str:
    if pixel == ".":
        return "0"
    elif pixel == "#":
        return "1"
    raise ValueError(f"Pixel '{pixel}' has to be '.' or '#'!")

def determine_pixel(image_lines: list, x: int, y: int):
    index_bin = ""
    for neighbor in neighbors:
        point = (x + neighbor[0], y + neighbor[1])
        pixel = image_lines[point[1]][point[0]]
        index_bin += translate(pixel)
    index = int(index_bin, 2)
    result = enhancement_map[index]
    return result

def enhance(image: str, filler_pixel: str = "."):
    lit_pixels = 0
    array = image.splitlines()
    width = len(array[0])
    height = len(array)
    image = pad_image(image, filler_pixel).splitlines()
    new_image = ""
    for y in range(1, height + 3):
        for x in range(1, width + 3):
            pixel = determine_pixel(image, x, y)
            if pixel == "#":
                lit_pixels += 1
            new_image += pixel
        new_image += "\n"
    new_image = new_image.strip()
    if filler_pixel == ".":
        filler_pixel = enhancement_map[0]
    elif filler_pixel == "#":
        filler_pixel = enhancement_map[511]
    return new_image, lit_pixels, filler_pixel
            


image = parse_input("input-20")
print(f"Original image: ")
print()
print(image)
print()
enhanced_image, lit_pixels, filler_pixel = enhance(image)
print(f"Enhanced once: ")
print()
print(enhanced_image)
print()
enhanced_image, lit_pixels, filler_pixel = enhance(enhanced_image, filler_pixel)
print(f"Enhanced twice: ")
print()
print(enhanced_image)
print()

print(f"Lit pixels: {lit_pixels}")