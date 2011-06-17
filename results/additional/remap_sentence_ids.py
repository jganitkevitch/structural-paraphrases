#!/opt/local/bin/python

import os, sys, codecs
from scipy.stats import binom_test

# Takes MTurk judgement outputs and produces:
# (a) a list of "good" example sentences
# (b) an analysis of the judgements

def main():
  
  sent_file_name = sys.argv[1]
  sent_num = int(sys.argv[2])
  
  dropped_ids = []
  sent_file = codecs.open(sent_file_name, "r", "utf-8")
  for line in sent_file:
    id = int(line.rstrip().lstrip())
    dropped_ids.append(id)
  dropped_ids.sort()
  
  dropped_offset = 0
  id_map = dict()
  for old_id in range(sent_num):
    if (old_id in dropped_ids):
      dropped_offset += 1
    else:
      id_map[old_id] = old_id - dropped_offset
  
  for line in sys.stdin:
    line = line.rstrip().lstrip()
    f = line.split("\t")    
    old_id = int(f[0])
    if (old_id not in dropped_ids):
      f[0] = str(id_map[old_id])
      print "\t".join(f)
 
    
if __name__ == "__main__":
    main()
