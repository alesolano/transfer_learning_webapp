import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
import numpy as np

from config import *


def predict(filename, retrained_model_name, imagenet_model_name, classes):   


    with open(UPLOAD_FOLDER + '/' + filename, 'rb') as f:
        image_string = f.read()


    ### FEATURE EXTRACTOR ###   

    tf.reset_default_graph()    

    from tensorflow.core.framework import graph_pb2
    graph_def = graph_pb2.GraphDef()    

    with open('retrained_models/'+retrained_model_name+'/'+imagenet_model_name+"/frozen_feature_extractor.pb", "rb") as f:
        graph_def.ParseFromString(f.read()) 

    tf.import_graph_def(graph_def, name='') 

    input_image_string = tf.get_default_graph().get_tensor_by_name('input_image_string:0')
    bottleneck = tf.get_default_graph().get_tensor_by_name('InceptionResnetV2/Logits/Flatten/Reshape:0')    

    print("Succesfully loaded feature extractor")   
    
    

    ### CLASSIFIER ###  

    # Link first fully connected layer with the bottleneck
    with tf.name_scope('fc1'):
        W_fc1 = tf.Variable(tf.truncated_normal([1536, 256], stddev=0.1), name='W')
        b_fc1 = tf.Variable(tf.constant(0.1, shape=[256]), name='b')
        fc1 = tf.add(tf.matmul(bottleneck, W_fc1), b_fc1)
        fc1 = tf.nn.relu(fc1)   

    with tf.name_scope('fc2'):
        W_fc2 = tf.Variable(tf.truncated_normal([256, len(classes)], stddev=0.1), name='W')
        b_fc2 = tf.Variable(tf.constant(0.1, shape=[len(classes)]), name='b')
        logits = tf.add(tf.matmul(fc1, W_fc2), b_fc2)
    probs = tf.nn.softmax(logits, name='probs') 

    print("Succesfully built classifier")   
    
    

    ### SAVE GRAPH ###  

    with tf.Session() as sess:
        
        saver = tf.train.Saver()    
        saver.restore(sess, './retrained_models/'+retrained_model_name+'/'+imagenet_model_name+'/flowers_model.ckpt')

        probs_values = sess.run(probs, feed_dict={
            input_image_string: image_string
        })

        pred_idx = probs_values[0].argmax()
        pred_class = classes[pred_idx]
        pred_score = round(100*probs_values[0][pred_idx], 2) # two decimals
        print("I'm {}% sure that this flower is a {}.".format(pred_score, pred_class))