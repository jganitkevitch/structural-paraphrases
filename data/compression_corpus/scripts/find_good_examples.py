#!/opt/local/bin/python

import os, sys, codecs
from scipy.stats import binom_test

# Takes MTurk judgement outputs and produces:
# (a) a list of "good" example sentences
# (b) an analysis of the judgements

def main():
  
  primary = sys.argv[1]
  contrastive = sys.argv[2]
  
  sent_file_name = sys.argv[3]
  
  have_compressions = False
  num_files = 0
  if (len(sys.argv) > 5):
    have_compressions = True
    file_names = sys.argv[4:]
    num_files = len(file_names)
    num_sent = 0
  else:
    num_sent = int(sys.argv[4])
  
  sent_filter = dict()
  sent_file = codecs.open(sent_file_name, "r", "utf-8")
  for line in sent_file:
    (id, slice) = line.rstrip().lstrip().split("\t")
    id = int(id)
    if (slice not in sent_filter):
      sent_filter[slice] = set()
    sent_filter[slice].add(id)
  
  cand_lists = list()
  if (have_compressions):
    # Read compression single-best outputs.
    for n in file_names:
      current_candidates = list()
      file = codecs.open(n, "r", "utf-8")
      for line in file:
        current_candidates.append(line.rstrip().lstrip())
      cand_lists.append(current_candidates)
      num_sent = len(current_candidates)
    # Open output file for good example sentences.
    output = codecs.open("EXAMPLES", "w", "utf-8")
  
  sent_data = list() 
  for i in range(num_sent):
    sent_data.append(dict())
  
  for line in sys.stdin:
    line = line.rstrip().lstrip()
    f = line.split("\t")
    
    id = int(f[0])
    sys_name = f[1]
    sys_slice = f[2]
    meaning = round(float(f[4]), 1)
    grammar = round(float(f[8]), 1)
    comp = round(float(f[3]), 1)
    
    if (True or id in sent_filter[sys_slice]):
      name = sys_name + "_" + sys_slice
      sent_data[id][name] = (comp, meaning, grammar)
  
  total = 0
  booted = 0
  no_overlap = 0
  
  c_better_meaning = 0
  c_better_grammar = 0
  
  c_equal_meaning = 0
  c_equal_grammar = 0
  
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
    
    if (primary not in d or contrastive not in d):
      booted += 1
      no_overlap += 1
      continue
    
    if (d[primary][0] == 1.0):
      booted += 1
      continue
    
    if (abs(d[primary][0] - d[contrastive][0]) > 0.05):
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
    
    # print d[primary]
    # print d[contrastive] 
    # print
    
    if (d[primary][1] < d[contrastive][1]):
      c_better_meaning += 1
    if (d[primary][1] == d[contrastive][1]):
      c_equal_meaning += 1
    if (d[primary][2] < d[contrastive][2]):
      c_better_grammar += 1
    if (d[primary][2] == d[contrastive][2]):
      c_equal_grammar += 1
    
    if (have_compressions and d[primary][1] > d[contrastive][1] 
        and d[primary][2] > d[contrastive][2]):
      output.write("\t".join(map(str, [i+1, d[primary][1], d[primary][2], 
          d[contrastive][1], d[contrastive][2]])) + "\n")
      for cl in cand_lists:
        output.write(cl[i] + "\n")
      output.write("\n\n")
  
  print "Total: " + str(total)
  print "Booted: " + str(booted)
  print "No overlap: " + str(no_overlap)
  print contrastive + " better_meaning: " + str(c_better_meaning)
  print contrastive + " better_grammar: " + str(c_better_grammar)
  print
  print contrastive + " equal_meaning: " + str(c_equal_meaning)
  print contrastive + " equal_grammar: " + str(c_equal_grammar)
  print
  print(primary + " better_meaning: " 
      + str(total - c_equal_meaning - c_better_meaning))
  print(primary + " better_grammar: "
      + str(total - c_equal_grammar - c_better_grammar))

  print "\n"
  m_p_val = binom_test(total - c_equal_meaning - c_better_meaning,
      total - c_equal_meaning)
  if (c_better_meaning > total - c_equal_meaning - c_better_meaning):
    m_p_val = 1 - m_p_val
  if (m_p_val > 0.1):
    print "MEANING OUCH (" + "%5f" % m_p_val  + ")"
  else:
    print "MEANING P-VALUE: " + "%5f" % m_p_val
  g_p_val = binom_test(total - c_equal_grammar - c_better_grammar,
      total - c_equal_grammar)
  if (c_better_grammar > total - c_equal_grammar - c_better_grammar):
    g_p_val = 1 - g_p_val
  if (g_p_val > 0.1):
    print "GRAMMAR OUCH (" + "%5f" % g_p_val  + ")"
  else:
    print "GRAMMAR P-VALUE: " + "%5f" % g_p_val


  if (have_compressions):
    print "\n"
    for i,c in enumerate(counts):
      print str(round(float(c)/counts[0], 2)) + "\t" + file_names[i]
  
  print "\n"
  print "SYSTEM\t\tCR\t\tMEANING\t\tGRAMMAR"
  for c in [primary, contrastive]:
    t = s_counts[c]
    print "\t".join(map(str, [c[:14], compression[c]/t, meaning[c]/t, 
        grammar[c]/t, t]))
    
if __name__ == "__main__":
    main()
