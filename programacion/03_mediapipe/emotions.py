import cv2
import mediapipe as mp
import numpy as np
import time

# --- Setup ---
# You'll need to download this file from the MediaPipe website
MODEL_PATH = "./tasks/face_landmarker.task"

# Setup the FaceLandmarker
BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# --- Callback Function ---
# This function will be called asynchronously when a result is ready
def print_result(result: mp.tasks.vision.FaceLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global latest_result
    latest_result = result
    # Optional: print(f'Got result at {timestamp_ms}')


# Create the options for our landmarker
# We need to set running_mode=VisionRunningMode.VIDEO
# and provide a result callback
options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.LIVE_STREAM,
    # THIS IS THE KEY:
    output_face_blendshapes=True,
    output_facial_transformation_matrixes=False,
    num_faces=1,
    result_callback=print_result) # We'll define this callback

# Global variable to store the latest results
latest_result = None
# --- Main Logic ---
# Initialize the landmarker
with FaceLandmarker.create_from_options(options) as landmarker:
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Convert the BGR image to RGB.
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Convert the numpy array to MediaPipe's Image format
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        # Get the current timestamp in milliseconds
        frame_timestamp_ms = int(time.time() * 1000)

        # Run the detection asynchronously
        landmarker.detect_async(mp_image, frame_timestamp_ms)

        # --- Display Logic ---
        # This is where you use the 'latest_result'
        current_emotion = "NEUTRAL" # Default
        
        if latest_result and latest_result.face_blendshapes:
            # We have blendshapes!
            # latest_result.face_blendshapes is a list of lists (one per face)
            # Each inner list contains Category objects (blendshapes)
            
            # Get blendshapes for the first (and only) detected face
            blendshapes = latest_result.face_blendshapes[0]
            
            # Create a dictionary of blendshape names and scores
            # e.g., {'mouthSmileLeft': 0.6, 'mouthSmileRight': 0.5, ...}
            blendshape_scores = {shape.category_name: shape.score for shape in blendshapes}

            # --- Simple Rule-Based Emotion Detection ---
            # You can build more complex rules!
            
            # Happy
            smile_score = (blendshape_scores.get('mouthSmileLeft', 0) + 
                           blendshape_scores.get('mouthSmileRight', 0)) / 2
            if smile_score > 0.5:
                current_emotion = "HAPPY"

            # Surprise
            jaw_open_score = blendshape_scores.get('jawOpen', 0)
            brow_up_score = (blendshape_scores.get('browOuterUpLeft', 0) + 
                             blendshape_scores.get('browOuterUpRight', 0)) / 2
            if jaw_open_score > 0.5 and brow_up_score > 0.3:
                current_emotion = "SURPRISED"

            # Angry
            brow_down_score = (blendshape_scores.get('browDownLeft', 0) + 
                               blendshape_scores.get('browDownRight', 0)) / 2
            if brow_down_score > 0.6:
                current_emotion = "ANGRY"
                
            # Sad
            mouth_frown_score = (blendshape_scores.get('mouthFrownLeft', 0) +
                                 blendshape_scores.get('mouthFrownRight', 0)) / 2
            if mouth_frown_score > 0.5:
                current_emotion = "SAD"

        # Display the detected emotion on the frame
        cv2.putText(image, current_emotion, (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        # Display the mesh (you can adapt your existing draw logic here)
        # You can get landmarks from `latest_result.face_landmarks`
        
        cv2.imshow('MediaPipe Face Mesh with Emotions', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
