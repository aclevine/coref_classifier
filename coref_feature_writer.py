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
    
    def get_weka_header(self, features, relation='coref'):
        """Write the WEKA feature format boilerplate."""
        header = ['@relation {}'.format(relation)]
        for feature in features:
            header += ["@attribute {} REAL".format(feature.__name__)]
        header += ["@attribute class {'yes', 'no'}"]
        header += ['@data']
        return '\n'.join(header)
    
    def write_features(self, seperator=',', train=True):
        """ extract features from MentionPair objects,
        write to training or test file """
        if train:
            output_path = self.output_name + '.train.arff'
        else:
            output_path = self.output_name + '.test.arff'
        # LOAD
        corpus = Corpus(self.index_path, data_dir='data')
        # WRITE
        with open(output_path, 'w+') as fo:
            fo.write(self.get_weka_header(self.features) + '\n')
            for line, pair in corpus.mention_pairs.iteritems():
                # FEATURES
                for feat_func in self.features:
                    feat = feat_func(pair)
                    # feat = codebook(feat)
                    fo.write(str(float(feat)))
                    fo.write(seperator)
                # LABEL
                fo.write(pair.label)
                fo.write('\n')

if __name__ == "__main__":
    
    features = [
                # FEATURES HERE
                string_match,
                string_match_lower,
                token_match,
                entity_type_match,
                pos_match,
                number_match,
                simple_pos_match,
                appositives,
                predicate_nominative,
                relative_pronoun,
                token_inbetween,
                extend_pos_match,
                extend_simple_pos_match,
                same_sentence,
                substring_match,
                acronym,
                sentence_distance,
                simple_token_distance,
                extended_token_distance
               ]

    output_name = "features/3-10-15"

    # train data
    extractor = FeatWriter(features, 'coref-trainset.gold',
                           output_name=output_name)
    extractor.write_features()
     
    # dev data
    extractor = FeatWriter(features, 'coref-devset.gold',
                           output_name=output_name)
    extractor.write_features(train=False)
     
    # test data
    extractor = FeatWriter(features, 'coref-testset.gold',
                           output_name="features/final_fixed")
    extractor.write_features(train=False)
