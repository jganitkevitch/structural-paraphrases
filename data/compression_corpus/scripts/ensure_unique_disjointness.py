#!/usr/bin/python

import random, os, sys, codecs

# after-the-fact script to make sure the sentences in dev and test 
# sets are unique and don't overlap - with the update to shuffle_and_slice.py 
# this should be obsolete

def main():
  
  dev_src_file = sys.argv[1]
  dev_ref_file = sys.argv[2]
  dev_src_p_file = sys.argv[3]
  dev_ref_p_file = sys.argv[4]
  
  test_src_file = sys.argv[5]
  test_ref_file = sys.argv[6]
  test_src_p_file = sys.argv[7]
  test_ref_p_file = sys.argv[8]
  
  dev_src_in = codecs.open(dev_src_file, "r", "utf-8")
  dev_ref_in = codecs.open(dev_ref_file, "r", "utf-8")
  dev_src_p_in = codecs.open(dev_src_p_file, "r", "utf-8")
  dev_ref_p_in = codecs.open(dev_ref_p_file, "r", "utf-8")
  
  dev_src_out = codecs.open(dev_src_file + ".du", "w", "utf-8")
  dev_ref_out = codecs.open(dev_ref_file + ".du", "w", "utf-8")
  dev_src_p_out = codecs.open(dev_src_p_file + ".du", "w", "utf-8")
  dev_ref_p_out = codecs.open(dev_ref_p_file + ".du", "w", "utf-8")
  
  test_src_in = codecs.open(test_src_file, "r", "utf-8")
  test_ref_in = codecs.open(test_ref_file, "r", "utf-8")
  test_src_p_in = codecs.open(test_src_p_file, "r", "utf-8")
  test_ref_p_in = codecs.open(test_ref_p_file, "r", "utf-8")
  
  test_src_out = codecs.open(test_src_file + ".du", "w", "utf-8")
  test_ref_out = codecs.open(test_ref_file + ".du", "w", "utf-8")
  test_src_p_out = codecs.open(test_src_p_file + ".du", "w", "utf-8")
  test_ref_p_out = codecs.open(test_ref_p_file + ".du", "w", "utf-8")
  
  seen = set()
  for s, r, sp, rp in zip(dev_src_in, dev_ref_in, dev_src_p_in, dev_ref_p_in):
    if (s not in seen):
      dev_src_out.write(s)
      dev_ref_out.write(r)
      dev_src_p_out.write(sp)
      dev_ref_p_out.write(rp)
      seen.add(s)
  dev_src_in.close()
  dev_ref_in.close()
  dev_src_p_in.close()
  dev_ref_p_in.close()
  dev_src_out.close()
  dev_ref_out.close()
  dev_src_p_out.close()
  dev_ref_p_out.close()
  
  for s, r, sp, rp in zip(test_src_in, test_ref_in, test_src_p_in, test_ref_p_in):
    if (s not in seen):
      test_src_out.write(s)
      test_ref_out.write(r)
      test_src_p_out.write(sp)
      test_ref_p_out.write(rp)
      seen.add(s)
  test_src_in.close()
  test_ref_in.close()
  test_src_p_in.close()
  test_ref_p_in.close()
  test_src_out.close()
  test_ref_out.close()
  test_src_p_out.close()
  test_ref_p_out.close()


if __name__ == "__main__":
    main()
