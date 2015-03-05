'''
Created on Mar 3, 2015

@author: Aaron Levine

'''

# HELPER FUNCTIONS
def load_tokens(pair, start_a, end_a, start_b, end_b):
    """ helper function to grab set of tokens from given sentences """
    mention_a, mention_b = pair.mentions
    sentences = list(mention_a.document.get_sentences())
    sentence_a = sentences[mention_a.sentence_index]
    tokens_a = sentence_a[start_a:end_a]
    sentence_b = sentences[mention_b.sentence_index]
    tokens_b = sentence_b[start_b:end_b]
    return tokens_a, tokens_b


# FEATURE FUNCTIONS
def pos_match(pair):
    """ how many parts of speech match? -potential backoff feature"""
    mention_a, mention_b = pair.mentions
    tokens_a, tokens_b = load_tokens(pair, 
                                     mention_a.start, mention_a.end, 
                                     mention_b.start, mention_b.end)
    pos_a = [tok.pos for tok in tokens_a]
    pos_b = {tok.pos for tok in tokens_b}
    return len([pos for pos in pos_a if pos in pos_b])

def simple_pos_match(pair):
    """ how many parts of speech match? -potential backoff feature"""
    mention_a, mention_b = pair.mentions
    tokens_a, tokens_b = load_tokens(pair, 
                                     mention_a.start, mention_a.end, 
                                     mention_b.start, mention_b.end)
    pos_a = [tok.pos[0] for tok in tokens_a]
    pos_b = {tok.pos[0] for tok in tokens_b}
    return len([pos for pos in pos_a if pos in pos_b])

def string_match(pair):
    """do strings match each other?"""
    mention_a, mention_b = pair.mentions
    return mention_a.text == mention_b.text

def token_match(pair):
    """do tokens match each other?"""
    mention_a, mention_b = pair.mentions
    tokens_a =  mention_a.text.split('_')
    tokens_b =  mention_b.text.split('_')
    return len([tok for tok in tokens_a if tok in tokens_b])

def entity_type_match(pair):
    """do strings match each other?"""
    mention_a, mention_b = pair.mentions
    return mention_a.entity_type == mention_b.entity_type

def acronym_first(pair):
    ''' check if fist letters of one matches all letters in others:
    [Agence France Presse] ~ [AFP] '''
    mention_a, mention_b = pair.mentions
    if (mention_a.start + 1) != mention_a.end\
    and (mention_b.start + 1) != mention_b.end:
        letters_a = [tok[0] for tok in mention_a.text.split('_')]
        letters_b = [l for l in mention_b.text if l not in {' ', '.', '_'}]
        return letters_a == letters_b
    else:
        return False

def token_inbetween(pair, targets=['is']):
    mention_a, mention_b = pair.mentions
    if mention_a.sentence_index == mention_b.sentence_index:
        inbetween_tokens, _ = load_tokens(pair, 
                                          mention_a.end, mention_b.end, 
                                          0, 0)
    
    return len([tok for tok in targets if tok in inbetween_tokens])

def token_inbetween_binary(pair, targets=['is']):
    value = token_inbetween(pair, targets)
    return bool(value)

def appositives(pair):
    '''check for comma between items'''
    return token_inbetween(pair, {','})
    
def predicate_nominative(pair):
    '''check for 'is' / 'are' between items'''
    return token_inbetween(pair, {'is', 'are', 'was', 'were'})

def relative_pronoun(pair):
    '''check for 'which' / 'who' between items'''
    return token_inbetween(pair, {'which', 'who'})

# def role_appositives(pair):
#     '''check for role noun and proper noun next to each other'''
#     # return if y is proper noun and x is noun
#     return
# 
# def demonyn(pair):
#     ''' number of matching letters? '''
#     return
# 
# def extended_token_match(pair):
#     """how many of modifiers / det match each other?"""
#     return

