#!/usr/bin/python

import random, os, sys, codecs

def main():
  
  in_file = sys.argv[1]
  
  input = codecs.open(in_file, "r", "utf-8")
  output = codecs.open(in_file + ".lc", "w", "utf-8")
  for line in input:
    line = line.rstrip().lstrip()
    tokens = line.split()
    lowered = list()
    for t in tokens:
      if (t[0] != '('):
        t = t.lower()
      lowered.append(t)
    output.write(" ".join(lowered) + "\n")
  input.close()
  output.close()
    
if __name__ == "__main__":
    main()
