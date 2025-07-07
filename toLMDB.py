import xmltodict
from PIL import Image
import os

xml_file = '/content/C133_D1_P1.xml'       
image_file = '/content/C133_D1_P1.jpg'     


with open(xml_file, 'rb') as f:
    raw = f.read()
try:
    xml = raw.decode('utf-8')
except UnicodeDecodeError:
    xml = raw.decode('utf-16')
voc = xmltodict.parse(xml)

dataset = voc['annotation']
img = Image.open(image_file)
save_dir = 'crops_' + os.path.splitext(image_file)[0]
os.makedirs(save_dir, exist_ok=True)

objects = dataset['object']
if not isinstance(objects, list):
    objects = [objects]  # Handle single-object case

label_lines = []
i = 0

for item in objects:
    if item['name'] != 'text':
        continue
    bndbox = item['bndbox']
    xmin, ymin, xmax, ymax = [int(float(bndbox[k])) for k in ('xmin', 'ymin', 'xmax', 'ymax')]
    crop = img.crop((xmin, ymin, xmax, ymax))

    # Extract text (word inside <text> tag)
    label = item.get('text', '').strip()
    # Safe filename
    crop_filename = f"{os.path.splitext(image_file)[0]}_text_{i}.png"
    crop.save(os.path.join(save_dir, crop_filename))
    print(f"Cropped and saved: {crop_filename}")

    # Add line: filename + tab + label
    label_lines.append(f"{crop_filename}\t{label}")
    i += 1

# Write to txt file as columns
with open(os.path.join(save_dir, "labels.txt"), "w", encoding="utf-8") as f:
    for line in label_lines:
        f.write(line + "\n")
