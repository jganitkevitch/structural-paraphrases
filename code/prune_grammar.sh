# runs after-the-fact pruning on a paraphrase grammar (this was used, unsuccessfully, to
# reduce the size of a Hiero grammar that was not count-threshold pruned)

cd $SGE_O_WORKDIR

java -Dfile.encoding=UTF8 -Xmx1g -cp /home/juri/decoders/joshua_juri/bin joshua.tools.PruneParaphraseGrammar -g $1 -k $2 -e $3 | gzip > $4
