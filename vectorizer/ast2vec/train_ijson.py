"""Train the ast2vect network."""

import json
import os
import logging
import cPickle as pickle
import tensorflow as tf
import vectorizer.ast2vec.network as network
import vectorizer.ast2vec.sampling_ijson as sampling_ijson
from vectorizer.node_map_php import PHP_NODE_MAP
from vectorizer.node_map import NODE_MAP
from vectorizer.ast2vec.parameters import \
    NUM_FEATURES, LEARN_RATE, BATCH_SIZE, EPOCHS, CHECKPOINT_EVERY
from tensorflow.contrib.tensorboard.plugins import projector

def learn_vectors(args, samplefile, logdir, outfile, num_feats=NUM_FEATURES, epochs=EPOCHS):
    """Learn a vector representation of Python AST nodes."""

    # build the inputs and outputs of the network
    input_node, label_node, embed_node, loss_node = network.init_net(args,
        num_feats=num_feats,
        batch_size=BATCH_SIZE
    )

    # use gradient descent with momentum to minimize the training objective
    train_step = tf.train.GradientDescentOptimizer(LEARN_RATE). \
                    minimize(loss_node)

    tf.summary.scalar('loss', loss_node)

    ### init the graph
    sess = tf.Session()

    with tf.name_scope('saver'):
        # Saver instance.  To save network graph for future use after training.
        saver = tf.train.Saver()
        summaries = tf.summary.merge_all()
        writer = tf.summary.FileWriter(logdir, sess.graph)
        config = projector.ProjectorConfig()
        embedding = config.embeddings.add()
        embedding.tensor_name = embed_node.name
        if not args.php:
            embedding.metadata_path = os.path.join('vectorizer', 'metadata.tsv')
        else:
            embedding.metadata_path = os.path.join('vectorizer', 'metadata_php.tsv')
        projector.visualize_embeddings(writer, config)

    sess.run(tf.global_variables_initializer())

    checkfile = os.path.join(logdir, 'ast2vec.ckpt')

    embed_file = open(outfile, 'wb')

    step = 0
    for epoch in range(1, epochs+1):

        sample_gen = sampling_ijson.batch_samples(args, samplefile, BATCH_SIZE)
        for batch in sample_gen:
            input_batch, label_batch = batch

            _, summary, embed, err = sess.run(
                [train_step, summaries, embed_node, loss_node],
                feed_dict={
                    input_node: input_batch,
                    label_node: label_batch
                }
            )
            print('Epoch: ', epoch, 'Loss: ', err)
            writer.add_summary(summary, step)
            if step % CHECKPOINT_EVERY == 0:
                # save state (tensorflow variables) so we can resume later
                saver.save(sess, os.path.join(checkfile), step)
                print('Checkpoint saved.')
                # save embeddings
                if not args.php:
                    pickle.dump((embed, NODE_MAP), embed_file)
                else:
                    pickle.dump((embed, PHP_NODE_MAP), embed_file)
            step += 1

    # save embeddings and the mapping
    if not args.php:
        pickle.dump((embed, NODE_MAP), embed_file)
    else:
        pickle.dump((embed, PHP_NODE_MAP), embed_file)

    embed_file.close()
    saver.save(sess, os.path.join(checkfile), step)
