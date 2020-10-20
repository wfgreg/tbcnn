"""File for defining commands for the sampler."""

import argparse
import logging

import samplerjson.trees as trees
import samplerjson.nodes as nodes

def main():

    parser = argparse.ArgumentParser(
        description="Sample trees or nodes from a crawler file.",
    )
    subparsers = parser.add_subparsers(help='sub-command help')

    tree_parser = subparsers.add_parser(
        'trees', help='Sample trees from a data source.'
    )
    tree_parser.add_argument('--infile', type=str, help='Data file to sample from')
    tree_parser.add_argument('--outfile', type=str, help='File to store samples in')
    tree_parser.add_argument('--usecv', action='store_true', help='Use cross-validation data (use 15 default if given without cv)')
    tree_parser.add_argument('--cv', default=0, type=int, help='Percent to save as cross-validation data (turns on usecv by default)')
    tree_parser.add_argument('--test', default=30, type=int, help='Percent to save as test data')
    tree_parser.add_argument(
        '--label-key', type=str, default='label',
        help='Change which key to use for the label'
    )
    tree_parser.add_argument(
        '--maxsize', type=int, default=10000,
        help='Ignore trees with more than --maxsize nodes'
    )
    tree_parser.add_argument(
        '--minsize', type=int, default=100,
        help='Ignore trees with less than --minsize nodes'
    )
    tree_parser.set_defaults(func=trees.parse)

    node_parser = subparsers.add_parser(
        'nodes', help='Sample nodes from a data source.'
    )
    node_parser.add_argument('--infile', type=str, help='Data file to sample from')
    node_parser.add_argument('--outfile', type=str, help='File to store samples in')
    node_parser.add_argument(
        '--per-node', type=int, default=-1,
        help='Sample up to a maxmimum number for each node type'
    )
    node_parser.add_argument(
        '--limit', type=int, default=-1,
        help='Maximum number of samples to store.'
    )
    node_parser.set_defaults(func=nodes.parse)

    args = parser.parse_args()

    if 'cv' in args:
        if(args.cv > 0):
            args.usecv = True
        elif args.usecv:
            args.cv = 15

    args.func(args)
