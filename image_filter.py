## Dependencies
import cv2
import time
import numpy as np
import mediapipe as mp

## Drawings
mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

## Webcam Input
BG_COLOR = (0, 255, 196)
vid_cap = cv2.VideoCapture(0)
prevTime = 0
with mp_selfie_segmentation.SelfieSegmentation(
  model_selection=0
) as selfie_segmentation:
  bg_image = None
  while vid_cap.isOpened():
    success, image = vid_cap.read()
    if not success:
      print("Ignoring empty camera frame")
      continue

    ### FLIP & CONVERT
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    ### --
    image.flags.writeable = False
    results = selfie_segmentation.process(image)
    ### --/
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    ### DRAW SELFIE SEGMENTATION
    condition = np.stack(
      (results.segmentation_mask,) * 3, axis=-1
    ) > 0.1
    bg_image = cv2.imread('backgrounds/2.png')
    if bg_image is None:
      bg_image = np.zeros(image.shape, dtype=np.uint8)
      bg_image[:] = BG_COLOR
    output_image = np.where(condition, image, bg_image)
    #### GET && PLACE FRAMERATE
    currTime = time.time()
    fps = 1/(currTime - prevTime)
    prevTime = currTime
    cv2.putText(output_image, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 3, (0, 196, 255), 2)
    cv2.imshow('DIY Zoom Virtual Background', output_image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
vid_cap.release()