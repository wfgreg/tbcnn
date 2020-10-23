"""Helper functions for sampling in ast2vec."""

import ast
import ijson.backends.yajl2_c as ijson

from vectorizer.node_map import NODE_MAP
from vectorizer.node_map_php import PHP_NODE_MAP

def batch_samples(args, samplefile, batch_size):
    """Batch samples and return batches in a generator."""
    batch = ([], [])
    count = 0
    index_of = None
    if not args.php:
        index_of = lambda x: NODE_MAP[x]
    else:
        index_of = lambda x: PHP_NODE_MAP[x]
    f = open(args.infile, 'rb')
    samples = ijson.items(f,'item')
    for sample in samples:
        if sample['parent'] is not None:
            batch[0].append(index_of(sample['node']))
            batch[1].append(index_of(sample['parent']))
            count += 1
            if count >= batch_size:
                yield batch
                batch, count = ([], []), 0
