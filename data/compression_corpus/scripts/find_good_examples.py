#!/usr/bin/python

import os, sys, codecs

# takes MTurk judgement outputs and produces:
# (a) a list of "good" example sentences
# (b) an analysis of the judgements

# assumes the format Courtney's eval scripts produces
# assumes further that our MAIN system is labeled "sys1" and 
# and that the main BASELINE is labeled "ilp" - this should 
# be easy enough to abstract


def main():
  
  file_names = sys.argv[1:]
  num_files = len(file_names)
  
  cand_lists = list()
  for n in file_names:
    current_candidates = list()
    file = codecs.open(n, "r", "utf-8")
    for line in file:
      current_candidates.append(line.rstrip().lstrip())
    cand_lists.append(current_candidates)
  output = codecs.open("EXAMPLES", "w", "utf-8")
  
  sent_data = list() 
  for i in range(561):
    sent_data.append(dict())
  
  for line in sys.stdin:
    line = line.rstrip().lstrip()
    f = line.split("\t")
    
    id = int(f[0])
    name = f[1]
    meaning = round(float(f[2]), 1)
    grammar = round(float(f[6]), 1)
    comp = round(float(f[10]), 1)
    
    sent_data[id][name] = (comp, meaning, grammar)
  
  total = 0
  booted = 0
  
  ilp_better_meaning = 0
  ilp_better_grammar = 0
  
  ilp_equal_meaning = 0
  ilp_equal_grammar = 0
  
  counts = [0] * len(cand_lists)
  meaning = dict()
  grammar = dict()
  compression = dict()
  s_counts = dict()
  
  for i,d in enumerate(sent_data[1:]):
    abort = False
    for cl in cand_lists:
      if (cl[i] == "<ERROR>" or cl[i] == "NULL"):
        # print "Skipping " + str(i) + "\t=> " + cl[i]
        booted += 1
        abort = True
        break
    if (abort):
      continue
    
    if ('sys1' not in d or 'ilp' not in d):
      booted += 1
      continue
    
    if (d['sys1'][0] == 1.0):
      booted += 1
      continue
    
    for s in d:
      if (s not in meaning):
        meaning[s] = 0.0
      meaning[s] += d[s][1]
      
      if (s not in grammar):
        grammar[s] = 0.0
      grammar[s] += d[s][2]
      
      if (s not in compression):
        compression[s] = 0.0
      compression[s] += d[s][0]
      
      if (s not in s_counts):
        s_counts[s] = 0
      s_counts[s] += 1
    
    for j, cl in enumerate(cand_lists):
      counts[j] += len(cl[i].split())
    
    total += 1
    
    if (d['sys1'][1] < d['ilp'][1]):
      ilp_better_meaning += 1
    if (d['sys1'][1] == d['ilp'][1]):
      ilp_equal_meaning += 1
    if (d['sys1'][2] < d['ilp'][2]):
      ilp_better_grammar += 1
    if (d['sys1'][2] == d['ilp'][2]):
      ilp_equal_grammar += 1
    
    if (d['sys1'][1] > d['ilp'][1] and d['sys1'][2] > d['ilp'][2]):
      output.write("\t".join(map(str, [i+1, d['sys1'][1], d['sys1'][2], 
          d['ilp'][1], d['ilp'][2]])) + "\n")
      for cl in cand_lists:
        output.write(cl[i] + "\n")
      output.write("\n\n")
  
  print "Total: " + str(total)
  print "Booted: " + str(booted)
  print "ilp_better_meaning: " + str(ilp_better_meaning)
  print "ilp_better_grammar: " + str(ilp_better_grammar)
  print "ilp_equal_meaning: " + str(ilp_equal_meaning)
  print "ilp_equal_grammar: " + str(ilp_equal_grammar)
  print "syn_better_meaning: " + str(total - ilp_equal_meaning - ilp_better_meaning)
  print "syn_better_grammar: " + str(total - ilp_equal_grammar - ilp_better_grammar)
  
  print "\n"
  
  for i,c in enumerate(counts):
    print str(round(float(c)/counts[0], 2)) + "\t" + file_names[i]
  
  print "\n"
    
  for c in compression:
    t = s_counts[c]
    print "\t".join(map(str, [c[:4], compression[c]/t, meaning[c]/t, 
        grammar[c]/t, t]))
    
if __name__ == "__main__":
    main()
