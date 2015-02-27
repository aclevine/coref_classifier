'''
Created on Feb 27, 2015

@author: Aaron Levine
'''

import re
import os

def gen_clean_files(pos_path):
    # make folder
    clean_path = re.sub('postagged-files', 'clean-files', pos_path)
    if not os.path.exists(clean_path):
        os.makedirs(clean_path)
    # make files
    for pos_file in os.listdir(pos_path):
        clean_file = re.sub('\.pos', '', pos_file)
        with open(os.path.join(clean_path, clean_file), 'w+') as fw:
            with open( os.path.join(pos_path, pos_file), 'r') as fr:
                for line in fr:
                    if line != '\n':
                        tok_pos = [t_p.split('_', 1) for t_p in line.split()]
                        line = '<s> {} </s>'.format(' '.join([t for t, _ in tok_pos]))
                        fw.write(line + '\n')

def gen_syntax_files(clean_path):
    # make folder
    syn_path = re.sub('clean-files', 'syntax-files', clean_path)
    if not os.path.exists(syn_path):
        os.makedirs(syn_path)

    # make files
    


if __name__ == "__main__":
    
    gen_clean_files('../data/postagged-files')