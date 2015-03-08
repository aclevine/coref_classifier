import os
from collections import defaultdict
from nltk import Tree


class Token(object):
    """A token is a tuple-like object with four attributes:
        index : an integer representing the index of the token in the sentence
        text  : a string representation of the token
        pos   : a string representing the POS tag of the token"""
    def __init__(self, index, text, pos):
        self.index = index
        self.text = text
        self.pos = pos
    
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self._args())
    
    def _args(self):
        """Returns an ordered list of arguments for string representation."""
        args = self.index, self.text, self.pos
        return ', '.join(map(repr, args))

class Sentence(tuple):
    """A tuple wrapper class for working with sequences of Tokens."""
    def __init__(self, tokens=tuple()):
        if not all(isinstance(item, Token) for item in tokens):
            raise TypeError, 'expected a sequence of Tokens'
    
    def __add__(self, other):
        if not isinstance(other, (Sentence, Token)):
            raise TypeError, 'can only concatenate Sentence or Token'
        if isinstance(other, Token):
            return self + Sentence((other,))
        return Sentence(super(Sentence, self).__add__(other))
    
    def __iadd__(self, other):
        if not isinstance(other, (Sentence, Token)):
            raise TypeError, 'can only concatenate Sentence or Token'
        if isinstance(other, Token):
            return self + Sentence((other,))
        return self + other
    
    def __repr__(self):
        return '<{} with {} tokens>'.format(self.__class__.__name__, len(self))
    
    def __str__(self):
        return ' '.join('/'.join([t.text.encode('utf-8'), t.pos]) for t in self)

class MentionPair(object):
    """A tuple-like object for working with coreference candidates:
        document : the document the MentionPair occurs in
        mention_a : the first Mention in the pair
        mention_b : the second Mention in the pair
        label : a label indicating whether the pair of mentions
                are coreferential or not (defualt is None, but may be 'yes'
                or 'no')"""
    def __init__(self, document, mention_a, mention_b, label=None):
        self.document = document
        self.mentions = (mention_a, mention_b)
        self.label = label
    
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self._args())
    
    def _args(self):
        """Returns an ordered list of arguments for string representation."""
        args = (
            self.document.name,
            self.mentions[0],
            self.mentions[1],
            self.label
        )
        return ', '.join(map(repr, args))

class Mention(object):
    """A class for working with individual co-reference mention candidates:
        document : the document that the mention occurs in
        sentence_index : integer indicating index of the sentence that
                         the Mention occurs in
        position_index : a pair of integers indicating the position of
                         the Mention within the sentence it occurs in
        text : a string representation of the token
        entity_type : string representing the ACE entity type of the mention"""
    def __init__(
        self,
        document,
        sentence_index,
        start,
        end,
        entity_type,
        text
    ):
        self.document = document
        self.sentence_index = int(sentence_index)
        self.start = int(start)
        self.end = int(end)
        self.entity_type = entity_type
        self.text = text
    
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self._args())
    
    def _args(self):
        """Returns an ordered list of arguments for string representation."""
        args = (
            self.sentence_index,
            self.start,
            self.end,
            self.entity_type,
            self.text
        )
        return ', '.join(map(repr, args))

class Document(object):
    """A class representing a document."""
    def __init__(
        self,
        name,
        data_dir='data',
        pos_data_dir='postagged-files',
        tree_data_dir='syntax-files'
    ):
        self.name = name
        self.data_dir = data_dir
        self.pos_data_dir = os.path.join(self.data_dir, pos_data_dir)
        self.tree_data_dir = os.path.join(self.data_dir, tree_data_dir)
        self.sentences = self.get_sentences()
        self.trees = self.get_trees()
    
    def __len__(self):
        return len(list(self.get_sentences()))
    
    def __repr__(self):
        return '<{}:{} with {} sentences>'.format(
            self.__class__.__name__,
            self.name,
            len(self)
        )
    
    def get_sentences(self):
        """Generates Sentences (list of pos / text Token objects) for the document."""
        sentence_data_path = os.path.join(
            self.pos_data_dir, self.name + '.raw.pos'
        )
        with open(sentence_data_path, 'rb') as file:
            lines = filter(None, file.read().split('\n'))
        for line in lines:
            sentence = Sentence()
            for i, word_pos in enumerate(line.strip().split(' ')):
                # Need to handle odd null tokens
                if word_pos.startswith('__'):
                    word, pos = word_pos[0], word_pos[2:]
                else:
                    try:
                        word, pos = word_pos.split('_')
                    except ValueError:
                        print self.name
                        print word_pos
                        print line
                        break
                sentence += Token(i, word, pos)
            yield sentence
    
    def get_trees(self):
        """Generates Tree objects for each sentence in the document."""
        tree_data_path = os.path.join(
            self.tree_data_dir, self.name + '.raw.syn'
        )
        with open(tree_data_path, 'rb') as file:
            lines = filter(None, file.read().split('\n'))
        for line in lines:
            yield Tree.fromstring(line)

class Corpus(object):
    """A class for working with collections of documents."""
    def __init__(
        self,
        coref_data,
        data_dir='data',
        pos_data_dir='postagged-files',
        tree_data_dir='syntax-files',
        verbose=0
    ):
        self.data_dir = data_dir
        self.coref_data = os.path.join(self.data_dir, coref_data)
        self.pos_data_dir = os.path.join(self.data_dir, pos_data_dir)
        self.tree_data_dir = os.path.join(self.data_dir, tree_data_dir)
        self.mention_pairs = defaultdict(list)
        self.process_documents(verbose)
    
    def process_documents(self, verbose=0):
        """Populates the document list and the mention pairs dictionary."""
        with open(self.coref_data, 'rb') as file:
            lines = filter(None, file.read().split('\n'))
        self.documents = set()
        current_document = None
        line_num = 1
        for line in lines:
            items = line.split(' ')
            document = Document(items[0])
            if current_document != document.name:
                current_document = document.name
                self.documents.add(document)
                if verbose:
                    print 'Processing {} ...'.format(current_document)
            a = [document] + items[1:6]
            b = [document] + items[6:11]
            if len(items) == 12:
                label = items[-1]
            else:
                label = None
            try:
                mention_a = Mention(*a)
                mention_b = Mention(*b)
            except TypeError:
                print items
                print a
                print b
                break
            pair = MentionPair(document, mention_a, mention_b, label)
            self.mention_pairs[line_num] = pair
            line_num += 1
        self.documents = sorted(self.documents)
        if verbose:
            print 'Processed {n} documents in total'.format(
                                                            n=len(self.documents)
                                                            )

if __name__ == '__main__':
    
    corpus = Corpus('coref-trainset.gold', data_dir='data', verbose=1)
    doc_index = 0
    sentence_index = 10
    sample_doc = corpus.documents[doc_index]
    sample_sentence = list(sample_doc.sentences)[sentence_index]
    sample_tree = list(sample_doc.trees)[sentence_index]
    print """Samples from {doc} :
    sentence {i} : {sentence}
    tree {i} : {tree}""".format(
        doc=sample_doc,
        i=sentence_index,
        sentence=sample_sentence,
        tree=sample_tree
    )
    print """Mention pairs from {doc} :""".format(
        doc=sample_doc
    )
    for pair in corpus.mention_pairs[sample_doc.name]:
        print pair