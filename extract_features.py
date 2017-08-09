import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
import tensorflow as tf

import cv2

data_dir = 'flower_photos/'
contents = os.listdir(data_dir)
classes = [each for each in contents if os.path.isdir(data_dir + each)]

codes = None # empty numpy array
labels = [] # empty list

### GRAPH ###
tf.reset_default_graph()

saver = tf.train.import_meta_graph('./models/inception_resnet_v2/model.ckpt.meta')

input_image_string = tf.get_default_graph().get_tensor_by_name('input_image_string:0')
bottleneck = tf.get_default_graph().get_tensor_by_name('InceptionResnetV2/Logits/Flatten/Reshape:0')

### SESSION ###
with tf.Session() as sess:
    saver.restore(sess, './models/inception_resnet_v2/model.ckpt')
        
    for each in classes:
        print("Starting {} images".format(each))
        class_path = data_dir + each
        files = os.listdir(class_path)

        for ii, file in enumerate(files, 1):

            # Add images to the current batch
            with open(os.path.join(class_path, file), 'rb') as f:
                image_string = f.read()
            
            # Running the batch through the network to get the codes
            new_code = sess.run(bottleneck, feed_dict={
                input_image_string: image_string
                })
                
            # Building an array with the codes
            if codes is None:
                codes = new_code
            else:
                codes = np.concatenate((codes, new_code))

            labels.append(each)
                
            if ii % 50 == 0:
                print('{} images processed'.format(ii))


# write codes to file
with open('codes', 'w') as f:
    codes.tofile(f)

# write labels to file
import csv
with open('labels', 'w') as f:
    writer = csv.writer(f, delimiter='\n')
    writer.writerow(labels)