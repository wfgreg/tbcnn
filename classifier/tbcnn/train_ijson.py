"""Train the cnn model as  described in Lili Mou et al. (2015)
https://arxiv.org/pdf/1409.5718.pdf"""

import ijson.backends.yajl2_c as ijson
import os,sys
import logging
import pickle
import tensorflow as tf
import numpy as np
import classifier.tbcnn.network as network
import classifier.tbcnn.sampling_ijson as sampling_ijson
import classifier.tbcnn.sampling as sampling
from classifier.tbcnn.parameters import LEARN_RATE, EPOCHS, \
    CHECKPOINT_EVERY, BATCH_SIZE, KBATCH_SIZE
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

def get_line_count(filepath):
    with open(filepath) as f:
        for i, line in enumerate(f):
            pass
    f.close()
    return (i+1)

def train_model(args, logdir, infile, embedfile, epochs=EPOCHS):
    """Train a classifier to label ASTs"""

    labels=["benign","malicious"]

    with open(embedfile, 'rb') as fh:
        embeddings, embed_lookup = pickle.load(fh)
        num_feats = len(embeddings[0])

    # build the inputs and outputs of the network
    nodes_node, children_node, hidden_node = network.init_net(
        num_feats,
        len(labels)
    )

    out_node = network.out_layer(hidden_node)
    labels_node, loss_node = network.loss_layer(hidden_node, len(labels))

    optimizer = tf.train.AdamOptimizer(LEARN_RATE)
    train_step = optimizer.minimize(loss_node)

    tf.summary.scalar('loss', loss_node)

    ### init the graph
    sess = tf.Session()#config=tf.ConfigProto(device_count={'GPU':0}))
    sess.run(tf.global_variables_initializer())

    with tf.name_scope('saver'):
        saver = tf.train.Saver()
        summaries = tf.summary.merge_all()
        writer = tf.summary.FileWriter(logdir, sess.graph)

    checkfile = os.path.join(logdir, 'cnn_tree.ckpt')

    num_batches = get_line_count(infile)-2
#    num_batches = len(trees) // BATCH_SIZE + (1 if len(trees) % BATCH_SIZE != 0 else 0)
    for epoch in range(1, epochs+1):
        for i, batch in enumerate(sampling_ijson.batch_samples_ijson(
            args, sampling_ijson.gen_samples_ijson(infile, labels, embeddings, embed_lookup), BATCH_SIZE
        )):
            nodes, children, meta, batch_labels = batch
            step = (epoch - 1) * num_batches + i * BATCH_SIZE

            if not nodes:
                continue # don't try to train on an empty batch

            _, summary, err, out = sess.run(
                [train_step, summaries, loss_node, out_node],
                feed_dict={
                    nodes_node: nodes,
                    children_node: children,
                    labels_node: batch_labels
                }
            )

            print('Epoch:', epoch,
                  'Step:', step,
                  'Loss:', err,
                  'Max nodes:', len(nodes[0])
            )

            writer.add_summary(summary, step)
            if step % CHECKPOINT_EVERY == 0:
                # save state so we can resume later
                saver.save(sess, os.path.join(checkfile), step)
                print('Checkpoint saved.')

    saver.save(sess, os.path.join(checkfile), step)

    # compute the training accuracy
    correct_labels = []
    predictions = []
    print('Computing training accuracy...')
    for batch in sampling_ijson.batch_samples_ijson(
        args, sampling_ijson.gen_samples_ijson(infile, labels, embeddings, embed_lookup), 1
    ):
        nodes, children, meta, batch_labels = batch
        output = sess.run([out_node],
            feed_dict={
                nodes_node: nodes,
                children_node: children,
            }
        )
        correct_labels.append(np.argmax(batch_labels))
        predictions.append(np.argmax(output))

    target_names = list(labels)
    print('Accuracy:', accuracy_score(correct_labels, predictions))
    print(classification_report(correct_labels, predictions, target_names=target_names))
    print(confusion_matrix(correct_labels, predictions))
