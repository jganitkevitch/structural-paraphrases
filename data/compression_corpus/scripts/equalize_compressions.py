#!/usr/bin/python

import random, os, sys, codecs

# takes a set of nbest-lists from different systems and equalizes the 
# compression rates for each sentence for a more fair evaluation

# in turn, each system gets to lead. the leading system's first-best 
# compression is selected for output, the other systems' nbest-lists 
# are searched for candidate compressions that are close in CR.


def main():
  
  min_sent = int(sys.argv[1])
  max_sent = int(sys.argv[2])
  
  slack = int(sys.argv[3])
  
  nbest_names = sys.argv[4:]
  num_nbest = len(nbest_names)
  
  nbest_files = list()
  select_files = list()
  for n in nbest_names:
    nbest_files.append(codecs.open(n, "r", "utf-8"))
    select_files.append(codecs.open(n + ".select_%03d_%03d_%02d" 
      % (min_sent, max_sent, slack), "w", "utf-8"))
  
  nbest_list = list()
  for file in nbest_files:
    this_nbest = list()
    last_id = -1
    current_sentence = list()
    for cand_line in file:
      id, cand, feats, score = cand_line.split(" ||| ")
      length = len(cand.split())
      if (last_id != id and id != "0"):
        this_nbest.append(current_sentence)
        current_sentence = list()
      last_id = id
      if (int(id) < min_sent or int(id) >= max_sent):
        continue
      current_sentence.append((length, cand))
    this_nbest.append(current_sentence)
    nbest_list.append(this_nbest)
  
  rank_sum = 0
  num_sent = max_sent - min_sent
  current_gold = 0
  current_index = [0] * num_nbest
  for i in xrange(min_sent, max_sent):
    for j in xrange(num_nbest):
      current_index[j] = 0
    current_gold = i % num_nbest
    current_len = nbest_list[current_gold][i][0][0]
    
    print("LIST " + nbest_names[current_gold]
        + " DECIDING ON SENTENCE " + str(i) 
        + ", CALLING FOR " + str(current_len))
    
    for j in xrange(num_nbest):
      k = current_index[j]
      min_dist = 10000
      while (k < len(nbest_list[j][i])):
        dist = abs(nbest_list[j][i][k][0] - current_len)
        if (dist < min_dist):
          min_dist = dist
          current_index[j] = k
        if (min_dist <= slack):
          break
        k += 1
      select_files[j].write(nbest_list[j][i][current_index[j]][1] + "\n")
      rank_sum += current_index[j]
  
  print "FINISHED."
  print "AVERAGE RANK SELECTED: " + str(float(rank_sum) / (num_nbest * num_sent))
  
  for i in xrange(num_nbest):
    nbest_files[i].close()
    select_files[i].close()


if __name__ == "__main__":
    main()
