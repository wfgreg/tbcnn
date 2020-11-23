"""Parse trees from a data source."""

import ijson.backends.yajl2_c as ijson
import sys
import ast,astpretty,pprint
import astunparse
import ast,json,pprint,itertools
import pickle
import random
from collections import defaultdict

import subprocess

import samplerjson.jsontree as jsontree
pp=pprint.PrettyPrinter(indent=4)

def parse(args):
    if args.ijson:
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

        f1 = open("/tmp/cv.txt", 'w')
        f2 = open("/tmp/test.txt", 'w')
        f3 = open("/tmp/train.txt", 'w')

        for item in data_source:
            root = item['tree']
            label = item['metadata'][args.label_key]
            sample, size = _traverse_tree(root)

            if size > args.maxsize or size < args.minsize:
                continue

            roll = random.randint(0, 100)
            if args.usecv and roll < args.cv:
                file_handler=f1
                cv_counts[label] += 1
            elif args.usecv and roll < (args.cv + args.test):
                file_handler=f2
                test_counts[label] += 1
            elif not args.usecv and roll < args.test:
                file_handler=f2
                test_counts[label] += 1
            else:
                file_handler=f3
                train_counts[label] += 1
            datum = {'tree': sample, 'label': label, 'meta': json.loads(json.dumps(item['metadata']))}
            file_handler.write(json.dumps(datum)+",\n")
        f1.close()
        f2.close()
        f3.close()

        # implement shuffling algorithm?
        for filelabel in ['train','test','cv']:
            tmpfile="/tmp/"+filelabel
            fout = open(tmpfile+".shuffled.txt","w")
            with open(tmpfile+".txt") as inhandle:
                p = subprocess.Popen("../terashuf/terashuf",stdin=inhandle,stdout=fout)
                [output,error] = p.communicate()
                rc = p.wait()
            print(tmpfile+".shuffled.txt")

        f1o = open(args.outfile+".cv.json", 'w')
        f2o = open(args.outfile+".test.json", 'w')
        f3o = open(args.outfile+".train.json", 'w')
        out_dict = {'cv':f1o,'test':f2o,'train':f3o}
        f1o.write('[\n')
        f2o.write('[\n')
        f3o.write('[\n')
        labels = list(set(itertools.chain(cv_counts.keys(),train_counts.keys(),test_counts.keys())))
        print(labels)
        print('Dumping sample')
        with open(args.outfile, 'w') as out_handler:
            out_handler.write('(\t[\n')
            for filelabel in ['train','test','cv']:
                c=0
                tmpfile="/tmp/"+filelabel+'.shuffled.txt'
                with open(tmpfile, 'r') as in_handler:
                    for line in in_handler:
                        linestr=line.rstrip().rstrip(',')
                        if c:
                            out_handler.write(",\n"+linestr)
                            out_dict[filelabel].write(",\n"+linestr)
                        else:
                            out_handler.write(linestr)
                            out_dict[filelabel].write(linestr)
                        c+=1
                out_handler.write('\n],\t[\n')
                out_dict[filelabel].write('\n]')
                out_dict[filelabel].close()
            out_handler.write('],\n')
            out_handler.write(json.dumps(labels))
            out_handler.write('\n)')

        f4o = open(args.outfile+".labels.json", 'w')
        f4o.write(json.dumps(labels))
        f4o.close();

        print('dump finished')
        print('Sampled tree counts: ')
        print('Cross-Validation:', cv_counts)
        print('Training:', train_counts)
        print('Testing:', test_counts)

        return



    """Parse trees with the given arguments."""
    print ('Loading json file')

    sys.setrecursionlimit(1000000)
    with open(args.infile, 'rb') as file_handler:
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
        elif args.usecv and roll < (args.cv + args.test):
            test_samples.append(datum)
            test_counts[label] += 1
        elif not args.usecv and roll < args.test:
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
        "node": "Module",
        "children": []
    }
    queue_json = [root_json]
    while queue:
        current_node = queue.pop(0)
        num_nodes += 1
        current_node_json = queue_json.pop(0)


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
    return node["nodeType"]
