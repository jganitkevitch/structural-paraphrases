#!/usr/bin/python

import os, sys, codecs

def usage():
  print "Usage info for postfilter_grammar.py"
  print "  postfilter_grammar.py -drop_identity index index ..."
  print "Where:"
  print "  stdin          - pipe in Joshua-formatted SAMT grammar"
  print "  stdout         - pipes out Joshua-formatted post-filtered SAMT grammar"
  print "  -drop_x        - whether to drop [_X] rules"
  print "  -drop_identity - whether to drop identity paraphrasing rules"
  print "  index          - feature to drop: index (i.e. '2') or range (i.e. '0-4')"
  print
  sys.exit()

def main():
  arguments = sys.argv[1:]
  
  if (len(arguments) == 0):
    usage()
  
  featureIndices = []
  drop_identity = False
  drop_x = False
  
  for i in arguments:
    if (i == "-drop_identity"):
      drop_identity = True
      continue
    if (i == "-drop_x"):
      drop_x = True
      continue
    try:
      index = int(i)
      featureIndices.append(index)
    except ValueError:
      try:
        bounds = i.split("-")
        
        start = int(bounds[0])
        end = int(bounds[1])
        featureIndices.extend(range(start, end+1))
      except:
        print "[ERR]    Wrong argument formatting.\n"
        usage()
  
  out = []
  
  for line in sys.stdin:
    (head, src, tgt, featureString) = line.rstrip().lstrip().split(" ||| ")
    
    if (drop_x and (head == "[_X]" or src.find("[_X,") != -1)):
      continue
    
    # drop useless identity unary rules
    if (head[1:-1] == src[1:-3]):
      continue

    featureScores = featureString.split(" ")
    
    if (drop_identity and featureScores[2] == "1.0"):
      continue
    
    filteredScores = []
    for (i, v) in enumerate(featureScores): 
      if (i not in featureIndices):
        filteredScores.append(v)
    
    sys.stdout.write(head  + ' ||| ' + src + ' ||| ' + 
      tgt + ' ||| ' + (" ".join(filteredScores)) + "\n")
    
    
if __name__ == "__main__":
    main()
