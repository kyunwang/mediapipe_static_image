# %%

import os, os.path
import shutil

import cv2

valid_images = ['.jpg','.gif','.png','.tga']


work_path = os.getcwd()

main_imgs = []
compare_imgs = []


main_path = f'{work_path}/MPII_Manual_selection/images_annotated'
compare_path = f'{work_path}/MPII_Manual_selection/images'
dest_path = f'{work_path}/MPII_Manual_selection/moved'


# Get images from annotated imgs
for f in os.listdir(main_path):
    ext = os.path.splitext(f)[1]

    if ext.lower() not in valid_images:
        continue

    main_imgs.append(f)

# Get images from non annotated images
for f in os.listdir(compare_path):
    ext = os.path.splitext(f)[1]

    if ext.lower() not in valid_images:
        continue

    # compare_imgs.append(os.path.join(compare_path,f))
    compare_imgs.append(f)


# find all identical names in annotated images in non annotated and move them-or copy them toa  adifferent folder
for index, file in enumerate(main_imgs):

	try:
		found_image_index = compare_imgs.index(file);
		found_image = compare_imgs[found_image_index];
		# print(f'main: {file} - compare: {compare_imgs[index]}')
		# print(f'main: {file} - compare: {compare_imgs[found_image_index]}')
		# print(os.path.join(compare_path, found_image))
		print(f'{dest_path}/moved/{found_image}')
		
		# continue

		cv2.imwrite(
			# f'{dest_path}/moved/{str(index)}.jpg', cv2.flip(annotated_image, 1)
			f'{dest_path}/{found_image}',
			cv2.imread(os.path.join(compare_path, found_image))
		)
	except ValueError as e:
		continue
		# print('none')
    	# print(f'Element "{elem}" not found in the list: ', e)
