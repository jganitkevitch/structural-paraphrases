cd $SGE_O_WORKDIR

# extacts a Hiero paraphrase grammar

java -Dfile.encoding=UTF8 -Xmx1g -cp $JOSHUA/bin \
   joshua.tools.BuildParaphraseGrammar -g $1 -hiero -min_c 10 | \
   gzip > $2

# -min_c $3 -min_p $4 -top $5
