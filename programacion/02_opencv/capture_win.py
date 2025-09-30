import cv2
import time
import os

# shared path (adjust to your Windows user)
out_dir = r"./frames/"
os.makedirs(out_dir, exist_ok=True)

cap = cv2.VideoCapture(0)

i = 0
while True:
    ret, frame = cap.read()
    if not ret:
        continue

    filename = os.path.join(out_dir, f"frame_{i:04d}.png")
    cv2.imwrite(filename, frame)
    i += 1

    time.sleep(0.2)  # capture ~5 fps

