cd $SGE_O_WORKDIR

# aggregates an SAMT paraphrase grammar (identical rules obtained through 
# different pivots are collapsed and features are adjusted, i.e. sum probabilities)

java -Dfile.encoding=UTF8 -Xmx1g -cp /home/juri/decoders/joshua_juri/bin joshua.tools.AggregateParaphraseGrammar -g $1 | gzip > $2
