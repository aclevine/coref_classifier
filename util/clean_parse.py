'''
Created on Feb 27, 2015

@author: Aaron Levine
'''

import re, os, subprocess

def gen_clean_files(pos_path):
    # make folder
    clean_path = re.sub('postagged-files', 'clean-files', pos_path)
    if not os.path.exists(clean_path):
        os.makedirs(clean_path)
    # make files
    for pos_file in os.listdir(pos_path):
        clean_file = re.sub('\.pos', '', pos_file)
        with open(os.path.join(clean_path, clean_file), 'w+') as fw:
            with open( os.path.join(pos_path, pos_file), 'rb') as fr:
                for line in filter(None,fr.read().split('\n')):
                    if bool(re.match('^\s*$',line)):
                        fw.write('{}\n'.format("This is not a sentence ."))
                    else:
                        tok_pos = [split_token(t_p) for t_p in line.split()]
                        line = '{}'.format(' '.join([t for t, _ in tok_pos]))
                        fw.write(line + '\n')


def split_token(token_string):
    if token_string.startswith('__'):
        out = (token_string[0],token_string[2:])
    else:
        out = tuple(token_string.split('_', 1 ))
    return out


if __name__ == "__main__":
        
    gen_clean_files('../data/postagged-files')