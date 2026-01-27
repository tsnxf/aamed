from PIL import Image
import os

source_path = "/Users/xf/.gemini/antigravity/brain/21385503-f2ac-4500-a06b-d3a435bc9e3e/uploaded_media_1769523727259.jpg"
dest_dir = "/Volumes/WD_BLACK/Agent/aamed/main/assets/images"
dest_path = os.path.join(dest_dir, "hero.jpg")

os.makedirs(dest_dir, exist_ok=True)

img = Image.open(source_path)
width, height = img.size
new_size = min(width, height)

left = (width - new_size) / 2
top = (height - new_size) / 2
right = (width + new_size) / 2
bottom = (height + new_size) / 2

img_cropped = img.crop((left, top, right, bottom))
img_cropped.save(dest_path, quality=90)
print(f"Image cropped and saved to {dest_path}")
