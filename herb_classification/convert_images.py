from PIL import Image
import os
import pathlib

TO_EXTENSION = 'png'  # jpg

image_directory_path = os.path.join(os.getcwd(), 'herb_images')
new_image_directory_path = os.path.join(os.getcwd(), 'herb_images_' + TO_EXTENSION)
pathlib.Path(new_image_directory_path).mkdir(parents=True, exist_ok=True)
image_directory_list = [name for name in os.listdir(image_directory_path) if
                        os.path.isdir(os.path.join(image_directory_path, name))]
print(image_directory_list)
for img_dir in image_directory_list:
    img_dir_path = os.path.join(image_directory_path, img_dir)
    image_file_list = [name for name in os.listdir(img_dir_path) if os.path.isfile(os.path.join(img_dir_path, name))]
    new_dir_path = os.path.join(new_image_directory_path, img_dir)
    print(new_dir_path)
    pathlib.Path(new_dir_path).mkdir(parents=True, exist_ok=True)
    for img_file in image_file_list:
        img_file_path = os.path.join(img_dir_path, img_file)
        # print(img_file_path)
        im = Image.open(img_file_path)
        # rgb_im = im.convert('RGB')
        img_file_name = os.path.splitext(img_file)[0] + '.' + TO_EXTENSION
        new_im_file_path = os.path.join(new_dir_path, img_file_name)
        im.save(new_im_file_path)
