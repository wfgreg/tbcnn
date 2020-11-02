"""Functions to help with sampling trees."""

import ijson.backends.yajl2_c as ijson

import sys
import pickle,json
import numpy as np
import random

def gen_samples_ijson(infile, labels, vectors, vector_lookup):
    """Creates a generator that returns a tree in BFS order with each node
    replaced by its vector embedding, and a child lookup table."""

    # encode labels as one-hot vectors
    label_lookup = {label: _onehot(i, len(labels)) for i, label in enumerate(labels)}

    f = open(infile, 'rb')
    trees = ijson.items(f,'item')

    for tree in trees:
        nodes = [] # array (with an entry per node of tree) of vectors holding feature weights (from vectorizer) for node type
        children = [] # array (with an entry per node of tree) of lists of parent->child mappings by indices in nodes array
        label = label_lookup[tree['label']]

        queue = [(tree['tree'], -1)]
        while queue:
            node, parent_ind = queue.pop(0)
            node_ind = len(nodes)
            # add children and the parent index to the queue
            queue.extend([(child, node_ind) for child in node['children']])
            # create a list to store this node's children indices
            children.append([])
            # add this child to its parent's child list
            if parent_ind > -1:
                children[parent_ind].append(node_ind)
            # get this node's feature weights by looking up the node type's number (from the node map) to find its position in the vectorized features
            nodes.append(vectors[vector_lookup[node['node']]])

        yield (nodes, children, tree['meta'], label)

def batch_samples_ijson(args, gen, batch_size):
    """Batch samples from a generator"""
    nodes, children, meta, labels = [], [], [], []
    samples = 0
    wholesize = 0
    for n, c, m, l in gen:
        nodes.append(n)
        children.append(c)
        meta.append(m)
        labels.append(l)

        # map(lambda x:sys.getsizeof(x),[n,c,labels]))) produces list of arrays of the getsize of each data set
        if len(n) > 10000:
            print(len(n))
            print(sum(map(sum,map(lambda x:map(sys.getsizeof,x),[n,c,labels]))))
        samples += 1
        if samples >= batch_size:
            yield _pad_batch_ijson(nodes, children, meta, labels)
            nodes, children, meta, labels = [], [], [], []
            samples = 0

    if nodes:
        yield _pad_batch_ijson(nodes, children, meta, labels)

def _pad_batch_ijson(nodes, children, meta, labels):
    if not nodes:
        return [], [], [], []
    max_nodes = max([len(x) for x in nodes])
    max_children = max([len(x) for x in children])
    feature_len = len(nodes[0][0])
    child_len = max([len(c) for n in children for c in n])

    nodes = [n + [[0] * feature_len] * (max_nodes - len(n)) for n in nodes]
    # pad batches so that every batch has the same number of nodes
    children = [n + ([[]] * (max_children - len(n))) for n in children]
    # pad every child sample so every node has the same number of children
    children = [[c + [0] * (child_len - len(c)) for c in sample] for sample in children]

    return nodes, children, meta, labels

def _onehot(i, total):
    return [1.0 if j == i else 0.0 for j in range(total)]
