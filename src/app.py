from PIL import Image
import os

SAMPLE_COUNT = 5
ACCURACY = 20

def compare_channel(reference: int, sample: int) -> bool:
    return sample in range(reference - ACCURACY, reference + ACCURACY + 1)

def compare_colors(reference, sample) -> bool:

    (rr, rg, rb) = reference
    (sr, sg, sb) = sample

    return compare_channel(rr, sr) and compare_channel(rg, sg) and compare_channel(rb, sb)

def auto_crop(image: Image) -> Image:
    px = image.load()
    (width, height) = image.size

    y_pos = [(height // SAMPLE_COUNT) * i for i in range(SAMPLE_COUNT)]


    left = 0
    left_ref = px[0, height // 2]

    for left in range(width):
        samples = [px[left, y] for y in y_pos]

        if not all(compare_colors(left_ref, s)  for s in samples):
            break
    
    right = width - 1
    right_ref = px[width - 1, height // 2]

    for right in reversed(range(width)):
        samples = [px[right, y] for y in y_pos]

        if not all(compare_colors(right_ref, s) for s in samples):
            break

    x_pos = [(width // SAMPLE_COUNT) * i for i in range(SAMPLE_COUNT)]

    top = 0
    top_ref = px[width // 2, 0]

    for top in range(height):
        samples = [px[x, top] for x in x_pos]

        if not all(compare_colors(top_ref, s) for s in samples):
            break
    
    bottom = height - 1
    bottom_ref = px[width // 2, height - 1]

    for bottom in reversed(range(height)):
        samples = [px[x, bottom] for x in x_pos]

        if not all(compare_colors(bottom_ref, s)  for s in samples):
            break

    crop = image.crop((left, top, right + 1, bottom + 1))
    return crop


in_dir = "../in"
out_dir = "../out"

files = os.listdir(in_dir)

print("Processing files...")

for i in range(len(files)):
    f = files[i]
    print(f"\r[{i + 1}/{len(files)}]", end="")
    [name, ext] = f.split(".")
    im = Image.open(f"{in_dir}/{f}")
    rgb = im.convert('RGB')
    cropped = auto_crop(rgb)
    cropped.save(f"{out_dir}/{name}.jpg")

print("\nDone.")
