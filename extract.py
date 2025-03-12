from PIL import Image

# Open the GIF file
# cus_gif = Image.open("deadpixels-dpgc.gif")
gif = Image.open("dpgc-dead-pixels.gif")

# Extract frames and save them as individual images
frame_number = 0
try:
    while True:
        gif.seek(frame_number)
        gif.save(f"frame{frame_number}.png")
        frame_number += 1
except EOFError:
    pass  # End of GIF