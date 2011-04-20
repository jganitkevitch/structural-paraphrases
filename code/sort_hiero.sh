# sorts Hiero-formatted translation grammar by source side in preparation for pivoting

zcat /mnt/data/juri/paraphrasing/hiero/fr-en.hiero.gz | \
sort -T /mnt/data/juri/tmp -t "|" -k4,4 | \
gzip > /mnt/data/juri/paraphrasing/hiero/translation_grammar_hiero_fr-en.gz
