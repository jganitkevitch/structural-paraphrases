#!/usr/bin/python

# for unknown reasons, the usual Perl lowercaser wouldn't work, 
# this is a Python version that does the exact same thing:

# lowercases the text; works with parsed input (detects and doesn't 
# touch the constituent labels)

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
