'''
Created on Mar 6, 2015

@author: Aaron Levine

Function for taking an new .arff feature vector document,
and appending it's data to the end of another feature vector document
run on the same dataset.

FILES MUST HAVE BEEN RUN ON THE SAME DATASET!
'''

def extend_features(old_path, new_path, out_path):
    with open(old_path, "w+") as fo:
        with open(new_path, "r") as old:
            with open(out_path, "r") as new:
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
                        fo.write(','.join(old_line.split(",")[:-1]) + new_line)
                        
if __name__ == '__old__':
    old_path, new_path, out_path = ["3-5-15.train.arff",
                                    "3-6-15.train.arff",
                                    "joined.train.arff"]
    
    extend_features(old_path, new_path, out_path)
