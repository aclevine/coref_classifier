'''
Created on Mar 4, 2015

@author: Aaron Levine
'''
from coref_corpus import *
from features import *

class FeatWriter(object):
     
    def __init__(self, features, index_path, output_name='test'):
        self.index_path = index_path
        self.features = features
        self.output_name = output_name

    def write_features(self, seperator=',', train=True):
        """ extract features from MentionPair objects,
        write to training or test file """
        if train:
            output_path = self.output_name + '.train'
        else:
            output_path = self.output_name + '.test'
        # LOAD
        corpus = Corpus(self.index_path, data_dir='data')
        # WRITE
        with open(output_path, 'w+') as fo:
            for doc, pair_list in corpus.mention_pairs.iteritems():
                for pair in pair_list:
                    # FEATURES
                    for feat_func in self.features:
                        feat = feat_func(pair)
                        # feat = codebook(feat)
                        fo.write(str(feat))
                        fo.write(seperator)
                    if train:
                        # LABEL
                        fo.write(pair.label)
                    fo.write('\n')


if __name__ == "__main__":
    
    features = [
                # FEATURES HERE
                pos_match,
                simple_pos_match
                ]
    
    extractor = FeatWriter(features, 'coref-trainset.gold')
    extractor.write_features()

        