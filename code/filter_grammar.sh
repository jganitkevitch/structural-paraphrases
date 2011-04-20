cd $SGE_O_WORKDIR

# wrapper for grammar test-set-filtering

zcat ${1} | \
  ~/experiments/paraphrasing/scripts_coe/convert.perl | \
  java -cp $THRAX/bin edu.jhu.thrax.util.TestSetFilter 8 ${3} | \
  gzip > ${2}
