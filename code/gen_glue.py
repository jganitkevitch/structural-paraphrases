#!/usr/bin/python

import os, sys, codecs

def usage():
  print "Usage info for gen_glue.py"
  print "  gen_glue.py"
  print "Where:"
  print "  stdin    - pipe in list of nonterminals"
  print "  stdout   - pipes out Joshua-formatted glue grammar"
  print
  sys.exit()

def main():
  
  if (len(sys.args) > 1 and (sys.args[1] == "-h" or sys.args[1] == "--help")):
    usage()
  
  for nt in sys.stdin:
    nt = nt.rstrip().lstrip()
    
    weights = ["0"] * 16
    
    # glue rule feature
    weights[0] = "1"
    # application count
    weights[1] = "1"
    # identity
    weights[2] = "1"

    # mock probabilities
    weights[3] = "1"
    weights[4] = "1"
    weights[5] = "1"
    weights[6] = "1"
    
    print "[GOAL] ||| [%s,1] ||| [%s,1] ||| %s" % (nt, nt, " ".join(weights))
    print "[GOAL] ||| [GOAL,1] [%s,2] ||| [GOAL,1] [%s,2] ||| %s" % (nt, nt, " ".join(weights))
    
    
if __name__ == "__main__":
    main()
