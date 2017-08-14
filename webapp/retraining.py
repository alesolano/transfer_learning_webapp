from os import environ
environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
import numpy as np


bottleneck_size = 1536

def retrain(retrained_model_name, imagenet_model_name):

    # read codes and labels from file
    import csv  

    with open('retrained_models/'+retrained_model_name+'/'+imagenet_model_name+'/labels') as f:
        reader = csv.reader(f, delimiter='\n')
        labels = np.array([each for each in reader if len(each) > 0]).squeeze()
    with open('retrained_models/'+retrained_model_name+'/'+imagenet_model_name+'/codes') as f:
        codes = np.fromfile(f, dtype=np.float32)
        codes = codes.reshape((len(labels), -1))    
    

    from sklearn.preprocessing import LabelBinarizer    

    lb = LabelBinarizer()
    lb.fit(labels)  

    labels_vecs = lb.transform(labels)  
    

    # GET VALIDATION
    from sklearn.model_selection import StratifiedShuffleSplit  

    ss = StratifiedShuffleSplit(n_splits=1, test_size=0.2)  

    train_idx, val_idx = next(ss.split(codes, labels))  

    half_val_len = int(len(val_idx)/2)
    val_idx, test_idx = val_idx[:half_val_len], val_idx[half_val_len:]  

    train_x, train_y = codes[train_idx], labels_vecs[train_idx]
    val_x, val_y = codes[val_idx], labels_vecs[val_idx]
    test_x, test_y = codes[test_idx], labels_vecs[test_idx] 
    

    print("Train shapes (x, y):", train_x.shape, train_y.shape)
    print("Validation shapes (x, y):", val_x.shape, val_y.shape)
    print("Test shapes (x, y):", test_x.shape, test_y.shape)    
    

    inputs_ = tf.placeholder(tf.float32, shape=[None, codes.shape[1]], name='inputs_clf')
    labels_ = tf.placeholder(tf.int64, shape=[None, labels_vecs.shape[1]], name='labels_clf')   
    

    with tf.name_scope('fc1'):
        W_fc1 = tf.Variable(tf.truncated_normal([bottleneck_size, 256], stddev=0.1), name='W')
        b_fc1 = tf.Variable(tf.constant(0.1, shape=[256]), name='b')
        fc1 = tf.add(tf.matmul(inputs_, W_fc1), b_fc1)
        fc1 = tf.nn.relu(fc1)   

    with tf.name_scope('fc2'):
        W_fc2 = tf.Variable(tf.truncated_normal([256, labels_vecs.shape[1]], stddev=0.1), name='W')
        b_fc2 = tf.Variable(tf.constant(0.1, shape=[labels_vecs.shape[1]]), name='b')
        logits = tf.add(tf.matmul(fc1, W_fc2), b_fc2)
    probs = tf.nn.softmax(logits, name='probs') 
    

    with tf.name_scope('train_clf'):
        cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=labels_, logits=logits)
        cost = tf.reduce_mean(cross_entropy)    

        optimizer = tf.train.AdamOptimizer().minimize(cost) 

    with tf.name_scope('accuracy_clf'):
        predicted = tf.nn.softmax(logits)
        correct_pred = tf.equal(tf.argmax(predicted, 1), tf.argmax(labels_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))    
    

    def get_batches(x, y, n_batches=10):
        """ Return a generator that yields batches from arrays x and y. """
        batch_size = len(x)//n_batches
        
        for ii in range(0, n_batches*batch_size, batch_size):
            # If we're not on the last batch, grab data with size batch_size
            if ii != (n_batches-1)*batch_size:
                X, Y = x[ii: ii+batch_size], y[ii: ii+batch_size] 
            # On the last batch, grab the rest of the data
            else:
                X, Y = x[ii:], y[ii:]
            # I love generators
            yield X, Y  
    

    epochs = 10
    iteration = 0
    saver = tf.train.Saver()
    with tf.Session() as sess:
        
        sess.run(tf.global_variables_initializer())
        for e in range(epochs):
            for x, y in get_batches(train_x, train_y):
                loss, _ = sess.run([cost, optimizer], feed_dict={
                    inputs_: x,
                    labels_: y
                    })
                print("Epoch: {}/{}".format(e+1, epochs),
                      "Iteration: {}".format(iteration),
                      "Training loss: {:.5f}".format(loss))
                iteration += 1
                
                if iteration % 5 == 0:
                    val_acc = sess.run(accuracy, feed_dict={
                        inputs_: val_x,
                        labels_: val_y
                        })
                    print("Validation Acc: {:.4f}".format(val_acc))
        
        saver.save(sess, './retrained_models/'+retrained_model_name+'/'+imagenet_model_name+'/flowers_model.ckpt')
        print('Model trained and saved in ./retrained_models/'+retrained_model_name+'/'+imagenet_model_name+'/flowers_model.ckpt')  

        test_acc = sess.run(accuracy, feed_dict={
            inputs_: test_x,
            labels_: test_y
            })
        print("Test accuracy: {:.4f}".format(test_acc))