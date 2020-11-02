"""Parse nodes from a given data source."""

import ijson.backends.yajl2_c as ijson
import sys
import ast,json,pprint,itertools
import cPickle as pickle
from collections import defaultdict

import samplerjson.jsontree as jsontree
pp=pprint.PrettyPrinter(indent=4)

def parse(args):
    if args.ijson:
        """Parse nodes with the given args."""
        print ('Loading json file')

        f = open(args.infile, 'rb')
        data_source = ijson.items(f,'item')

        node_counts = defaultdict(int)
        samples = []
        has_capacity = lambda x: args.per_node < 0 or node_counts[x] < args.per_node
        can_add_more = lambda: args.limit < 0 or len(samples) < args.limit
        print ('Json load finished')

        fc=0
        c=0
        file_handler = open(args.outfile, 'wb')
        file_handler.write("[\t")

        for item in data_source:
            root = None
            samples = []
            if 'tree' in item.keys() and isinstance(item['tree'],list):
                root = item['tree']
            else:
                root = item
            if not root:
                continue
            new_samples = [
                {
                    'node': "Module",
                    'nodeType': "Module",
                    'parent': None,
                    'children': [_name(x) for x in jsontree.JsonTree.iter_child_nodes(root)]
    #                'children': [_name(x) for x in ast.iter_child_nodes(root)]
                }
            ]
            gen_samples = lambda x,p: new_samples.extend(_create_samples(x,p))
            _traverse_tree(_name(new_samples[0]), root, gen_samples)
            for sample in new_samples:
                if has_capacity(sample['node']):
                    samples.append(sample)
                    node_counts[sample['node']] += 1
                if not can_add_more:
                    break
            if not can_add_more:
                break
            for sample in samples:
#                print (sample)
                if c:
                    file_handler.write(",\n"+json.dumps(sample, indent=2))
                else:
                    file_handler.write(json.dumps(sample, indent=2))
                c+=1
#            print(fc, len(new_samples), item['metadata']['name'])
            fc+=1
        print ('dumping sample')

        file_handler.write("]")
        file_handler.close()

        print('Sampled node counts:')
        print(node_counts)
        print('Total: %d' % sum(node_counts.values()))

        return


    """Parse nodes with the given args."""
    print ('Loading json file')

    with open(args.infile, 'rb') as file_handler:
        data_source = json.load(file_handler)

    print ('Json load finished')

    node_counts = defaultdict(int)
    samples = []
    has_capacity = lambda x: args.per_node < 0 or node_counts[x] < args.per_node
    can_add_more = lambda: args.limit < 0 or len(samples) < args.limit

#    print(len(data_source))
    for item in data_source:
        root = None
        if 'tree' in item.keys() and isinstance(item['tree'],list):
            root = item['tree']
        else:
            root = item
        if not root:
            continue
        new_samples = [
            {
                'node': "Module",
                'nodeType': "Module",
                'parent': None,
                'children': [_name(x) for x in jsontree.JsonTree.iter_child_nodes(root)]
#                'children': [_name(x) for x in ast.iter_child_nodes(root)]
            }
        ]
        gen_samples = lambda x,p: new_samples.extend(_create_samples(x,p))
        _traverse_tree(_name(new_samples[0]), root, gen_samples)
        for sample in new_samples:
            if has_capacity(sample['node']):
                samples.append(sample)
                node_counts[sample['node']] += 1
            if not can_add_more:
                break
        if not can_add_more:
            break
    print ('dumping sample')

    with open(args.outfile, 'wb') as file_handler:
        pickle.dump(samples, file_handler)
        file_handler.close()

    print('Sampled node counts:')
    print(node_counts)
    print('Total: %d' % sum(node_counts.values()))

def _create_samples(node,parentname):
    """Convert a node's children into a sample points."""
    samples = []
#    for child in ast.iter_child_nodes(node):
#    print('s',_name(node),parentname)
    for child in jsontree.JsonTree.iter_child_nodes(node):
#        print("***A2***")
#        print(_name(child),parentname)
        if isinstance(node,dict):
            parentname=_name(node)
        sample = {
            "node": _name(child),
            "parent": parentname,
#                'children': []
            "children": [_name(x) for x in jsontree.JsonTree.iter_child_nodes(child)]
#            "children": [_name(x) for x in ast.iter_child_nodes(child)]
        }
#        if isinstance(child, list):
#            sample["children"]=[_name(x) for x in child]
#        elif isinstance(child, dict):
#            sample["children"]=[_name(x) for x in child.values()]
#        print(node)
#        print(sample["children"])
#        print("***B2***")
        samples.append(sample)
    return samples

def _traverse_tree(parentname, tree, callback):
    """Traverse a tree and execute the callback on every node."""
#    print("TRAVERSE")
#    pp.pprint(tree)
#    print("================================")
#    it = iter(tree)
#    queue = list(zip([parentname],tree))
    queue = list(itertools.izip_longest([parentname],[tree],fillvalue=parentname))

#    pp.pprint(queue)

#    queue = [tree]
    while queue:
#        parent_name = parentname
#        current_node = queue.pop(0)
        current = queue.pop(0)
        parent_name = current[0]
        current_node = current[1]
#        print("***A3***")
#        print(current_node)
#        if isinstance(current_node, dict):
#            print('*',parent_name,_name(current_node))
#        else:
#            print('*',parent_name,current_node)

        nextparentname=parent_name
        if isinstance(current_node, dict):
#            print('x.')
            nextparentname=_name(current_node)
#        current_node = queue.pop(0)
#        print('x',nextparentname)
        children = list(jsontree.JsonTree.iter_child_nodes(current_node))
        if len(children) > 0:
            children_list = list(itertools.izip_longest([nextparentname],children,fillvalue=nextparentname))
        else:
            children_list = []
#        pp.pprint(children_list)
#        children = list(ast.iter_child_nodes(current_node))
#        print(children)
#        print("***B3***")
        queue.extend(children_list)
#        queue.extend(children)
#        if isinstance(current_node, dict):
#            print('*.',parent_name,_name(current_node))
#        else:
#            print('*.',parent_name,current_node)
        callback(current_node,parent_name)
#        callback(current_node, parent)

def _name(node):
    """Get the name of a node."""
    return node["nodeType"]
