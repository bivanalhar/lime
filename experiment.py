import tensorflow as tf
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

slim = tf.contrib.slim
sys.path.append("/usr/local/lib/python3.5/dist-packages/tensorflow/models/research/slim")

from nets import inception
from preprocessing import inception_preprocessing
from datasets import imagenet
from skimage.segmentation import mark_boundaries
from lime import lime_image

import cv2

session = tf.Session()
image_size = inception.inception_v3.default_image_size

def transform_img_fn(path_list):
	out = []
	for f in path_list:
		file = open(f, 'rb')
		image_raw = tf.image.decode_jpeg(file.read(), channels=3)
		image = inception_preprocessing.preprocess_image(image_raw, image_size, image_size, is_training=False)
		out.append(image)
	return session.run([out])[0]

names = imagenet.create_readable_names_for_imagenet_labels()

processed_images = tf.placeholder(tf.float32, shape = (None, 299, 299, 3))

with slim.arg_scope(inception.inception_v3_arg_scope()):
	logits, _ = inception.inception_v3(processed_images, num_classes=1001, is_training=False)
probabilities = tf.nn.softmax(logits)

checkpoints_dir = '/usr/local/lib/python3.5/dist-packages/tensorflow/models/research/slim/pretrained'
init_fn = slim.assign_from_checkpoint_fn(
	os.path.join(checkpoints_dir, 'inception_v3.ckpt'),
	slim.get_model_variables('InceptionV3'))
init_fn(session)

def predict_fn(images):
	return session.run(probabilities, feed_dict={processed_images: images})

images = transform_img_fn(['dog.jpg'])
preds = predict_fn(images)
id_list = []

for x in preds.argsort()[0][-5:]:
	id_list.insert(0, x)

image = images[0]

explainer = lime_image.LimeImageExplainer()
explanation, segments = explainer.explain_instance_and_get_segments(image, predict_fn, top_labels = 5, hide_color = 0, num_samples = 1000)

temp, mask = explanation.get_image_and_mask(id_list[0], positive_only=False, num_features=30, hide_rest=True)

img_save = mark_boundaries(image = temp / 2 + 0.5, label_img = segments, color = (0,0,0))
plt.imsave(fname = "explain_dog2.jpeg", arr = img_save)

print(list(segments))