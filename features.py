'''
Created on Mar 3, 2015

@author: Aaron Levine

'''

def token_match(pair):
    """do tokens match each other?"""
    x, y = pair
    return x.token == y.token

def extended_token_match(pair):
    """how many of modifiers / det match each other?"""
    # score = 0
    # for i in range(len(x.offset)):
        # if x.sent[x.offset - 1].pos == x.sent[y.offset - 1].pos:
            # if x.sent[x.offset - 1].token == x.sent[y.offset - 1].token: 
            # score += 1    
        # else:
            #break
    #return score
    return

def entity_type_match(pair):
    """ are the BIO entity types the same? """
    # return x.type == y.type
    return


def token_inbetween(pair, tokens):
    # if same sent offset:
        # for token in sent[x.offset: y.offset]:
            # if token in tokens:
                # return True
    return False

def appositives(pair):
    '''check for comma between items'''
    return token_inbetween(pair, {','})
    
def predicate_nominative(pair):
    '''check for 'is' / 'are' between items'''
    return token_inbetween(pair, {'is', 'are', 'was', 'were'})

def relative_pronoun(pair):
    '''check for 'which' / 'who' between items'''
    return token_inbetween(pair, {'which', 'who'})

def acronym(pair):
    ''' check if fist letters of one matches all letters in others:
    [Agence France Presse] ~ [AFP] '''
    
    #if x multiple tokens:
        # letters_x = [tok[0] for tok in x.tokens]
        # letters_y = [l for l in y.tokens if l not in {' ', '.'}
    #return letters_x == letters_y

def role_appositives(pair):
    '''check for role noun and proper noun next to each other'''
    # return if y is proper noun and x is noun
    return

def demonyn(pair):
    ''' number of matching letters? '''
    return






