"""File for defining commands for the classifier."""

import argparse
import logging
import re

import classifier.tbcnn.train_ijson as tbcnn_train_ijson
import classifier.tbcnn.test_ijson as tbcnn_test_ijson
import classifier.tbcnn.predict_ijson as tbcnn_predict_ijson

import classifier.tbcnn.train as tbcnn_train
import classifier.tbcnn.test as tbcnn_test
import classifier.tbcnn.predict as tbcnn_predict

def main():
    """Commands to train and test classifiers."""

    parser = argparse.ArgumentParser(
        description="Train and test classifiers on datasets.""",
    )
    subparsers = parser.add_subparsers(help='sub-command help')

    train_parser = subparsers.add_parser(
        'train', help='Train a model to classify'
    )
    train_parser.add_argument('model', type=str, help='Model to train: options are "tbcnn"')
    train_parser.add_argument('--infile', type=str, help='Data file to sample from')
    train_parser.add_argument('--logdir', type=str, help='File to store logs in')
    train_parser.add_argument(
        '--embedfile', type=str, help='Learned vector embeddings from the vectorizer'
    )
    train_parser.set_defaults(action='train')

    test_parser = subparsers.add_parser(
        'test', help='Test a model'
    )
    test_parser.add_argument('model', type=str, help='Model to train: options are "tbcnn"')
    test_parser.add_argument('--infile', type=str, help='Data file to sample from')
    test_parser.add_argument('--logdir', type=str, help='File to store logs in')
    test_parser.add_argument(
        '--embedfile', type=str, help='Learned vector embeddings from the vectorizer'
    )
    test_parser.set_defaults(action='test')

    predict_parser = subparsers.add_parser(
        'predict', help='Predict with a model'
    )
    predict_parser.add_argument('model', type=str, help='Model to use: options are "tbcnn"')
#    predict_parser.add_argument('--labels', help='Data file to sample from')
    predict_parser.add_argument('--infile', type=str, help='Data file to sample from')
    predict_parser.add_argument('--logdir', type=str, help='File to store logs in')
    predict_parser.add_argument(
        '--embedfile', type=str, help='Learned vector embeddings from the vectorizer'
    )
    predict_parser.set_defaults(action='predict')


    args = parser.parse_args()

#    if args.action == 'cv':
#        if args.model == 'tbcnn':
#            tbcnn_train.test_model(args.logdir, args.infile, args.embedfile)

    if args.action == 'train':
        if args.model == 'tbcnn':
            if re.match('.*\.pkl',args.infile):
                tbcnn_train.train_model(args.logdir, args.infile, args.embedfile)
            if re.match('.*\.train\.json',args.infile):
                tbcnn_train_ijson.train_model(args, args.logdir, args.infile, args.embedfile)

    if args.action == 'test':
        if args.model == 'tbcnn':
            if re.match('.*\.pkl',args.infile):
                tbcnn_test.test_model(args.logdir, args.infile, args.embedfile)
            if re.match('.*\.test\.json',args.infile):
                tbcnn_test_ijson.test_model(args, args.logdir, args.infile, args.embedfile)

    if args.action == 'predict':
        if args.model == 'tbcnn':
            if re.match('.*\.pkl',args.infile):
                tbcnn_predict.predict_model(args, args.logdir, args.infile, args.embedfile)
            if re.match('.*\.test\.json',args.infile):
                tbcnn_predict_ijson.predict_model(args, args.logdir, args.infile, args.embedfile)
