#!/usr/bin/python

import os, sys, codecs, re

# a script to extract a simplification corpus in the same 
# way as we extracted the compression corpus from MT references

# uses an impressively arbitrary interpolation of unigram LM scores, 
# chars-per-word and ratio of pseudo-stemmed words from a basic English 
# dictionary


def score(ref):
  global basic_words, unigram_logp
  
  tokens = map(lambda x: x.lower(), ref.split())
  words = list()
  for t in tokens:
    if (re.match("[a-z$0-9]+", t)):
      words.append(t)
  
  if (len(words) == 0):
    return 0
  
  basic_count = 0
  for w in words:
    if (w[:5].lower() in basic_words):
      basic_count += 1
  complex_ratio = 1.0 - (float(basic_count) / len(words))
  
  avg_word_len = float(len(ref) - len(words) + 1) / len(words)
  
  avg_unigram_logp = 0.0
  for w in words:
    if (w in unigram_logp): 
      avg_unigram_logp += unigram_logp[w]
    else:
      avg_unigram_logp += -8
  avg_unigram_logp /= -len(words)
  
  return complex_ratio + avg_word_len + avg_unigram_logp
  



def main():
  global basic_words, unigram_logp
  
  dictionary_file = codecs.open("basic_english_dict", "r", "utf-8")
  basic_words = set()
  for w in dictionary_file:
    basic_words.add(w.lstrip().rstrip()[:5].lower())
  
  unigram_file = codecs.open("unigrams", "r", "utf-8")
  unigram_logp = dict()
  for l in unigram_file:
    logp, w = l.lstrip().rstrip().split("\t")
    unigram_logp[w.lower()] = float(logp)
  
  for line in sys.stdin:
    line = line.rstrip().lstrip()
    if (line == ""):
      continue
    refs = line.split("\t")
    
    simplest = refs[0]
    simplest_score = 10000
    most_complex = refs[0]
    most_complex_score = -10000
    
    for r in refs:
      if (len(r.split()) <= 0):
        continue
      s = score(r)
      
      if (s > most_complex_score):
        most_complex = r
        most_complex_score = s
      
      if (s < simplest_score):
        simplest = r
        simplest_score = s
    
    difference = simplest_score - most_complex_score
    
    print "\t".join([str(difference), str(most_complex_score), str(simplest_score), str(most_complex), str(simplest)])
    
    
if __name__ == "__main__":
    main()
