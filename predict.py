import os

import numpy as np
from PIL import ImageEnhance, Image
from cnn.neural_network import CNN
from keras.utils import np_utils
from skimage import io


def convert_img(img_file, path_to_img='./data/'):
    if img_file.endswith('.jpg') or img_file.endswith('.png') or img_file.endswith('.bmp'):
        print(img_file + ' is being processed')
        image = Image.open(os.path.join(path_to_img, img_file))
        if image.width != 32 or image.height != 32:
            image = image.resize((32, 32), resample=Image.LANCZOS)
        if image.mode != '1' or image.mode != 'L':
            image = ImageEnhance.Brightness(image).enhance(3.0)
            image = ImageEnhance.Contrast(image).enhance(10.0)
            image = ImageEnhance.Sharpness(image).enhance(5.0)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        # print image_path + "isn't 1"
        image_path = os.path.join(path_to_img, img_file)
        if image_path.endswith('.jpg'):
            image_path = image_path.strip('.jpg')
            image.save('.' + image_path + '_conv.png')
        if image_path.endswith('.png'):
            image_path = image_path.strip('.png')
            image.save('.' + image_path + '_conv.png')
        if image_path.endswith('.bmp'):
            image_path = image_path.strip('.bmp')
            image.save('.' + image_path + '_conv.png')


print('\nLoading Data For Prediction...')
path = './data/'
all_images = []
all_labels = []
pic_names = []
i = 0

for file in sorted(os.listdir(path)):
    if not file.startswith("."):
        if not file.endswith('_conv.png'):
            convert_img(file)

for file in sorted(os.listdir(path)):
    if not file.startswith("."):
        if file.endswith('_conv.png'):
            print(file + " - " + str(i))
            img = io.imread(os.path.join(path, file), as_gray=True)
            img = img.reshape([32, 32, 1])
            all_images.append(img)
            all_labels.append(i)
            i += 1
            pic_names.append(file)

input_img = np.array(all_images)
input_labels = np_utils.to_categorical(all_labels, i)
print("image shape: ")
print(input_img.shape)

print("label shape: ")
print(input_labels.shape)

print('\nLoading the Model...')
model_labels = []
with open("labels_big_new.txt") as file:  # change labels file name
    for line in file:
        line = line.strip().split()[0]
        model_labels.append(line)

clf = CNN.build(width=32, height=32, depth=1, total_classes=len(model_labels), input_shape=(32, 32, 1),
                Saved_Weights_Path='cnn_weights_big_new.hdf5')  # change model file name

text_file = open("predictions.txt", "w")
print("Writing predictions to predictions.txt ...")
for num in range(0, len(input_labels)):
    probs = clf.predict(input_img[np.newaxis, num])
    prediction = probs.argmax(axis=1)

    print(model_labels[int(prediction[0])] + ' - ' + pic_names[num], file=text_file)
    # print(model_labels[int(prediction[0])] + ' - ' + pic_names[num])
    # print(model_labels[int(prediction[0])] + ' Number of Picture: {}'.format(np.argmax(input_labels[num])))

text_file.close()
print("Done")
