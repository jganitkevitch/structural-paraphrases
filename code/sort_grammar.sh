# sorts Hiero-formatted paraphrase grammar by entire rule (lhs-src-tgt) in preparation for aggregation

cd $SGE_O_WORKDIR

#zcat $1 | /home/juri/tools/bin/sort --parallel=8 -T /mnt/data/juri/tmp -t "|" -k4,4 | gzip > $2

zcat $1 | /home/juri/tools/bin/sort --parallel=8 -T /mnt/data/juri/tmp -t "|" -k1,7 | gzip > $2
