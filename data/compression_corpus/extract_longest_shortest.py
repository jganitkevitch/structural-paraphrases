#!/usr/bin/python

import os, sys, codecs

def main():

  for line in sys.stdin:
    line = line.rstrip().lstrip()
    if (line == ""):
      continue
    refs = line.split("\t")
    
    shortest = refs[0]
    longest = refs[0]
    
    for r in refs:
      if (len(r.split()) <= 0):
        continue
      if (len(r.split()) < len(shortest.split())):
        shortest = r
      elif (len(r.split()) > len(longest.split())):
        longest = r
    
    ratio = float(len(shortest.split()))/len(longest.split())
    
    print str(ratio) + "\t" + longest + "\t" + shortest
    
    
if __name__ == "__main__":
    main()
