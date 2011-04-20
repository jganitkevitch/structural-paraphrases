# sorts SAMT-formatted translation grammar by lhs-and-source in preparation for pivoting

zcat /mnt/data/juri/paraphrasing/europarl_v5/es-en/m8_slice_000/filteredrules_sorted.gz | \
/home/juri/tools/bin/sort --parallel=8 -T /mnt/data/juri/tmp -t "#" -k1,1 -k3,3 | \
gzip > /mnt/data/juri/paraphrasing/europarl_v5/es-en/translation_grammar_samt_es-en.gz
