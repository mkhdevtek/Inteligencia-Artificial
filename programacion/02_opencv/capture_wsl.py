import cv2
import numpy as np
import glob
import time

frame_dir = "./frames/"

while True:
    frames = sorted(glob.glob(f"{frame_dir}/*.png"))
    if not frames:
        time.sleep(0.1)
        continue

    latest = frames[-1]
    img = cv2.imread(latest)

    # Example: print RGB of pixel (100,100)
    b, g, r = img[100, 100]
    print(f"Pixel(100,100) -> R:{r} G:{g} B:{b}")

    cv2.imshow("Frame from Windows", img)
    if cv2.waitKey(100) & 0xFF == 27:  # Esc to exit
        break

