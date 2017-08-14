import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
import tensorflow as tf

from config import *


bottleneck_name = 'InceptionResnetV2/Logits/Flatten/Reshape'


def extract_features(retrained_model_name, imagenet_model_name, classes):

    codes = None # empty numpy array
    labels = [] # empty list

    ### GRAPH ###
    tf.reset_default_graph()

    saver = tf.train.import_meta_graph('./imagenet_models/'+imagenet_model_name+'/model.ckpt.meta')

    input_image_string = tf.get_default_graph().get_tensor_by_name('input_image_string:0')
    bottleneck = tf.get_default_graph().get_tensor_by_name(bottleneck_name+':0')

    print("Succesfully loaded feature extractor")

    ### SESSION ###
    with tf.Session() as sess:
        saver.restore(sess, './imagenet_models/'+imagenet_model_name+'/model.ckpt')
        print("Extracting features...")
        
        for each in classes:
            print("Starting {} images".format(each))
            class_path = UPLOAD_FOLDER + '/' + each
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


    print("Succesfully extracted features")

    if not os.path.exists('retrained_models/'+retrained_model_name+'/'+imagenet_model_name):
        os.makedirs('retrained_models/'+retrained_model_name+'/'+imagenet_model_name)

    # write codes to file
    with open('retrained_models/'+retrained_model_name+'/'+imagenet_model_name+'/codes', 'w') as f:
        codes.tofile(f)

    # write labels to file
    import csv
    with open('retrained_models/'+retrained_model_name+'/'+imagenet_model_name+'/labels', 'w') as f:
        writer = csv.writer(f, delimiter='\n')
        writer.writerow(labels)


    print("Freezing feature extractor...")

    # FREEZE
    from tensorflow.python.tools import freeze_graph

    input_graph_path = 'imagenet_models/'+imagenet_model_name+"/graph.pb"
    input_saver_def_path = ""
    input_binary = False
    checkpoint_path = 'imagenet_models/'+imagenet_model_name+"/model.ckpt"
    output_node_names = bottleneck_name
    restore_op_name = "save/restore_all"
    filename_tensor_name = "save/Const:0"
    output_graph_path = 'retrained_models/'+retrained_model_name+'/'+imagenet_model_name+"/frozen_feature_extractor.pb"
    clear_devices = False

    freeze_graph.freeze_graph(input_graph_path, input_saver_def_path, input_binary, checkpoint_path,
        output_node_names, restore_op_name, filename_tensor_name, output_graph_path, clear_devices, "")


