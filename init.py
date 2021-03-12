import os, os.path
import json

import cv2
import mediapipe as mp
from PIL import Image


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

imgs = []
valid_images = ['.jpg','.gif','.png','.tga']

# Current python dir
path = f'{os.getcwd()}/images'
# 
export_path = f'{os.getcwd()}/exports'


output = []

print(mp_hands.HAND_CONNECTIONS)
print(mp_hands.HandLandmark.INDEX_FINGER_TIP)


for f in os.listdir(path):
    ext = os.path.splitext(f)[1]

    if ext.lower() not in valid_images:
        continue
    imgs.append(os.path.join(path,f))

# For static images:
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.75) as hands:
    
    # for index, file in enumerate(file_list):
    # for file in enumerate(imgs):
    for index, file in enumerate(imgs):
        # Read an image, flip it around y-axis for correct handedness output (see
        # above).
        image = cv2.flip(cv2.imread(file), 1)
        # Convert the BGR image to RGB before processing.
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Print handedness and draw hand landmarks on the image.
        # print('Handedness:', results.multi_handedness)
        if not results.multi_hand_landmarks:
            continue

        image_height, image_width, _ = image.shape
        annotated_image = image.copy()

        for hand_landmarks in results.multi_hand_landmarks:
            indexTip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # print('hand_landmarks:', hand_landmarks)
            print(
                f'Index finger tip coordinates: (',
                f'{indexTip.x * image_width}, '
                f'{indexTip.y * image_height})'
            )

            output.append({ 'file': f'{str(index)}.jpg', 'x': indexTip.x, 'y': indexTip.y })

            # Drawing on the image
            mp_drawing.draw_landmarks(annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            # mp_drawing.draw_landmarks(annotated_image, hand_landmarks, [indexTip])


            # Export annotated image
            print(f'{export_path}/{str(index)}.jpg')
            cv2.imwrite(
                f'{export_path}/images/{str(index)}.jpg', cv2.flip(annotated_image, 1)
            )

    # Export to json
    with open(f'{export_path}/output.json', 'w') as out_file:
        json.dump(output, out_file, ensure_ascii=False)