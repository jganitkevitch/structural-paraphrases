#!/usr/bin/python

import random, os, sys, codecs

def main():
  
  corpus = list()
  corpus_file = codecs.open("long_short_by_words_0.5_0.8", "r", "utf-8")
  
  for line in corpus_file:
    line = line.rstrip().lstrip()
    if (line == ""):
      continue
    (ratio, long, short) = line.split("\t")
    corpus.append((long, short))
  
  random.shuffle(corpus)
  
  dev_src_file = codecs.open("dev_src", "w", "utf-8")
  dev_ref_file = codecs.open("dev_ref", "w", "utf-8")
  test_src_file = codecs.open("test_src", "w", "utf-8")
  test_ref_file = codecs.open("test_ref", "w", "utf-8")
  
  for (l, s) in corpus[:1000]:
    dev_src_file.write(l + "\n")
    dev_ref_file.write(s + "\n")
    
  for (l, s) in corpus[1000:2000]:
    test_src_file.write(l + "\n")
    test_ref_file.write(s + "\n")
    
  dev_src_file.close()
  dev_ref_file.close()
  test_src_file.close()
  test_ref_file.close()
    
if __name__ == "__main__":
    main()
