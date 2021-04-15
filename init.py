# %%
import os, os.path
import json
from datetime import datetime
import shutil

start_time = datetime.now()

import cv2
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
Landmarks = mp_hands.HandLandmark
IndexFinger = [
    Landmarks['WRIST'],
    Landmarks['INDEX_FINGER_DIP'],
    Landmarks['INDEX_FINGER_MCP'],
    Landmarks['INDEX_FINGER_PIP'],
    Landmarks['INDEX_FINGER_TIP']
]


imgs = []
valid_images = ['.jpg','.gif','.png','.tga']
output = []


SOURCE_DIR_NAME = 'images_smallset'
SOURCE_DIR_PATH = f'{os.getcwd()}/input/{SOURCE_DIR_NAME}'

EXPORT_PATH = f'{os.getcwd()}/exports/{SOURCE_DIR_NAME}'
EXPORT_PATH_IMAGES = f'{EXPORT_PATH}/images'
EXPORT_PATH_IMAGES_ANN = f'{EXPORT_PATH}/images_annotated'

# Quick clean - delete create output dirs with content

# Clean up first if they already exist
# And create them again cleanly
if os.path.exists(EXPORT_PATH_IMAGES):
    shutil.rmtree(EXPORT_PATH_IMAGES)
if os.path.exists(EXPORT_PATH_IMAGES_ANN):
    shutil.rmtree(EXPORT_PATH_IMAGES_ANN)

if not os.path.exists(EXPORT_PATH_IMAGES):
    os.makedirs(EXPORT_PATH_IMAGES)
if not os.path.exists(EXPORT_PATH_IMAGES_ANN):
    os.makedirs(EXPORT_PATH_IMAGES_ANN)


for f in os.listdir(SOURCE_DIR_PATH):
    ext = os.path.splitext(f)[1]

    if ext.lower() not in valid_images:
        continue
    imgs.append(os.path.join(SOURCE_DIR_PATH,f))

# For static images:
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.8
) as hands:
    for index, file in enumerate(imgs):
        # Read an image, flip it around y-axis for correct handedness output (see
        # above).
        image = cv2.flip(cv2.imread(file), 1)
        # Convert the BGR image to RGB before processing.
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Print handedness and draw hand landmarks on the image.
        if not results.multi_hand_landmarks:
            continue

        image_height, image_width, _ = image.shape
        annotated_image = image.copy()

        for hand_landmarks in results.multi_hand_landmarks:
            indexTip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Get all landmarks
            output.append({ 'file': f'{str(index)}.jpg', 'landmarks': [], 'center': [] })

            all_coord_x = 0
            all_coord_y = 0


            # for landmark in IndexFinger:
            for landmark in Landmarks:
                output[-1]['landmarks'].append(hand_landmarks.landmark[landmark].x)
                output[-1]['landmarks'].append(hand_landmarks.landmark[landmark].y)

                all_coord_x += hand_landmarks.landmark[landmark].x
                all_coord_y += hand_landmarks.landmark[landmark].y


            # Set center coord of bbox
            center_x = all_coord_x / len(hand_landmarks.landmark)
            center_y = all_coord_y / len(hand_landmarks.landmark)
            output[-1]['center'].append(center_x)
            output[-1]['center'].append(center_y)


            # Export images with detected hands
            cv2.imwrite(
                f'{EXPORT_PATH_IMAGES}/{str(index)}.jpg', cv2.flip(image, 1)
            )


            # Drawing on the image
            mp_drawing.draw_landmarks(annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Export annotated image
            print(f'{EXPORT_PATH_IMAGES}/{str(index)}.jpg')
            cv2.imwrite(
                f'{EXPORT_PATH_IMAGES_ANN}/{str(index)}.jpg', cv2.flip(annotated_image, 1)
            )

    # Export to json
    with open(f'{EXPORT_PATH}/output.json', 'w') as out_file:
        json.dump(output, out_file, ensure_ascii=False)
        print('Exported JSON')
        end_time = datetime.now()
        print('Duration: {}'.format(end_time - start_time))
        # print("--- %s seconds ---" % (time.clock() - start_time))