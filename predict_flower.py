from os import environ
environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf

### CLASSES ###
classes = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']


### LOAD IMAGE ###
import sys
with open(sys.argv[1], 'rb') as f:
    image_string = f.read()


### GRAPH 1: FEATURE EXTRACTION ###
tf.reset_default_graph()

saver_fe = tf.train.import_meta_graph('./models/inception_resnet_v2/model.ckpt.meta')

input_image_string = tf.get_default_graph().get_tensor_by_name('input_image_string:0')
bottleneck = tf.get_default_graph().get_tensor_by_name('InceptionResnetV2/Logits/Flatten/Reshape:0')


### SESSION 1: FEATURE EXTRACTION ###
with tf.Session() as sess:
    saver_fe.restore(sess, './models/inception_resnet_v2/model.ckpt')

    features = sess.run(bottleneck, feed_dict={
            input_image_string: image_string
        })


### GRAPH 2: CLASSIFICATION ###

tf.reset_default_graph()

saver_clf = tf.train.import_meta_graph('./models/inception_resnet_v2/flowers_clf.ckpt.meta')

inputs_clf = tf.get_default_graph().get_tensor_by_name('inputs_clf:0')
probs = tf.get_default_graph().get_tensor_by_name('probs_clf:0')


### SESSION 2: CLASSIFICATION ###
with tf.Session() as sess:
    saver_clf.restore(sess, './models/inception_resnet_v2/flowers_clf.ckpt')
    
    probs_values = sess.run(probs, feed_dict={
            inputs_clf: features
        })

    
    pred_idx = probs_values[0].argmax()
    pred_class = classes[pred_idx]
    pred_score = round(100*probs_values[0][pred_idx], 2) # two decimals
    print("I'm {}% sure that this flower is a {}.".format(pred_score, pred_class))