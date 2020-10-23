"""Parse trees from a data source."""

import ijson.backends.yajl2_c as ijson
import sys
import ast,astpretty,pprint
import astunparse
import ast,json,pprint,itertools
import pickle
import random
from collections import defaultdict

import samplerjson.jsontree as jsontree
pp=pprint.PrettyPrinter(indent=4)

def parse(args):
    if not args.picklize:
        """Parse trees with the given arguments."""
        print ('Loading json file')

        sys.setrecursionlimit(1000000)
        f = open(args.infile, 'rb')
        data_source = ijson.items(f,'item')

        print('Json file load finished')

        train_samples = []
        cv_samples = []
        test_samples = []

        train_counts = defaultdict(int)
        cv_counts = defaultdict(int)
        test_counts = defaultdict(int)

        f1 = open("/tmp/cv.txt", 'wb')
        f2 = open("/tmp/test.txt", 'wb')
        f3 = open("/tmp/train.txt", 'wb')

        c=0
        for item in data_source:
            root = item['tree']
            label = item['metadata'][args.label_key]
            sample, size = _traverse_tree(root)

            roll = random.randint(0, 100)
            if args.usecv and roll < args.cv:
                file_handler=f1
                cv_counts[label] += 1
            elif roll < args.test:
                file_handler=f2
                test_counts[label] += 1
            else:
                file_handler=f3
                train_counts[label] += 1
            file_handler.write(json.dumps(sample)+",\n")
            c+=1
        f1.close()
        f2.close()
        f3.close()

        # implement shuffling algorithm?


        labels = list(set(cv_counts.keys() + train_counts.keys() + test_counts.keys()))
        print(labels)
        print('Dumping sample')
        with open(args.outfile, 'wb') as out_handler:
            out_handler.write('(\t[\n')
            for filelabel in ['train','test','cv']:
                c=0
                with open('/tmp/'+filelabel+'.txt', 'r') as in_handler:
                    for line in in_handler:
                        if c:
                            out_handler.write(",\n"+line.rstrip().rstrip(','))
                        else:
                            out_handler.write(line.rstrip().rstrip(','))
                        c+=1
                out_handler.write('\n],\t[\n')
            out_handler.write('],\n')
            out_handler.write(json.dumps(labels))
            out_handler.write('\n)')


        print('dump finished')
        print('Sampled tree counts: ')
        print('Cross-Validation:', cv_counts)
        print('Training:', train_counts)
        print('Testing:', test_counts)

    if not args.picklize:
        return
    """Parse trees with the given arguments."""
    print ('Loading json file')

    sys.setrecursionlimit(1000000)
    with open(args.infile, 'rb') as file_handler:
#        data_source = pickle.load(file_handler)
        data_source = json.load(file_handler)

    print('Json file load finished')

    train_samples = []
    cv_samples = []
    test_samples = []

    train_counts = defaultdict(int)
    cv_counts = defaultdict(int)
    test_counts = defaultdict(int)

    for item in data_source:
        root = item['tree']
        label = item['metadata'][args.label_key]
        sample, size = _traverse_tree(root)

        if size > args.maxsize or size < args.minsize:
            continue

        roll = random.randint(0, 100)

        datum = {'tree': sample, 'label': label, 'meta': json.loads(json.dumps(item['metadata']))}

        if args.usecv and roll < args.cv:
            cv_samples.append(datum)
            cv_counts[label] += 1
        elif roll < args.test:
            test_samples.append(datum)
            test_counts[label] += 1
        else:
            train_samples.append(datum)
            train_counts[label] += 1

    random.shuffle(cv_samples)
    random.shuffle(train_samples)
    random.shuffle(test_samples)
    # create a list of unique labels in the data
    labels = list(set(cv_counts.keys() + train_counts.keys() + test_counts.keys()))
    print('Dumping sample')
    with open(args.outfile, 'wb') as file_handler:
        pickle.dump((train_samples, test_samples, cv_samples, labels), file_handler)
        file_handler.close()
    print('dump finished')
    print('Sampled tree counts: ')
    print('Cross-Validation:', cv_counts)
    print('Training:', train_counts)
    print('Testing:', test_counts)

def _traverse_tree(root):
    num_nodes = 1
    queue = [root]
    root_json = {
#        "node": _name(root),
        "node": "Module",
        "children": []
    }
    queue_json = [root_json]
    while queue:
        current_node = queue.pop(0)
        num_nodes += 1
        current_node_json = queue_json.pop(0)


#        children = list(ast.iter_child_nodes(current_node))
        children = list(jsontree.JsonTree.iter_child_nodes(current_node))
        queue.extend(children)
        for child in children:
            child_json = {
                "node": _name(child),
                "children": []
            }
            current_node_json['children'].append(child_json)
            queue_json.append(child_json)

    return root_json, num_nodes

def _name(node):
#    return type(node).__name__
    return node["nodeType"]
