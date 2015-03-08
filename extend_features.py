'''
Created on Mar 6, 2015

@author: Aaron Levine

Function for taking an new .arff feature vector document,
and appending its data to the end of another feature vector document
run on the same dataset.

FILES MUST HAVE BEEN RUN ON THE SAME DATASET!
'''

def extend_features(old_path, new_path, out_path):
    with open(out_path, "w+") as fo:
        with open(old_path, "r") as old:
            with open(new_path, "r") as new:
                # load new leaders
                new_line = ""
                new_attributes = []
                while not new_line.startswith("@data"):
                    new_line = new.readline()
                    if not new_line.startswith("@relation"):
                        new_attributes.append(new_line)
                # write to output file
                header = True
                for old_line in old:
                    # load old and new headers
                    if header:
                        if old_line.startswith("@data"):
                            header = False
                            fo.write(''.join(new_attributes))
                        elif not old_line.startswith("@attribute class"):
                            fo.write(old_line)
                    # join old and new feature vectors
                    else:
                        new_line = new.readline()
                        fo.write(','.join(old_line.split(",")[:-1])+','+new_line)
                        
def add_labels(no_tag_path, tag_path, out_path):
    with open(out_path, "w+") as fo:
        with open(no_tag_path, "r") as old:
            with open(tag_path, "r") as new:
                for old_line in old:
                    new_line = new.readline()
                    fo.write(old_line.replace('\n', '') + new_line)
                    
            
if __name__ == '__main__':

#     old_path = "features/temp.train.arff"
#     new_path = "features/3-7-15.train.arff"
#     out_path = "features/joined.train.arff"
#      
#     extend_features(old_path, new_path, out_path)
#     
#     old_path = "features/temp.test.arff"
#     new_path = "features/3-7-15.test.arff"
#     out_path = "features/joined.test.arff"
#     
#     extend_features(old_path, new_path, out_path)

    old_path = "data/coref-devset.notag"
    new_path = "data/dev predictions.txt"
    out_path = "data/dev.pred"
      
    add_labels(old_path, new_path, out_path)


    old_path = "data/coref-testset.notag"
    new_path = "data/final predictions.txt"
    out_path = "data/test.pred"
      
    add_labels(old_path, new_path, out_path)

    
    